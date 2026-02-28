# licky_T Trust Meter

Fully automatic community trust tracker for licky_T's stream.
No admin panel. No manual input. Everything is tracked via Twitch API.

## How It Works

1. Backend polls Twitch every time the frontend calls `/api/status` (every 60s)
2. When licky_T goes live → start time is cached in Redis, lateness calculated automatically
3. When licky_T goes offline → duration calculated from start → finish, stream saved to history
4. Community votes reset daily at midnight PST (enforced via dated Redis keys + localStorage)
5. Trust meter stacks forever across all streams

---

## Project Structure

```
lickyt/
├── api/
│   └── index.py          ← FastAPI backend (Twitch + Redis)
├── frontend/
│   └── index.html        ← Frontend (no keys, calls /api/*)
├── vercel.json           ← Routes /api/* to Python, everything else to frontend
└── requirements.txt
```

---

## Deploy to Vercel

### 1. Push to GitHub
Create a new repo and push this entire folder.

### 2. Import to Vercel
- Go to https://vercel.com → New Project → Import repo
- Framework preset: **Other**
- Root directory: `/`
- Hit Deploy (first deploy may fail — that's fine, env vars come next)

### 3. Add Vercel KV (Redis)
- Vercel project dashboard → **Storage** tab → Create Database → **KV**
- Name it anything (e.g. `lickyt-kv`) → Connect to project
- Vercel automatically adds `KV_REST_API_URL` and `KV_REST_API_TOKEN` to your env vars

### 4. Add your env vars
Vercel project → **Settings** → **Environment Variables**:

| Variable               | Value                                      |
|------------------------|--------------------------------------------|
| `TWITCH_CLIENT_ID`     | From dev.twitch.tv (your app's Client ID)  |
| `TWITCH_CLIENT_SECRET` | From dev.twitch.tv (your app's Secret)     |
| `STREAMER_LOGIN`       | licky_T's Twitch username (e.g. `licky_t`) |

### 5. Redeploy
Vercel dashboard → Deployments → Redeploy latest. Done.

---

## Getting Twitch Credentials (free)

1. Go to https://dev.twitch.tv/console
2. **Register Your Application**
3. Name: anything (e.g. `lickyt-monitor`)
4. OAuth Redirect URLs: `http://localhost` (required field but never used)
5. Category: **Website Integration**
6. Submit → copy **Client ID** → click **New Secret**

The backend auto-refreshes the Twitch token. You never touch it again.

---

## What Gets Tracked Automatically

| Event              | How                                                    |
|--------------------|--------------------------------------------------------|
| Stream start time  | `started_at` from Twitch API                          |
| Lateness (mins)    | Compared against scheduled 5pm PST                    |
| Stream duration    | Detected when stream goes offline, calculated from gap |
| Community votes    | Stored in Redis, keyed by PST date (auto-expire 48h)  |
| Trust score        | Calculated from full stream history on every load      |

## API Endpoints

| Method | Path              | Description                              |
|--------|-------------------|------------------------------------------|
| GET    | `/api/status`     | Poll Twitch + return all site data       |
| GET    | `/api/streams`    | All logged stream history                |
| GET    | `/api/votes`      | Today's community votes                  |
| POST   | `/api/votes`      | Cast on-time/late vote `{type}`          |
| POST   | `/api/votes/length` | Cast duration vote `{bucket}`          |
