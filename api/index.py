import os
import json
import httpx
from datetime import datetime, timezone, timedelta
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from upstash_redis import Redis
from zoneinfo import ZoneInfo

pt = ZoneInfo("America/Los_Angeles")

def pt_now() -> datetime:
    return datetime.now(timezone.utc).astimezone(pt)

def pt_today() -> str:
    return pt_now().strftime("%Y-%m-%d")

def pt_time_str(dt_utc: datetime) -> str:
    return dt_utc.astimezone(pt).strftime("%H:%M")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── ENV VARS (set in Vercel dashboard) ──────────────────
TWITCH_CLIENT_ID     = os.environ.get("TWITCH_CLIENT_ID", "")
TWITCH_CLIENT_SECRET = os.environ.get("TWITCH_CLIENT_SECRET", "")
STREAMER_LOGIN       = os.environ.get("STREAMER_LOGIN", "licky_t")
KV_URL               = os.environ.get("KV_REST_API_URL", "")
KV_TOKEN             = os.environ.get("KV_REST_API_TOKEN", "")
ADMIN_SECRET         = os.environ.get("ADMIN_SECRET", "")  # required to run the backfill endpoint

# Scheduled start = 1:40 PM PT (countdown target).
# Late after 2:00 PM PT (1:40 + 20m grace).
SCHEDULED_HOUR_PT = 13   # 1 PM
SCHEDULED_MIN_PT  = 40   # :40
LATE_GRACE_MINS   = 20   # grace before a stream is counted as late

# ── REDIS ────────────────────────────────────────────────
def get_redis():
    if not KV_URL or not KV_TOKEN:
        raise HTTPException(status_code=503, detail="Redis not configured")
    return Redis(url=KV_URL, token=KV_TOKEN)

# ── TWITCH TOKEN CACHE ───────────────────────────────────
_token_cache = {"token": None, "expires_at": 0}

async def get_twitch_token() -> str:
    now = datetime.now(timezone.utc).timestamp()
    if _token_cache["token"] and now < _token_cache["expires_at"] - 60:
        return _token_cache["token"]
    async with httpx.AsyncClient() as client:
        r = await client.post(
            "https://id.twitch.tv/oauth2/token",
            params={
                "client_id": TWITCH_CLIENT_ID,
                "client_secret": TWITCH_CLIENT_SECRET,
                "grant_type": "client_credentials",
            }
        )
        r.raise_for_status()
        data = r.json()
        _token_cache["token"] = data["access_token"]
        _token_cache["expires_at"] = now + data["expires_in"]
        return data["access_token"]

# ── HELPERS ──────────────────────────────────────────────


def calc_late_mins(start_hhmm: str) -> int:
    h, m = map(int, start_hhmm.split(":"))
    actual_mins    = h * 60 + m
    scheduled_mins = SCHEDULED_HOUR_PT * 60 + SCHEDULED_MIN_PT
    # grace applied universally
    return max(0, actual_mins - (scheduled_mins + LATE_GRACE_MINS))

# ── ROUTES ───────────────────────────────────────────────

from fastapi import Response

def _try_finalize_stale_current_stream(r: Redis):
    cached_raw = r.get("current_stream")
    if not cached_raw:
        return False

    cached = normalize_session(json.loads(cached_raw))
    started_at_utc = datetime.fromisoformat(cached["started_at"].replace("Z", "+00:00"))
    now_utc = datetime.now(timezone.utc)
    age_minutes = (now_utc - started_at_utc).total_seconds() / 60

    if age_minutes < 15:
        return False

    duration_hours = round((now_utc - started_at_utc).total_seconds() / 3600, 2)
    _save_completed_stream(r, cached, duration_hours)
    r.delete("current_stream")
    return True

def normalize_session(session: dict) -> dict:
    # Handle older key name "started_pst" (from earlier builds)
    if "started_pt" not in session and "started_pst" in session:
        session["started_pt"] = session["started_pst"]
    return session

