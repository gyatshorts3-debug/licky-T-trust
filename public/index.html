<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>licky_T Trust Meter</title>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Share+Tech+Mono&family=Rajdhani:wght@400;600;700&display=swap" rel="stylesheet">
<style>
  :root {
    --red: #ff2233;
    --green: #00ff88;
    --yellow: #ffcc00;
    --dark: #080a0e;
    --card: #0d1117;
    --card2: #111820;
    --border: #1e2d3d;
    --text: #c9d8e8;
    --dim: #556677;
    --purple: #9d4edd;
  }

  * { margin:0; padding:0; box-sizing:border-box; }

  body {
    background: var(--dark);
    color: var(--text);
    font-family: 'Rajdhani', sans-serif;
    min-height: 100vh;
    overflow-x: hidden;
  }

  /* scanlines */
  body::before {
    content:''; position:fixed; inset:0;
    background: repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,0.03) 2px,rgba(0,0,0,0.03) 4px);
    pointer-events:none; z-index:9999;
  }

  /* grid bg */
  body::after {
    content:''; position:fixed; inset:0;
    background-image: linear-gradient(rgba(0,255,136,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(0,255,136,0.03) 1px,transparent 1px);
    background-size:40px 40px;
    pointer-events:none; z-index:0;
  }

  .container { max-width:960px; margin:0 auto; padding:0 20px; position:relative; z-index:1; }

  /* ── HEADER ── */
  header { text-align:center; padding:40px 0 20px; }
  .site-tag { font-family:'Share Tech Mono',monospace; font-size:11px; color:var(--green); letter-spacing:4px; margin-bottom:8px; opacity:.7; }
  h1 {
    font-family:'Bebas Neue',sans-serif;
    font-size:clamp(52px,10vw,96px);
    line-height:.9; letter-spacing:2px;
    background:linear-gradient(135deg,#fff 0%,var(--green) 50%,var(--red) 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
    filter:drop-shadow(0 0 30px rgba(0,255,136,.3));
  }
  .subtitle { font-family:'Share Tech Mono',monospace; font-size:13px; color:var(--dim); margin-top:10px; letter-spacing:2px; }
  .twitch-badge { display:inline-flex; align-items:center; gap:6px; font-family:'Share Tech Mono',monospace; font-size:10px; color:var(--dim); margin-top:10px; }
  .twitch-dot { width:7px; height:7px; border-radius:50%; background:var(--dim); flex-shrink:0; transition:all .3s; }
  .twitch-dot.ok  { background:var(--green); box-shadow:0 0 6px var(--green); }
  .twitch-dot.err { background:var(--red); }

  /* ── COUNTDOWN ── */
  .countdown-section { text-align:center; padding:30px 0; }
  .countdown-label { font-family:'Share Tech Mono',monospace; font-size:11px; letter-spacing:4px; color:var(--dim); margin-bottom:12px; }
  .countdown-display { font-family:'Bebas Neue',sans-serif; font-size:clamp(48px,12vw,100px); letter-spacing:4px; line-height:1; transition:color .5s; }
  .countdown-display.waiting { color:var(--yellow); text-shadow:0 0 40px rgba(255,204,0,.4); }
  .countdown-display.late    { color:var(--red);    text-shadow:0 0 40px rgba(255,34,51,.5); animation:shake .5s infinite; }
  .countdown-display.live    { color:var(--green);  text-shadow:0 0 40px rgba(0,255,136,.5); }
  @keyframes shake { 0%,100%{transform:translateX(0)} 25%{transform:translateX(-3px) rotate(-.5deg)} 75%{transform:translateX(3px) rotate(.5deg)} }

  .status-pill { display:inline-block; padding:6px 20px; border-radius:100px; font-family:'Share Tech Mono',monospace; font-size:12px; letter-spacing:2px; margin-top:12px; }
  .pill-waiting { background:rgba(255,204,0,.1);  border:1px solid var(--yellow); color:var(--yellow); }
  .pill-late    { background:rgba(255,34,51,.15);  border:1px solid var(--red);    color:var(--red);    animation:pulse-red 1s infinite; }
  .pill-live    { background:rgba(0,255,136,.15);  border:1px solid var(--green);  color:var(--green);  animation:pulse-green 1.5s infinite; }
  @keyframes pulse-red   { 0%,100%{box-shadow:0 0 0 0 rgba(255,34,51,.4)}  50%{box-shadow:0 0 0 8px rgba(255,34,51,0)} }
  @keyframes pulse-green { 0%,100%{box-shadow:0 0 0 0 rgba(0,255,136,.4)}  50%{box-shadow:0 0 0 8px rgba(0,255,136,0)} }

  /* live stream info strip */
  .live-strip {
    display:none; background:rgba(0,255,136,.06); border:1px solid rgba(0,255,136,.2);
    border-radius:10px; padding:12px 20px; margin-bottom:20px;
    font-family:'Share Tech Mono',monospace; font-size:11px; color:var(--green);
    letter-spacing:1px; text-align:center;
  }
  .live-strip.show { display:block; }

  /* ── SECTION LABEL ── */
  .section-label { font-family:'Bebas Neue',sans-serif; font-size:28px; letter-spacing:3px; color:var(--dim); margin-bottom:16px; border-bottom:1px solid var(--border); padding-bottom:8px; }

  /* ── TRUST METER ── */
  .meter-card { background:var(--card); border:1px solid var(--border); border-radius:16px; padding:30px; position:relative; overflow:hidden; }
  .meter-card::before { content:''; position:absolute; top:0;left:0;right:0; height:2px; background:linear-gradient(90deg,var(--red),var(--yellow),var(--green)); }
  .gauge-wrap { display:flex; justify-content:center; align-items:center; flex-direction:column; gap:8px; }
  .gauge-svg { width:min(340px,90vw); height:auto; filter:drop-shadow(0 0 20px rgba(0,0,0,.5)); }
  .trust-label-text { font-family:'Share Tech Mono',monospace; font-size:13px; letter-spacing:3px; text-align:center; margin-top:-4px; transition:color .5s; }
  .trust-stats-row { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-top:24px; }
  .trust-stat { background:var(--card2); border:1px solid var(--border); border-radius:10px; padding:14px; text-align:center; }
  .trust-stat .num { font-family:'Bebas Neue',sans-serif; font-size:32px; line-height:1; }
  .trust-stat .lbl { font-family:'Share Tech Mono',monospace; font-size:10px; color:var(--dim); letter-spacing:1px; margin-top:4px; }

  /* ── BETS ── */
  .bets-grid { display:grid; grid-template-columns:1fr 1fr; gap:16px; }
  @media(max-width:600px){.bets-grid{grid-template-columns:1fr}}

  .bet-card { background:var(--card); border:1px solid var(--border); border-radius:16px; padding:24px; position:relative; overflow:hidden; }
  .bet-title { font-family:'Bebas Neue',sans-serif; font-size:22px; letter-spacing:2px; margin-bottom:4px; }
  .bet-subtitle { font-family:'Share Tech Mono',monospace; font-size:10px; color:var(--green); letter-spacing:2px; margin-bottom:16px; }

  .vote-buttons { display:flex; gap:10px; margin-bottom:16px; }
  .vote-btn { flex:1; padding:14px 10px; border-radius:10px; border:2px solid transparent; cursor:pointer; font-family:'Bebas Neue',sans-serif; font-size:18px; letter-spacing:1px; transition:all .2s; background:var(--card2); color:var(--text); }
  .vote-btn:disabled { opacity:.4; cursor:not-allowed; }
  .vote-btn.green { border-color:rgba(0,255,136,.3); }
  .vote-btn.green:hover:not(:disabled),.vote-btn.green.active { background:rgba(0,255,136,.15); border-color:var(--green); color:var(--green); }
  .vote-btn.red { border-color:rgba(255,34,51,.3); }
  .vote-btn.red:hover:not(:disabled),.vote-btn.red.active { background:rgba(255,34,51,.15); border-color:var(--red); color:var(--red); }

  .vote-bar-labels { display:flex; justify-content:space-between; font-family:'Share Tech Mono',monospace; font-size:11px; color:var(--dim); margin-bottom:6px; }
  .vote-bar-track { height:10px; background:var(--card2); border-radius:100px; overflow:hidden; display:flex; }
  .vote-bar-green { height:100%; background:linear-gradient(90deg,#00cc66,var(--green)); transition:width .6s cubic-bezier(.4,0,.2,1); border-radius:100px 0 0 100px; }
  .vote-bar-red   { height:100%; background:linear-gradient(90deg,var(--red),#cc1122); transition:width .6s cubic-bezier(.4,0,.2,1); border-radius:0 100px 100px 0; }
  .vote-totals { display:flex; justify-content:space-between; margin-top:8px; font-family:'Share Tech Mono',monospace; font-size:12px; }
  .vtot-green{color:var(--green)} .vtot-red{color:var(--red)}

  /* ── LENGTH BET ── */
  .length-options { display:grid; grid-template-columns:repeat(3,1fr); gap:8px; margin-bottom:14px; }
  .len-btn { padding:10px 6px; border-radius:8px; border:1px solid var(--border); cursor:pointer; font-family:'Share Tech Mono',monospace; font-size:11px; text-align:center; background:var(--card2); color:var(--dim); transition:all .2s; }
  .len-btn:disabled { opacity:.4; cursor:not-allowed; }
  .len-btn:hover:not(:disabled) { border-color:var(--purple); color:var(--purple); }
  .len-btn.active { background:rgba(157,78,221,.15); border-color:var(--purple); color:var(--purple); }
  .len-bar-wrap { display:flex; flex-direction:column; gap:6px; }
  .len-bar-row { display:flex; align-items:center; gap:8px; font-family:'Share Tech Mono',monospace; font-size:10px; color:var(--dim); }
  .len-bar-row .lb-label { width:55px; text-align:right; flex-shrink:0; }
  .len-bar-track { flex:1; height:8px; background:var(--card2); border-radius:100px; overflow:hidden; }
  .len-bar-fill { height:100%; background:linear-gradient(90deg,var(--purple),#c77dff); border-radius:100px; transition:width .6s cubic-bezier(.4,0,.2,1); }
  .len-bar-row .lb-pct { width:32px; flex-shrink:0; }

  /* ── ENGINE ── */
  .engine-card { background:var(--card); border:1px solid var(--border); border-radius:16px; padding:24px; position:relative; overflow:hidden; }
  .engine-card::before { content:'ENGINE'; position:absolute; top:12px;right:16px; font-family:'Share Tech Mono',monospace; font-size:9px; letter-spacing:3px; color:rgba(157,78,221,.4); }
  .engine-header { display:flex; align-items:center; gap:10px; margin-bottom:20px; }
  .engine-dot { width:10px;height:10px;border-radius:50%;background:var(--purple);box-shadow:0 0 10px var(--purple);animation:pulse-purple 2s infinite; }
  @keyframes pulse-purple{0%,100%{opacity:1}50%{opacity:.4}}
  .engine-title { font-family:'Share Tech Mono',monospace; font-size:12px; letter-spacing:3px; color:var(--purple); }
  .engine-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:12px; }
  @media(max-width:500px){.engine-grid{grid-template-columns:1fr}}
  .engine-stat { background:var(--card2); border:1px solid rgba(157,78,221,.2); border-radius:10px; padding:14px; }
  .engine-stat .e-label { font-family:'Share Tech Mono',monospace; font-size:9px; color:rgba(157,78,221,.6); letter-spacing:2px; margin-bottom:6px; text-transform:uppercase; }
  .engine-stat .e-value { font-family:'Bebas Neue',sans-serif; font-size:26px; line-height:1; }
  .engine-stat .e-sub { font-family:'Share Tech Mono',monospace; font-size:10px; color:var(--dim); margin-top:4px; }
  .conf-bar-wrap{margin-top:8px}
  .conf-bar-track{height:6px;background:var(--card2);border-radius:100px;overflow:hidden;margin-top:4px}
  .conf-bar-fill{height:100%;border-radius:100px;transition:width .8s ease}

  /* ── SHAME ── */
  .shame-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:12px; }
  @media(max-width:500px){.shame-grid{grid-template-columns:1fr}}
  .shame-card { background:var(--card); border:1px solid var(--border); border-radius:12px; padding:20px; text-align:center; }
  .shame-num { font-family:'Bebas Neue',sans-serif; font-size:48px; line-height:1; }
  .shame-lbl { font-family:'Share Tech Mono',monospace; font-size:10px; letter-spacing:2px; color:var(--dim); margin-top:4px; }

  /* ── RECENT STREAMS ── */
  .stream-list { display:flex; flex-direction:column; gap:8px; }
  .stream-row { background:var(--card); border:1px solid var(--border); border-radius:10px; padding:14px 16px; display:flex; align-items:center; gap:16px; font-family:'Share Tech Mono',monospace; font-size:12px; flex-wrap:wrap; }
  .stream-badge { padding:4px 10px; border-radius:100px; font-size:10px; letter-spacing:1px; flex-shrink:0; }
  .badge-late   { background:rgba(255,34,51,.15);  border:1px solid var(--red);   color:var(--red); }
  .badge-ontime { background:rgba(0,255,136,.15);  border:1px solid var(--green); color:var(--green); }
  .stream-date  { color:var(--dim); flex:1; }
  .stream-info  { color:var(--text); }

  /* ── DAILY RESET NOTE ── */
  .reset-note { font-family:'Share Tech Mono',monospace; font-size:10px; color:var(--dim); text-align:center; padding:12px; letter-spacing:1px; }

  /* ── EMPTY ── */
  .empty-state { font-family:'Share Tech Mono',monospace; font-size:12px; color:var(--dim); text-align:center; padding:24px; }

  .gap    { margin-top:24px; }
  .gap-sm { margin-top:14px; }

  footer { text-align:center; padding:40px 0 30px; font-family:'Share Tech Mono',monospace; font-size:10px; color:var(--dim); letter-spacing:2px; }
</style>
</head>
<body>
<div class="container">

  <!-- HEADER -->
  <header>
    <div class="site-tag">// COMMUNITY TRUST MONITOR //</div>
    <h1>LICKY_T</h1>
    <div class="subtitle">SCHEDULED: 5:00 PM PST</div>
    <div class="twitch-badge">
      <div class="twitch-dot" id="twitchDot"></div>
      <span id="twitchStatus">connecting to twitch...</span>
    </div>
  </header>

  <!-- LIVE STRIP -->
  <div class="live-strip" id="liveStrip">
    🔴 LIVE NOW &nbsp;·&nbsp; <span id="liveTitle"></span> &nbsp;·&nbsp; <span id="liveViewers"></span> viewers
  </div>

  <!-- COUNTDOWN -->
  <div class="countdown-section">
    <div class="countdown-label" id="countdownLabel">TIME UNTIL STREAM</div>
    <div class="countdown-display waiting" id="countdownDisplay">--:--:--</div>
    <div><span class="status-pill pill-waiting" id="statusPill">⏳ WAITING</span></div>
  </div>

  <!-- TRUST METER -->
  <div class="section-label">TRUST METER</div>
  <div class="meter-card">
    <div class="gauge-wrap">
      <svg class="gauge-svg" viewBox="0 0 340 200" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="gaugeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%"   stop-color="#ff2233"/>
            <stop offset="40%"  stop-color="#ffcc00"/>
            <stop offset="100%" stop-color="#00ff88"/>
          </linearGradient>
          <filter id="glow">
            <feGaussianBlur stdDeviation="3" result="blur"/>
            <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
          </filter>
        </defs>
        <!-- track bg -->
        <path d="M 30 175 A 140 140 0 0 1 310 175" fill="none" stroke="#1e2d3d" stroke-width="18" stroke-linecap="round"/>
        <!-- color track dim -->
        <path d="M 30 175 A 140 140 0 0 1 310 175" fill="none" stroke="url(#gaugeGrad)" stroke-width="18" stroke-linecap="round" opacity=".3"/>
        <!-- active arc -->
        <path id="gaugeArc" d="M 30 175 A 140 140 0 0 1 310 175" fill="none" stroke="url(#gaugeGrad)" stroke-width="18" stroke-linecap="round"
          stroke-dasharray="439.8" stroke-dashoffset="439.8" style="transition:stroke-dashoffset 1.2s cubic-bezier(.4,0,.2,1)"/>
        <!-- ticks -->
        <g stroke="#1e2d3d" stroke-width="1.5">
          <line x1="170" y1="35" x2="170" y2="55" transform="rotate(-90 170 175)"/>
          <line x1="170" y1="35" x2="170" y2="45" transform="rotate(-67.5 170 175)"/>
          <line x1="170" y1="35" x2="170" y2="55" transform="rotate(-45 170 175)"/>
          <line x1="170" y1="35" x2="170" y2="45" transform="rotate(-22.5 170 175)"/>
          <line x1="170" y1="35" x2="170" y2="55" transform="rotate(0 170 175)"/>
          <line x1="170" y1="35" x2="170" y2="45" transform="rotate(22.5 170 175)"/>
          <line x1="170" y1="35" x2="170" y2="55" transform="rotate(45 170 175)"/>
          <line x1="170" y1="35" x2="170" y2="45" transform="rotate(67.5 170 175)"/>
          <line x1="170" y1="35" x2="170" y2="55" transform="rotate(90 170 175)"/>
        </g>
        <text x="24"  y="192" fill="#ff2233" font-family="Bebas Neue, sans-serif" font-size="12" text-anchor="middle">LIAR</text>
        <text x="316" y="192" fill="#00ff88" font-family="Bebas Neue, sans-serif" font-size="12" text-anchor="middle">SAINT</text>
        <text x="170" y="50"  fill="#ffcc00" font-family="Bebas Neue, sans-serif" font-size="11" text-anchor="middle">MEH</text>
        <!-- needle -->
        <g id="needleGroup" style="transform-origin:170px 175px;transition:transform 1.2s cubic-bezier(.4,0,.2,1);transform:rotate(-90deg)">
          <line x1="170" y1="175" x2="170" y2="50" stroke="white" stroke-width="3" stroke-linecap="round" filter="url(#glow)"/>
          <circle cx="170" cy="175" r="8" fill="#0d1117" stroke="white" stroke-width="2"/>
          <circle cx="170" cy="175" r="3" fill="white"/>
        </g>
        <text id="gaugeCenterScore" x="170" y="155" fill="white" font-family="Bebas Neue, sans-serif" font-size="36" text-anchor="middle">--</text>
        <text x="170" y="170" fill="#556677" font-family="Share Tech Mono, monospace" font-size="9" text-anchor="middle">/100</text>
      </svg>
      <div class="trust-label-text" id="trustLabelText" style="color:var(--yellow)">CALCULATING...</div>
    </div>
    <div class="trust-stats-row">
      <div class="trust-stat"><div class="num" id="stat-ontime" style="color:var(--green)">--</div><div class="lbl">ON TIME</div></div>
      <div class="trust-stat"><div class="num" id="stat-late"   style="color:var(--red)">--</div><div class="lbl">TIMES LATE</div></div>
      <div class="trust-stat"><div class="num" id="stat-avg"    style="color:var(--yellow)">--m</div><div class="lbl">AVG LATE</div></div>
    </div>
  </div>

  <!-- COMMUNITY BETS -->
  <div class="section-label gap">COMMUNITY BETS</div>
  <div class="bets-grid">

    <!-- On time or late -->
    <div class="bet-card">
      <div class="bet-title">🎰 ON TIME OR LATE?</div>
      <div class="bet-subtitle">↻ RESETS DAILY · VOTE ONCE PER DAY</div>
      <div class="vote-buttons">
        <button class="vote-btn green" id="btnOnTime" onclick="vote('ontime')">🟢 ON TIME<br><small style="font-size:12px;font-family:'Share Tech Mono'">(lol)</small></button>
        <button class="vote-btn red"   id="btnLate"   onclick="vote('late')">🔴 LATE<br><small style="font-size:12px;font-family:'Share Tech Mono'">(obviously)</small></button>
      </div>
      <div class="vote-bar-labels">
        <span style="color:var(--green)" id="pctOnTime">0%</span>
        <span style="color:var(--dim)"   id="totalVotes">0 votes</span>
        <span style="color:var(--red)"   id="pctLate">0%</span>
      </div>
      <div class="vote-bar-track">
        <div class="vote-bar-green" id="barOnTime" style="width:0%"></div>
        <div class="vote-bar-red"   id="barLate"   style="width:0%"></div>
      </div>
      <div class="vote-totals">
        <span class="vtot-green" id="numOnTime">0</span>
        <span class="vtot-red"   id="numLate">0</span>
      </div>
    </div>

    <!-- Stream length -->
    <div class="bet-card">
      <div class="bet-title">⏱️ HOW LONG WILL HE STREAM?</div>
      <div class="bet-subtitle">↻ RESETS DAILY · VOTE ONCE PER DAY</div>
      <div class="length-options">
        <button class="len-btn" data-key="under1"   onclick="voteLength(this,'under1')">Under 1hr</button>
        <button class="len-btn" data-key="1to2"     onclick="voteLength(this,'1to2')">1–2 hrs</button>
        <button class="len-btn" data-key="2to3"     onclick="voteLength(this,'2to3')">2–3 hrs</button>
        <button class="len-btn" data-key="3to4"     onclick="voteLength(this,'3to4')">3–4 hrs</button>
        <button class="len-btn" data-key="over4"    onclick="voteLength(this,'over4')">4+ hrs</button>
        <button class="len-btn" data-key="ragequit" onclick="voteLength(this,'ragequit')">💀 Rage quit</button>
      </div>
      <div class="len-bar-wrap" id="lenBars"></div>
    </div>
  </div>
  <div class="reset-note">Community votes reset every day at midnight PST. Trust meter stacks forever.</div>

  <!-- ENGINE PREDICTION -->
  <div class="section-label gap">PREDICTION ENGINE</div>
  <div class="engine-card">
    <div class="engine-header">
      <div class="engine-dot"></div>
      <div class="engine-title">DATA-DRIVEN PREDICTION // v1.0</div>
    </div>
    <div class="engine-grid">
      <div class="engine-stat">
        <div class="e-label">LATE PROBABILITY</div>
        <div class="e-value" id="eng-lateprob" style="color:var(--red)">--%</div>
        <div class="conf-bar-wrap"><div class="conf-bar-track"><div class="conf-bar-fill" id="eng-lateprob-bar" style="width:0%;background:var(--red)"></div></div></div>
        <div class="e-sub" id="eng-lateprob-sub">Awaiting stream data</div>
      </div>
      <div class="engine-stat">
        <div class="e-label">PREDICTED START TIME</div>
        <div class="e-value" id="eng-starttime" style="color:var(--yellow)">--:-- PM</div>
        <div class="e-sub" id="eng-starttime-sub">PST</div>
      </div>
      <div class="engine-stat">
        <div class="e-label">PREDICTED DURATION</div>
        <div class="e-value" id="eng-duration" style="color:var(--purple)">-- hrs</div>
        <div class="e-sub" id="eng-duration-sub">Based on stream history</div>
      </div>
      <div class="engine-stat">
        <div class="e-label">CONFIDENCE SCORE</div>
        <div class="e-value" id="eng-confidence" style="color:var(--green)">--%</div>
        <div class="conf-bar-wrap"><div class="conf-bar-track"><div class="conf-bar-fill" id="eng-conf-bar" style="width:0%;background:var(--green)"></div></div></div>
        <div class="e-sub" id="eng-conf-sub">More streams = more accuracy</div>
      </div>
    </div>
  </div>

  <!-- HALL OF SHAME -->
  <div class="section-label gap">HALL OF SHAME</div>
  <div class="shame-grid">
    <div class="shame-card"><div class="shame-num" id="shame-total"     style="color:var(--text)">--</div><div class="shame-lbl">TOTAL STREAMS TRACKED</div></div>
    <div class="shame-card"><div class="shame-num" id="shame-latecount" style="color:var(--red)">--</div><div class="shame-lbl">STREAMS WHERE HE WAS LATE</div></div>
    <div class="shame-card"><div class="shame-num" id="shame-record"    style="color:var(--red)">--m</div><div class="shame-lbl">RECORD LATENESS 💀</div></div>
    <div class="shame-card"><div class="shame-num" id="shame-longest"   style="color:var(--green)">--h</div><div class="shame-lbl">LONGEST STREAM</div></div>
  </div>

  <!-- RECENT STREAMS -->
  <div class="section-label gap">RECENT STREAMS</div>
  <div class="stream-list" id="recentStreams">
    <div class="empty-state">No streams recorded yet — site will auto-log once licky_T goes live.</div>
  </div>

  <footer>
    LICKY_T TRUST MONITOR // AUTO-TRACKED VIA TWITCH API // COMMUNITY FAN SITE<br>
  </footer>
</div>

<script>
// ── CONFIG ────────────────────────────────────────────────
const SCHEDULED_MIN  = 17 * 60; // 5pm PST
const LENGTH_KEYS    = ['under1','1to2','2to3','3to4','over4','ragequit'];
const LENGTH_LABELS  = { under1:'< 1hr','1to2':'1–2h','2to3':'2–3h','3to4':'3–4h',over4:'4+h',ragequit:'💀 Quit' };

// ── STATE ─────────────────────────────────────────────────
let streams      = [];
let votes        = { ontime:0, late:0 };
let lengthVotes  = {};
let liveData     = null;
let userVoted    = null;
let userLenVoted = null;

// ── DAILY RESET — votes stored with today's date key ──────
function todayKey() {
  const pt = getPT();
  const y = pt.getFullYear();
  const m = String(pt.getMonth() + 1).padStart(2, '0');
  const d = String(pt.getDate()).padStart(2, '0');
  return `${y}-${m}-${d}`;
}

function getPST() { // keep name if you want, but it's PT
  return getPT();
}

function loadLocalVoteState() {
  const today = todayKey();
  userVoted    = localStorage.getItem('vote_'    + today) || null;
  userLenVoted = localStorage.getItem('voteLen_' + today) || null;
  // Clean up old keys
  for (const k of Object.keys(localStorage)) {
    if ((k.startsWith('vote_') || k.startsWith('voteLen_')) && !k.endsWith(today)) {
      localStorage.removeItem(k);
    }
  }
}

function saveLocalVote(type)    { localStorage.setItem('vote_'    + todayKey(), type); }
function saveLocalLenVote(type) { localStorage.setItem('voteLen_' + todayKey(), type); }

// ── HELPERS ───────────────────────────────────────────────

function fmtTime(h, m) {
  const ap = h >= 12 ? 'PM' : 'AM';
  return `${h % 12 || 12}:${String(m).padStart(2,'0')} ${ap}`;
}

// ── API CALLS ─────────────────────────────────────────────
async function apiGet(path) {
  const r = await fetch(path);
  return r.json();
}
async function apiPost(path, body) {
  const r = await fetch(path, {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify(body)
  });
  return r.json();
}

// ── TWITCH POLL ───────────────────────────────────────────
async function pollStatus() {
  try {
    const data = await apiGet('/api/status');

    if (data.error && data.error.includes('not configured')) {
      setTwitchBadge('err', 'twitch api not configured in vercel env vars');
    } else {
      setTwitchBadge('ok', data.live
        ? `licky_T is LIVE · ${data.viewer_count} viewers`
        : 'connected · licky_T is offline');
    }

    liveData = data.live ? data : null;

    // Live strip
    const strip = document.getElementById('liveStrip');
    if (data.live) {
      strip.classList.add('show');
      document.getElementById('liveTitle').textContent   = data.title || '';
      document.getElementById('liveViewers').textContent = data.viewer_count;
    } else {
      strip.classList.remove('show');
    }

    // Merge in community data from status response
    if (data.votes)        { votes       = data.votes; }
    if (data.length_votes) { lengthVotes = data.length_votes; }
    if (data.streams)      { streams     = data.streams; }

    renderAll();
  } catch(e) {
    setTwitchBadge('err', 'connection error');
  }
}

function setTwitchBadge(cls, msg) {
  document.getElementById('twitchDot').className    = 'twitch-dot ' + cls;
  document.getElementById('twitchStatus').textContent = msg;
}

function getScheduledStreamTimePT(nowPT = getPT()) {
  // returns a Date object for today's scheduled stream time in PT (5:00 PM)
  const scheduled = new Date(nowPT);
  scheduled.setHours(17, 0, 0, 0); // 5:00 PM PT
  return scheduled;
}

// ── COUNTDOWN ─────────────────────────────────────────────
function updateCountdown() {
  const now = getPST();

  const el   = document.getElementById('countdownDisplay');
  const lbl  = document.getElementById('countdownLabel');
  const pill = document.getElementById('statusPill');
  
  const scheduled = getScheduledStreamTimePT(now);
  const diff = scheduled - now; // milliseconds
  
  // Saturday = no stream day
  if (isNoStreamDayPT(now) && !liveData) {
    el.className   = 'countdown-display waiting';
    el.textContent = `--:--:--`;
    lbl.textContent  = '🚫 NO STREAM SCHEDULED (SATURDAY)';
    pill.className   = 'status-pill pill-waiting';
    pill.textContent = 'OFF DAY';
    return;
  }
  
  if (diff > 0) {
    const h=Math.floor(diff/3600000),
          m=Math.floor((diff%3600000)/60000),
          s=Math.floor((diff%60000)/1000);
  
    el.className   = 'countdown-display waiting';
    el.textContent = `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;
    lbl.textContent  = 'TIME UNTIL SCHEDULED STREAM';
    pill.className   = 'status-pill pill-waiting';
    pill.textContent = '⏳ NOT LIVE YET';
  } else {
    const late = Math.abs(diff);
  
    const h=Math.floor(late/3600000),
          m=Math.floor((late%3600000)/60000),
          s=Math.floor((late%60000)/1000);
  
    el.className   = 'countdown-display late';
    el.textContent = `${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}:${String(s).padStart(2,'0')}`;
    lbl.textContent  = '⚠️ HE\'S LATE — OVERDUE BY';
    pill.className   = 'status-pill pill-late';
    pill.textContent = '🔴 NOT LIVE — RUNNING LATE';
  }
}

// ── TRUST SCORE ───────────────────────────────────────────
function clamp(n, a, b){ return Math.max(a, Math.min(b, n)); }

function hardScoreFromLate(lateMins) {
  // 0–2 minutes = perfect
  if (lateMins <= 2) return 100;

  // Simple linear decay after grace:
  // 10 mins late -> 84
  // 30 mins late -> 44
  // 52+ mins late -> 0
  const score = 100 - (lateMins - 2) * 2;
  return clamp(Math.round(score), 0, 100);
}

function crowdScoreFromVotes(votesObj) {
  const on = votesObj?.ontime || 0;
  const lt = votesObj?.late   || 0;
  const total = on + lt;
  if (!total) return 50; // only neutral when 0 votes
  return Math.round((on / total) * 100);
}

function isSameDayPST(dateISO, pstDateKey) {
  return dateISO === pstDateKey;
}

function calcLateMinsFromStartedAtUTC(startedAtISO) {
  // startedAtISO is UTC (e.g. "2026-02-27T01:23:45Z")
  // Convert to PST by subtracting 8 hours (your whole site does this)
  const d = new Date(startedAtISO);
  const pst = new Date(d.getTime() - 8 * 3600000);
  const h = pst.getUTCHours();
  const m = pst.getUTCMinutes();
  const actualMins = h * 60 + m;
  return Math.max(0, actualMins - SCHEDULED_MIN);
}

function calcLateMinsRightNow() {
  // If not live yet and it's past schedule, count how late he is so far.
  const now = getPST(); // already PST-shifted Date
  const h = now.getUTCHours();
  const m = now.getUTCMinutes();
  const actualMins = h * 60 + m;
  return Math.max(0, actualMins - SCHEDULED_MIN);
}

function streamsAlreadyContainToday(streamsArr) {
  const today = todayKey();
  return streamsArr.some(s => s.date === today);
}

function buildTodaySyntheticStream() {
  const today = todayKey();

  // If he's live, use actual start time from Twitch.
  // If not live, use "lateness so far" once past scheduled time.
  let late_mins = 0;
  let startTime = "17:00"; // fallback

  if (liveData?.started_at) {
    late_mins = calcLateMinsFromStartedAtUTC(liveData.started_at);

    // also build startTime "HH:MM" in PST for display / consistency
    const d = new Date(liveData.started_at);
    const pst = new Date(d.getTime() - 8 * 3600000);
    const hh = String(pst.getUTCHours()).padStart(2, "0");
    const mm = String(pst.getUTCMinutes()).padStart(2, "0");
    startTime = `${hh}:${mm}`;
  } else {
    // Not live yet:
    late_mins = calcLateMinsRightNow();
    // If not yet scheduled time, late_mins = 0 which is fine.
  }

  return {
    date: today,
    startTime,
    late_mins,
    // IMPORTANT: use LIVE current votes (not persisted snapshot)
    votes: { ...votes },

    // Optional: keep length votes live too if you ever use them later
    length_votes: { ...lengthVotes },

    // Mark as synthetic so you can ignore elsewhere if needed
    _synthetic: true,
  };
}


function getPT() {
  // Robust PT wall-clock date (handles DST correctly)
  return new Date(new Date().toLocaleString('en-US', { timeZone: 'America/Los_Angeles' }));
}

function isNoStreamDayPT(d = getPT()) {
  // Saturday = 6
  return d.getDay() === 6;
}
  
function calcTrust(streams) {
  const HARD_WEIGHT  = 1;
  const CROWD_WEIGHT = 4; // 4x influence vs hard score
  if (!streams.length) return { score:50, ontimeCount:0, lateCount:0, avgLate:0 };

  let on=0, late=0, totalLate=0;
  let blendedSum = 0;
  

  streams.forEach(s => {
    const late_mins = s.late_mins ?? (() => {
      const [h,m] = s.startTime.split(':').map(Number);
      return Math.max(0, h*60+m - SCHEDULED_MIN);
    })();

    if (late_mins <= 2) on++;
    else { late++; totalLate += late_mins; }

    const hard  = hardScoreFromLate(late_mins);

    // Use persisted votes for that stream-day if present.
    // Fallback to null => neutral 50
    const crowd = crowdScoreFromVotes(s.votes || null);

    // TRUE equal influence:
    const denom = HARD_WEIGHT + CROWD_WEIGHT;
    const scoreThis = Math.round((HARD_WEIGHT * hard + CROWD_WEIGHT * crowd) / denom);
    blendedSum += scoreThis;
    
  });

  const avgLate = late ? Math.round(totalLate / late) : 0;
  const score   = Math.round(blendedSum / streams.length);

  return { score, ontimeCount:on, lateCount:late, avgLate };
}
function renderTrust(t) {
  const { score, ontimeCount, lateCount, avgLate } = t;
  document.getElementById('needleGroup').style.transform = `rotate(${(score/100)*180-90}deg)`;
  document.getElementById('gaugeArc').style.strokeDashoffset = 439.8 - (score/100)*439.8;
  document.getElementById('gaugeCenterScore').textContent = score;

  let color, label;
  if      (score < 20) { color='#ff2233'; label='CERTIFIED LIAR'; }
  else if (score < 40) { color='#ff6633'; label='CHRONICALLY LATE'; }
  else if (score < 60) { color='#ffcc00'; label='HIT OR MISS'; }
  else if (score < 80) { color='#88ee44'; label='SOMEWHAT RELIABLE'; }
  else                  { color='#00ff88'; label='SURPRISINGLY TRUSTWORTHY'; }

  document.getElementById('trustLabelText').style.color   = color;
  document.getElementById('trustLabelText').textContent   = label;
  document.getElementById('gaugeCenterScore').setAttribute('fill', color);
  document.getElementById('stat-ontime').textContent = ontimeCount;
  document.getElementById('stat-late').textContent   = lateCount;
  document.getElementById('stat-avg').textContent    = avgLate + 'm';
}

// ── ENGINE PREDICTION ─────────────────────────────────────
function renderEngine(streams) {
  if (!streams.length) return;
  let lateMinsArr=[], durs=[], lateCount=0;
  streams.forEach(s => {
    const lm = s.late_mins ?? 0;
    lateMinsArr.push(lm);
    if (lm > 2) lateCount++;
    if (s.duration) durs.push(parseFloat(s.duration));
  });

  const lateProb   = Math.round((lateCount / streams.length) * 100);
  const avgLate    = Math.round(lateMinsArr.reduce((a,b)=>a+b,0) / lateMinsArr.length);
  const predMin    = SCHEDULED_MIN + avgLate;
  const avgDur     = durs.length ? durs.reduce((a,b)=>a+b,0) / durs.length : null;
  const confidence = Math.min(95, 40 + streams.length * 7);

  document.getElementById('eng-lateprob').textContent     = lateProb + '%';
  document.getElementById('eng-lateprob-bar').style.width = lateProb + '%';
  document.getElementById('eng-lateprob-sub').textContent = `${lateCount} of ${streams.length} streams late`;
  document.getElementById('eng-starttime').textContent    = fmtTime(Math.floor(predMin/60), predMin%60);
  document.getElementById('eng-starttime-sub').textContent= `PST · avg ${avgLate}min delay`;

  if (avgDur) {
    const dh=Math.floor(avgDur), dm=Math.round((avgDur-dh)*60);
    document.getElementById('eng-duration').textContent     = `${dh}h ${dm}m`;
    document.getElementById('eng-duration-sub').textContent = `avg over ${durs.length} streams`;
  } else {
    document.getElementById('eng-duration').textContent     = 'Building...';
    document.getElementById('eng-duration-sub').textContent = 'Need more stream data';
  }

  document.getElementById('eng-confidence').textContent    = Math.round(confidence) + '%';
  document.getElementById('eng-conf-bar').style.width      = confidence + '%';
  document.getElementById('eng-conf-sub').textContent      = `Based on ${streams.length} streams`;
}

// ── SHAME + RECENT ────────────────────────────────────────
function renderShame(streams) {
  let late=0, maxLate=0, maxDur=0;
  streams.forEach(s => {
    const lm = s.late_mins ?? 0;
    if (lm > 2) { late++; if(lm>maxLate) maxLate=lm; }
    if (s.duration && parseFloat(s.duration) > maxDur) maxDur = parseFloat(s.duration);
  });
  document.getElementById('shame-total').textContent     = streams.length || '--';
  document.getElementById('shame-latecount').textContent = streams.length ? late : '--';
  document.getElementById('shame-record').textContent    = maxLate ? maxLate+'m' : '--m';
  document.getElementById('shame-longest').textContent   = maxDur  ? maxDur+'h'  : '--h';
}

function renderRecent(streams) {
  const el = document.getElementById('recentStreams');
  if (!streams.length) {
    el.innerHTML = '<div class="empty-state">No streams recorded yet — site auto-logs once licky_T goes live.</div>';
    return;
  }
  el.innerHTML = [...streams].reverse().slice(0, 8).map(s => {
    const lm   = s.late_mins ?? 0;
    const isLate = lm > 2;
    const badge  = isLate
      ? `<span class="stream-badge badge-late">LATE +${lm}m</span>`
      : `<span class="stream-badge badge-ontime">ON TIME</span>`;
    const dur = s.duration ? ` · ${parseFloat(s.duration).toFixed(1)}h stream` : '';
    const [h,m] = s.startTime.split(':').map(Number);
    return `<div class="stream-row">${badge}<span class="stream-date">${s.date}</span><span class="stream-info">Started ${fmtTime(h,m)} PST${dur}</span></div>`;
  }).join('');
}

// ── VOTES ─────────────────────────────────────────────────
function renderVotes() {
  const total = votes.ontime + votes.late;
  const pOn   = total ? Math.round((votes.ontime/total)*100) : 0;
  const pLate = total ? 100 - pOn : 0;

  document.getElementById('pctOnTime').textContent  = pOn + '%';
  document.getElementById('pctLate').textContent    = pLate + '%';
  document.getElementById('totalVotes').textContent = total + ' votes';
  document.getElementById('numOnTime').textContent  = votes.ontime;
  document.getElementById('numLate').textContent    = votes.late;
  document.getElementById('barOnTime').style.width  = pOn + '%';
  document.getElementById('barLate').style.width    = pLate + '%';

  const hasVoted = !!userVoted;
  document.getElementById('btnOnTime').classList.toggle('active', userVoted === 'ontime');
  document.getElementById('btnLate').classList.toggle('active',   userVoted === 'late');
  document.getElementById('btnOnTime').disabled = hasVoted;
  document.getElementById('btnLate').disabled   = hasVoted;
}

function renderLength() {
  const total = LENGTH_KEYS.reduce((a,k) => a + (lengthVotes[k]||0), 0);
  document.getElementById('lenBars').innerHTML = LENGTH_KEYS.map(k => {
    const pct = total ? Math.round(((lengthVotes[k]||0)/total)*100) : 0;
    return `<div class="len-bar-row">
      <span class="lb-label">${LENGTH_LABELS[k]}</span>
      <div class="len-bar-track"><div class="len-bar-fill" style="width:${pct}%"></div></div>
      <span class="lb-pct" style="color:var(--purple)">${pct}%</span>
    </div>`;
  }).join('');

  const hasVoted = !!userLenVoted;
  document.querySelectorAll('.len-btn').forEach(b => {
    b.classList.toggle('active', b.dataset.key === userLenVoted);
    b.disabled = hasVoted;
  });
}

async function vote(type) {
  if (userVoted) return;
  userVoted = type;
  saveLocalVote(type);
  renderVotes();
  try {
    const data = await apiPost('/api/votes', { type });
    if (data.votes) { votes = data.votes; renderVotes(); }
  } catch {}
}

async function voteLength(btn, key) {
  if (userLenVoted) return;
  userLenVoted = key;
  saveLocalLenVote(key);
  renderLength();
  try {
    const data = await apiPost('/api/votes/length', { bucket: key });
    if (data.length_votes) { lengthVotes = data.length_votes; renderLength(); }
  } catch {}
}

// ── RENDER ALL ────────────────────────────────────────────
function renderAll() {
  let trustStreams = streams;

  const totalVotesNow = (votes.ontime || 0) + (votes.late || 0);
  const nowLate = calcLateMinsRightNow() > 0;

  // Inject a "today" record if:
  // - we don't already have today in history, AND
  // - he's live OR he's late OR people have voted
  if (!streamsAlreadyContainToday(streams) && (liveData || nowLate || totalVotesNow > 0)) {
    const todaySynthetic = buildTodaySyntheticStream();

    // If it's a no-stream day and he's not live, don't punish lateness logic
    // (still allow votes to affect trust)
    if (isNoStreamDayPT() && !liveData) {
      todaySynthetic.late_mins = 0;
    }

    trustStreams = [...streams, todaySynthetic];
  }

  const trust = calcTrust(trustStreams);
  renderTrust(trust);

  renderEngine(streams);
  renderShame(streams);
  renderRecent(streams);

  renderVotes();
  renderLength();
}
// ── INIT ──────────────────────────────────────────────────
async function init() {
  loadLocalVoteState();
  updateCountdown();
  setInterval(updateCountdown, 1000);

  await pollStatus();             // first poll — gets everything
  setInterval(pollStatus, 60000); // re-poll every 60s
}

init();
</script>
</body>
</html>
