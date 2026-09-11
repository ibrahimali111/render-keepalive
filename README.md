<div align="right">
  <em>💡 100% original ideas &nbsp;•&nbsp; 🤖 100% vibe coding &nbsp;•&nbsp; 🚫 0% nudes</em>
  &nbsp;&nbsp;
  <a href="https://github.com/ibrahimali111" title="100% Original Ideas • 100% Vibe Coding • 0% Nudes">
    <img src="https://raw.githubusercontent.com/ibrahimali111/fair-hearts/main/assets/vibe-coded-badge.svg" height="28" alt="Vibe Coded" />
  </a>
</div>

# 🚀 Render & Cloud Keep-Alive Heartbeat

<p align="center">
  <a href="https://github.com/ibrahimali111/render-keepalive/actions/workflows/keepalive.yml">
    <img src="https://github.com/ibrahimali111/render-keepalive/actions/workflows/keepalive.yml/badge.svg" alt="Keep-Alive Cron Status" />
  </a>
  <a href="https://github.com/ibrahimali111/render-keepalive/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License: MIT" />
  </a>
  <img src="https://img.shields.io/badge/python-3.8+-3776AB?logo=python&logoColor=white" alt="Python 3.8+" />
  <img src="https://img.shields.io/badge/cost-$0%20free-brightgreen" alt="100% Free" />
  <img src="https://img.shields.io/badge/docker-ready-2496ED?logo=docker&logoColor=white" alt="Docker Ready" />
</p>

A zero-dependency, automated 24/7 keep-alive heartbeat and uptime monitoring bot designed to keep free-tier cloud applications awake and avoid painful 50+ second cold boots.

Works seamlessly with **Render.com**, **Koyeb**, **Hugging Face Spaces**, **Glitch**, and any public HTTP/HTTPS endpoint.

---

## ⚡ The Problem It Solves

Free tiers on modern cloud platforms put your applications to sleep after **15 minutes of inactivity**:
- When a user visits your app, they experience a frustrating **50–90 second delay** while the container cold-boots.
- External webhooks, bots, and background tasks fail to respond in time.

**`render-keepalive`** pings your endpoints on a scheduled cycle (every 12 minutes) directly via **GitHub Actions Cron** for **100% free**, ensuring your free cloud servers stay awake around the clock!

---

## 🌟 Quick Setup (Fork & Run in 60 Seconds)

You do **not** need a server to run this! You can run it entirely on GitHub:

1. **Fork this repository** by clicking the **Fork** button in the top-right corner.
2. In your forked repository, go to **Settings** &rarr; **Secrets and variables** &rarr; **Actions**.
3. Click **New repository secret**:
   - **Name:** `APP_URLS`
   - **Value:** Your target URLs separated by commas:
     ```text
     https://my-app.onrender.com, https://api.koyeb.app, https://my-space.hf.space
     ```
4. *(Optional)* Add another secret `DISCORD_WEBHOOK` with your Discord webhook URL to receive instant alerts if any service goes down.
5. Go to the **Actions** tab, select **Cloud Keep-Alive Cron**, and click **Run workflow** to test it immediately!

The cron schedule will now automatically run every **12 minutes** in the cloud.

---

## 💻 Local & CLI Usage

You can also run it locally on your computer, VPS, or Raspberry Pi:

```bash
# Clone the repository
git clone https://github.com/ibrahimali111/render-keepalive.git
cd render-keepalive

# Option A: Run directly with an environment variable
export APP_URLS="https://my-app.onrender.com,https://api.koyeb.app"
python3 keepalive.py

# Option B: Create a urls.txt file
cp urls.txt.example urls.txt
# (Edit urls.txt with your own URLs)
python3 keepalive.py
```

### Output Preview:
```text
=================================================
   🚀 Render & Cloud Keep-Alive Heartbeat Bot   
=================================================

Loaded 2 endpoint(s) to ping:

STATUS   | LATENCY    | URL
-----------------------------------------------------------------
ONLINE   | 142.18 ms  | https://my-app.onrender.com
ONLINE   | 185.04 ms  | https://api.koyeb.app
-----------------------------------------------------------------

[✓] All 2 services are active and awake!
```

---

## 🐳 Docker Deployment

```bash
docker build -t render-keepalive .
docker run -d --name keepalive -e APP_URLS="https://my-app.onrender.com" render-keepalive
```

---

## 🛡️ License

Distributed under the [MIT License](LICENSE). Free for personal and commercial use.
