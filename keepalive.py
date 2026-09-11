#!/usr/bin/env python3
"""
render-keepalive
Zero-dependency 24/7 cloud app keep-alive & uptime heartbeat bot.
Pings your free-tier Render, Koyeb, Glitch, and Hugging Face services so they never sleep.
"""

import os
import sys
import time
import json
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor

# ANSI Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"


def get_target_urls():
    """Retrieve URLs from environment variable or urls.txt file."""
    urls = []
    
    # Check environment variable APP_URLS
    env_urls = os.getenv("APP_URLS", "").strip()
    if env_urls:
        for u in env_urls.split(","):
            cleaned = u.strip()
            if cleaned:
                urls.append(cleaned)
                
    # Check local urls.txt file
    if os.path.exists("urls.txt"):
        try:
            with open("urls.txt", "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        if line not in urls:
                            urls.append(line)
        except Exception as e:
            print(f"{YELLOW}[!] Warning reading urls.txt: {e}{RESET}")
            
    # Normalize URLs to include http/https
    normalized = []
    for u in urls:
        if not u.startswith("http://") and not u.startswith("https://"):
            u = "https://" + u
        normalized.append(u)
        
    return normalized


def ping_url(url, timeout=15):
    """Ping a single endpoint and return status and latency."""
    headers = {
        "User-Agent": "Render-KeepAlive/1.0 (+https://github.com/ibrahimali111/render-keepalive)"
    }
    req = urllib.request.Request(url, headers=headers, method="GET")
    
    start_time = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            latency = (time.time() - start_time) * 1000
            status_code = response.getcode()
            return {
                "url": url,
                "status": status_code,
                "latency_ms": round(latency, 2),
                "success": 200 <= status_code < 400,
                "error": None
            }
    except urllib.error.HTTPError as e:
        latency = (time.time() - start_time) * 1000
        return {
            "url": url,
            "status": e.code,
            "latency_ms": round(latency, 2),
            "success": e.code in [401, 403],  # Some auth endpoints return 401/403 but are awake
            "error": f"HTTP {e.code}"
        }
    except Exception as e:
        latency = (time.time() - start_time) * 1000
        return {
            "url": url,
            "status": 0,
            "latency_ms": round(latency, 2),
            "success": False,
            "error": str(e)
        }


def send_discord_alert(webhook_url, failures):
    """Send a notification to Discord if any services are down."""
    if not webhook_url or not failures:
        return
        
    embed_fields = []
    for f in failures:
        embed_fields.append({
            "name": f["url"],
            "value": f"Error: `{f['error']}` | Status: `{f['status']}`",
            "inline": False
        })
        
    payload = {
        "username": "KeepAlive Monitor",
        "embeds": [{
            "title": "⚠️ Service Outage Detected",
            "color": 15158332,
            "fields": embed_fields,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }]
    }
    
    try:
        req = urllib.request.Request(
            webhook_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        urllib.request.urlopen(req, timeout=10)
        print(f"{CYAN}[*] Discord alert dispatched successfully.{RESET}")
    except Exception as e:
        print(f"{YELLOW}[!] Failed to send Discord alert: {e}{RESET}")


def main():
    print(f"\n{BOLD}{CYAN}================================================={RESET}")
    print(f"{BOLD}{CYAN}   🚀 Render & Cloud Keep-Alive Heartbeat Bot   {RESET}")
    print(f"{BOLD}{CYAN}================================================={RESET}\n")
    
    urls = get_target_urls()
    if not urls:
        print(f"{RED}[!] Error: No target URLs found!{RESET}")
        print(f"Set {YELLOW}APP_URLS{RESET} environment variable or create {YELLOW}urls.txt{RESET}.")
        sys.exit(1)
        
    print(f"Loaded {BOLD}{len(urls)}{RESET} endpoint(s) to ping:\n")
    
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(ping_url, urls))
        
    failures = []
    print(f"{'STATUS':<8} | {'LATENCY':<10} | {'URL'}")
    print("-" * 65)
    
    for r in results:
        if r["success"]:
            status_text = f"{GREEN}ONLINE{RESET}"
            latency_text = f"{r['latency_ms']} ms"
            print(f"{status_text:<17} | {latency_text:<10} | {r['url']}")
        else:
            status_text = f"{RED}OFFLINE{RESET}"
            err_msg = r['error'] if r['error'] else f"Code {r['status']}"
            print(f"{status_text:<17} | {r['latency_ms']} ms   | {r['url']} ({YELLOW}{err_msg}{RESET})")
            failures.append(r)
            
    print("-" * 65)
    
    if failures:
        print(f"\n{RED}[!] {len(failures)} service(s) failed or unreachable!{RESET}")
        discord_webhook = os.getenv("DISCORD_WEBHOOK", "").strip()
        if discord_webhook:
            send_discord_alert(discord_webhook, failures)
        sys.exit(1)
    else:
        print(f"\n{GREEN}[✓] All {len(urls)} services are active and awake!{RESET}\n")
        sys.exit(0)


if __name__ == "__main__":
    main()