@app.api_route("/api/status", methods=["GET", "HEAD"])
async def get_status():
    """
    Poll Twitch. Auto-detect going live and going offline.
    When going live: record stream start in Redis.
    When going offline: calculate duration, save completed stream.
    """
    r = get_redis()

    if not TWITCH_CLIENT_ID or not TWITCH_CLIENT_SECRET:
        _try_finalize_stale_current_stream(r)
        return {"live": False, "error": "Twitch not configured", **_get_community_data(r)}

    try:
        token = await get_twitch_token()
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                "https://api.twitch.tv/helix/streams",
                params={"user_login": STREAMER_LOGIN},
                headers={
                    "Client-ID": TWITCH_CLIENT_ID,
                    "Authorization": f"Bearer {token}",
                }
            )
            resp.raise_for_status()
            data = resp.json()

        # ── IS HE LIVE? ──────────────────────────────────
        if data.get("data"):
            stream = data["data"][0]
            started_at_utc = datetime.fromisoformat(stream["started_at"].replace("Z", "+00:00"))
            started_pt = pt_time_str(started_at_utc)

            # Check if we already know about this stream session
            cached_raw = r.get("current_stream")
            cached = json.loads(cached_raw) if cached_raw else None

            if not cached or cached.get("started_at") != stream["started_at"]:
                # New stream detected — record it
                today = pt_today()
                late_mins = calc_late_mins(started_pt)
                new_session = {
                    "started_at": stream["started_at"],
                    "started_pt": started_pt,
                    "date": today,
                    "late_mins": late_mins,
                }
                r.set("current_stream", json.dumps(new_session))

            return {
                "live": True,
                "started_at": stream["started_at"],
                "started_pt": started_pt,
                "viewer_count": stream["viewer_count"],
                "title": stream.get("title", ""),
                **_get_community_data(r),
            }

        else:
            # ── HE'S OFFLINE ─────────────────────────────
            cached_raw = r.get("current_stream")
            if cached_raw:
                # Stream just ended — calculate duration and save
                cached = normalize_session(json.loads(cached_raw))
                started_at_utc = datetime.fromisoformat(cached["started_at"].replace("Z", "+00:00"))
                ended_at_utc = datetime.now(timezone.utc)
                duration_hours = round((ended_at_utc - started_at_utc).total_seconds() / 3600, 2)

                # Only save if stream was at least 1 minutes (avoid false positives)
                if duration_hours >= (1 / 60):
                    _save_completed_stream(r, cached, duration_hours)

                # Clear the active session
                r.delete("current_stream")

            return {
                "live": False,
                **_get_community_data(r),
            }

    except Exception as e:
        try:
            r = get_redis()
            _try_finalize_stale_current_stream(r)
            return {"live": False, "error": str(e), **_get_community_data(r)}
        except Exception as e2:
            return {"live": False, "error": f"{e} | redis_finalize_failed: {e2}", "streams": [], "votes": {}, "length_votes": {}}


def _save_completed_stream(r, session: dict, duration_hours: float):
    """Append a completed stream to the history list."""
    session = normalize_session(session)
    raw = r.get("streams")
    streams = json.loads(raw) if raw else []
    

    # Don't double-save the same session
    for s in streams:
        if s.get("started_at") == session["started_at"]:
            return

    # Snapshot today's votes into the stream record (so votes persist)
    date = session["date"]
    vkey  = f"votes:{date}"
    lvkey = f"length_votes:{date}"

    vraw  = r.get(vkey)
    lvraw = r.get(lvkey)

    day_votes = json.loads(vraw) if vraw else {"ontime": 0, "late": 0}
    day_len   = json.loads(lvraw) if lvraw else {k: 0 for k in ["lt6","6to8","8to10","10to12","12plus"]}

    streams.append({
        "date": date,
        "startTime": session["started_pt"],
        "started_at": session["started_at"],
        # Recompute against the current cutoff at save time
        # (don't trust the late_mins stamped at go-live).
        "late_mins": calc_late_mins(session["started_pt"]),
        "duration": duration_hours,

        # NEW: persisted community sentiment for that stream-day
        "votes": day_votes,
        "length_votes": day_len,
    })

    r.set("streams", json.dumps(streams))

def _get_community_data(r) -> dict:
    today = pt_today()
    vraw  = r.get(f"votes:{today}")
    lvraw = r.get(f"length_votes:{today}")
    sraw  = r.get("streams")
    return {
        "votes":        json.loads(vraw)  if vraw  else {"ontime": 0, "late": 0},
        "length_votes": json.loads(lvraw) if lvraw else {k: 0 for k in ["lt6","6to8","8to10","10to12","12plus"]},
        "streams":      json.loads(sraw)  if sraw  else [],
    }


