import os
import json
import httpx
from datetime import datetime, timezone, timedelta
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from upstash_redis import Redis

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

SCHEDULED_HOUR_PST = 17  # 5:00 PM PST
LATE_GRACE_MINS    = 2   # 2 min grace period before counted as late

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
def pst_now() -> datetime:
    return datetime.now(timezone.utc) - timedelta(hours=8)

def pst_today() -> str:
    return pst_now().strftime("%Y-%m-%d")

def pst_time_str(dt: datetime) -> str:
    """Convert UTC datetime to PST HH:MM string."""
    pst = dt - timedelta(hours=8)
    return pst.strftime("%H:%M")

def calc_late_mins(start_hhmm: str) -> int:
    h, m = map(int, start_hhmm.split(":"))
    actual_mins = h * 60 + m
    scheduled_mins = SCHEDULED_HOUR_PST * 60
    return max(0, actual_mins - scheduled_mins)

# ── ROUTES ───────────────────────────────────────────────

@app.get("/api/status")
async def get_status():
    """
    Poll Twitch. Auto-detect going live and going offline.
    When going live: record stream start in Redis.
    When going offline: calculate duration, save completed stream.
    """
    if not TWITCH_CLIENT_ID or not TWITCH_CLIENT_SECRET:
        return {"live": False, "error": "Twitch not configured", "streams": [], "votes": {}, "length_votes": {}}

    r = get_redis()

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
            started_pst = pst_time_str(started_at_utc)

            # Check if we already know about this stream session
            cached_raw = r.get("current_stream")
            cached = json.loads(cached_raw) if cached_raw else None

            if not cached or cached.get("started_at") != stream["started_at"]:
                # New stream detected — record it
                today = pst_today()
                late_mins = calc_late_mins(started_pst)
                new_session = {
                    "started_at": stream["started_at"],
                    "started_pst": started_pst,
                    "date": today,
                    "late_mins": late_mins,
                }
                r.set("current_stream", json.dumps(new_session))

            return {
                "live": True,
                "started_at": stream["started_at"],
                "started_pst": started_pst,
                "viewer_count": stream["viewer_count"],
                "title": stream.get("title", ""),
                **_get_community_data(r),
            }

        else:
            # ── HE'S OFFLINE ─────────────────────────────
            cached_raw = r.get("current_stream")
            if cached_raw:
                # Stream just ended — calculate duration and save
                cached = json.loads(cached_raw)
                started_at_utc = datetime.fromisoformat(cached["started_at"].replace("Z", "+00:00"))
                ended_at_utc = datetime.now(timezone.utc)
                duration_hours = round((ended_at_utc - started_at_utc).total_seconds() / 3600, 2)

                # Only save if stream was at least 10 minutes (avoid false positives)
                if duration_hours >= (10 / 60):
                    _save_completed_stream(r, cached, duration_hours)

                # Clear the active session
                r.delete("current_stream")

            return {
                "live": False,
                **_get_community_data(r),
            }

    except Exception as e:
        return {"live": False, "error": str(e), **_get_community_data(r)}


def _save_completed_stream(r, session: dict, duration_hours: float):
    """Append a completed stream to the history list."""
    raw = r.get("streams")
    streams = json.loads(raw) if raw else []

    # Don't double-save the same session
    for s in streams:
        if s.get("started_at") == session["started_at"]:
            return

    streams.append({
        "date": session["date"],
        "startTime": session["started_pst"],
        "started_at": session["started_at"],
        "late_mins": session["late_mins"],
        "duration": duration_hours,
    })

    r.set("streams", json.dumps(streams))


def _get_community_data(r) -> dict:
    today = pst_today()
    vraw  = r.get(f"votes:{today}")
    lvraw = r.get(f"length_votes:{today}")
    sraw  = r.get("streams")
    return {
        "votes":        json.loads(vraw)  if vraw  else {"ontime": 0, "late": 0},
        "length_votes": json.loads(lvraw) if lvraw else {k: 0 for k in ["under1","1to2","2to3","3to4","over4","ragequit"]},
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
    today = pst_today()
    vraw  = r.get(f"votes:{today}")
    lvraw = r.get(f"length_votes:{today}")
    return {
        "votes":        json.loads(vraw)  if vraw  else {"ontime": 0, "late": 0},
        "length_votes": json.loads(lvraw) if lvraw else {k: 0 for k in ["under1","1to2","2to3","3to4","over4","ragequit"]},
        "date": today,
    }


class VoteBody(BaseModel):
    type: str  # "ontime" | "late"

@app.post("/api/votes")
async def cast_vote(body: VoteBody):
    if body.type not in ("ontime", "late"):
        raise HTTPException(status_code=400, detail="type must be 'ontime' or 'late'")
    r = get_redis()
    today = pst_today()
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
    valid = {"under1", "1to2", "2to3", "3to4", "over4", "ragequit"}
    if body.bucket not in valid:
        raise HTTPException(status_code=400, detail="Invalid bucket")
    r = get_redis()
    today = pst_today()
    key = f"length_votes:{today}"
    raw = r.get(key)
    votes = json.loads(raw) if raw else {k: 0 for k in valid}
    votes[body.bucket] = votes.get(body.bucket, 0) + 1
    r.set(key, json.dumps(votes))
    r.expire(key, 60 * 60 * 48)
    return {"ok": True, "length_votes": votes}