@app.get("/api/streams")
async def get_streams():
    r = get_redis()
    raw = r.get("streams")
    return {"streams": json.loads(raw) if raw else []}


@app.get("/api/votes")
async def get_votes():
    r = get_redis()
    today = pt_today()
    vraw  = r.get(f"votes:{today}")
    lvraw = r.get(f"length_votes:{today}")
    return {
        "votes":        json.loads(vraw)  if vraw  else {"ontime": 0, "late": 0},
        "length_votes": json.loads(lvraw) if lvraw else {k: 0 for k in ["lt6","6to8","8to10","10to12","12plus"]},
        "date": today,
    }


class VoteBody(BaseModel):
    type: str  # "ontime" | "late"

@app.post("/api/votes")
async def cast_vote(body: VoteBody):
    if body.type not in ("ontime", "late"):
        raise HTTPException(status_code=400, detail="type must be 'ontime' or 'late'")
    r = get_redis()
    today = pt_today()
    key = f"votes:{today}"
    raw = r.get(key)
    votes = json.loads(raw) if raw else {"ontime": 0, "late": 0}
    votes[body.type] = votes.get(body.type, 0) + 1
    r.set(key, json.dumps(votes))
    r.expire(key, 60 * 60 * 48)  # auto-expire after 48h
    return {"ok": True, "votes": votes} 


class LengthVoteBody(BaseModel):
    bucket: str

@app.post("/api/votes/length")
async def cast_length_vote(body: LengthVoteBody):
    valid = {"lt6", "6to8", "8to10", "10to12", "12plus"}
    if body.bucket not in valid:
        raise HTTPException(status_code=400, detail="Invalid bucket")
    r = get_redis()
    today = pt_today()
    key = f"length_votes:{today}"
    raw = r.get(key)
    votes = json.loads(raw) if raw else {k: 0 for k in valid}
    votes[body.bucket] = votes.get(body.bucket, 0) + 1
    r.set(key, json.dumps(votes))
    r.expire(key, 60 * 60 * 48)
    return {"ok": True, "length_votes": votes}


# ── ONE-TIME BACKFILL ────────────────────────────────────
@app.post("/api/admin/recompute-late")
async def recompute_late(secret: str = "", dry_run: bool = False, from_date: str = "2026-06-01"):
    """
    One-time backfill: recompute late/on-time for every saved stream dated
    `from_date` or later, using the current cutoff (1:40 PM + 20m grace = 2:00 PM PT).

    Requires ?secret=... matching the ADMIN_SECRET env var (set it in the Vercel dashboard).

    `from_date` (YYYY-MM-DD) is the day the 1:40 PM schedule took effect. Streams
    before it keep their stored values (they were graded against the old schedule).
    Defaults to 2026-06-01, when start times settle onto the 1:40 PM target.

    Before committing, the current streams list is snapshotted to
    streams:backup:<timestamp> so a bad run can be rolled back.

    Usage (replace YOURSECRET):
      1) POST /api/admin/recompute-late?secret=YOURSECRET&dry_run=true                      -> preview, changes nothing
      2) POST /api/admin/recompute-late?secret=YOURSECRET&dry_run=true&from_date=2026-05-15 -> preview a different cutover
      3) POST /api/admin/recompute-late?secret=YOURSECRET                                   -> commit the changes (runs once)

    Idempotent: it always recomputes from each stream's recorded start time, so
    re-running produces the same result. A Redis flag (migration:late_cutoff_2pm)
    blocks accidental re-commits. To intentionally re-run later, delete that key first.
    """
    if not ADMIN_SECRET:
        raise HTTPException(status_code=503, detail="ADMIN_SECRET not configured on the server")
    if secret != ADMIN_SECRET:
        raise HTTPException(status_code=401, detail="bad or missing secret")

    r = get_redis()

    if not dry_run and r.get("migration:late_cutoff_2pm"):
        return {
            "ok": False,
            "skipped": True,
            "reason": "already migrated (delete key migration:late_cutoff_2pm to force a re-run)",
        }

    raw = r.get("streams")
    streams = json.loads(raw) if raw else []

    changes = []
    for s in streams:
        # Only touch streams on/after the cutover date
        if s.get("date", "") < from_date:
            continue

        hhmm = s.get("startTime")
        if not hhmm and s.get("started_at"):  # fallback for any older record missing startTime
            dt = datetime.fromisoformat(s["started_at"].replace("Z", "+00:00"))
            hhmm = pt_time_str(dt)
        if not hhmm:
            continue

        old_late = s.get("late_mins", 0)
        new_late = calc_late_mins(hhmm)

        if old_late != new_late:
            changes.append({
                "date": s.get("date"),
                "startTime": hhmm,
                "old": f"{old_late}m ({'late' if old_late > 0 else 'ontime'})",
                "new": f"{new_late}m ({'late' if new_late > 0 else 'ontime'})",
            })
            if not dry_run:
                s["late_mins"] = new_late

    backup_key = None
    if not dry_run:
        # Snapshot the ORIGINAL streams before overwriting, so we can roll back.
        backup_key = f"streams:backup:{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
        r.set(backup_key, raw if raw else json.dumps([]))

        r.set("streams", json.dumps(streams))
        r.set("migration:late_cutoff_2pm", pt_today())

    return {
        "ok": True,
        "dry_run": dry_run,
        "from_date": from_date,
        "backup_key": backup_key,  # null on dry runs; the Redis key holding the pre-run snapshot
        "total_streams": len(streams),
        "changed": len(changes),
        "changes": changes,
    }


# ── REPAIR: split-schedule recompute (no flag, idempotent) ───────────────
def _calc_late_mins_old5pm(start_hhmm: str) -> int:
    """Old schedule: 5:00 PM PT + same 20m grace = late after 5:20 PM."""
    h, m = map(int, start_hhmm.split(":"))
    actual_mins = h * 60 + m
    scheduled_mins = 17 * 60  # 5:00 PM
    return max(0, actual_mins - (scheduled_mins + LATE_GRACE_MINS))


@app.post("/api/admin/repair-late")
async def repair_late(dry_run: bool = False, new_from_date: str = "2026-05-20"):
    """
    One-shot repair that recomputes EVERY stream's late_mins from its recorded
    start time, using a split schedule:
      - date >= new_from_date  -> new 1:40 PM cutoff (late after 2:00 PM)
      - date <  new_from_date  -> old 5:00 PM cutoff (late after 5:20 PM)

    Recomputes from start times, so it corrects records a previous run mutated.
    Ignores the migration flag and writes a backup before committing.

      preview:  POST /api/admin/repair-late?dry_run=true
      commit:   POST /api/admin/repair-late
      other date: ...?dry_run=true&new_from_date=2026-05-18
    """
    r = get_redis()
    raw = r.get("streams")
    streams = json.loads(raw) if raw else []

    changes = []
    for s in streams:
        hhmm = s.get("startTime")
        if not hhmm and s.get("started_at"):
            dt = datetime.fromisoformat(s["started_at"].replace("Z", "+00:00"))
            hhmm = pt_time_str(dt)
        if not hhmm:
            continue

        date = s.get("date", "")
        if date >= new_from_date:
            new_late = calc_late_mins(hhmm)            # new 1:40 PM rule
            rule = "1:40pm"
        else:
            new_late = _calc_late_mins_old5pm(hhmm)    # old 5:00 PM rule
            rule = "5pm"

        old_late = s.get("late_mins", 0)
        if old_late != new_late:
            changes.append({
                "date": date,
                "startTime": hhmm,
                "rule": rule,
                "old": f"{old_late}m ({'late' if old_late > 0 else 'ontime'})",
                "new": f"{new_late}m ({'late' if new_late > 0 else 'ontime'})",
            })
            if not dry_run:
                s["late_mins"] = new_late

    backup_key = None
    if not dry_run:
        backup_key = f"streams:backup:{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}"
        r.set(backup_key, raw if raw else json.dumps([]))
        r.set("streams", json.dumps(streams))

    return {
        "ok": True,
        "dry_run": dry_run,
        "new_from_date": new_from_date,
        "backup_key": backup_key,
        "total_streams": len(streams),
        "changed": len(changes),
        "changes": changes,
    }
