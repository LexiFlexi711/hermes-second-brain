---
title: "Hermes Vision Capture"
type: project
status: operational
created: 2026-06-12
tags: [hermes, vision, screenshot, playwright, chromium, cdp]
---

# Hermes Vision Capture

Hermes kan nu zelfstandig screenshots nemen van zijn dashboards en die
visueel analyseren via browser_vision.

## Skills Gemaakt

### hermes-vision-capture
- **Locatie:** `~/.hermes/skills/hermes-agent/hermes-vision-capture/`
- **Script:** `scripts/capture.py`
- Gebruikt Playwright in `/home/sjoe/venv/` met headless Chromium
- Parameters: url, output, width, height, full-page, wait-until, timeout
- Default output: `/tmp/hermes_vision/<safe_name>_<timestamp>.png`
- Na elke capture: `ls -lh` + `file` + PIL validatie + afmetingen
- Exitcodes: 0=OK, 1=browser error, 2=timeout, 3=HTTP error, 4=validation error, 5=argument error

### hermes-vision-analyze
- **Locatie:** `~/.hermes/skills/hermes-agent/hermes-vision-analyze/`
- **Script:** `scripts/serve_image.py`
- Start HTTP server om PNG te serveren voor Hermes browser_vision
- Parameters: --image, --port (optioneel, auto-pick)
- Server stopt na 120s idle timeout
- Output: SERVE_OK met URL + metadata

## CDP Lokale Chromium Setup

Gebruikt Playwright's Chromium (Chrome 149) voor lokale browser via CDP.

**Start commando:**
```bash
rm -rf /tmp/hermes-cdp-profile
mkdir -p /tmp/hermes-cdp-profile
/home/sjoe/.cache/ms-playwright/chromium-1223/chrome-linux64/chrome \
  --headless \
  --no-sandbox \
  --disable-gpu \
  --disable-dev-shm-usage \
  --remote-debugging-port=9222 \
  --remote-debugging-address=127.0.0.1 \
  --user-data-dir=/tmp/hermes-cdp-profile \
  --window-size=1280,800
```

**Verificatie:**
```bash
curl -s http://127.0.0.1:9222/json/version
```

## Config Wijzigingen (config.yaml)

```yaml
browser:
  cdp_url: http://127.0.0.1:9222
  allow_private_urls: true    # tijdelijk voor test

auxiliary:
  vision:
    provider: openrouter
    model: openai/gpt-4o-mini
    base_url: https://openrouter.ai/api/v1
    api_key: ${OPENROUTER_API_KEY}
    timeout: 120
```

## Status 2026-06-12

- ✅ capture.py — Playwright screenshot, PIL validatie, exitcodes
- ✅ serve_image.py — HTTP server, auto-port, idle watchdog 120s
- ✅ CDP Chromium — headless, eigen profile, port 9222
- ✅ browser_navigate — werkt naar localhost via CDP
- ❌ browser_vision — werkt nog niet in huidige sessie (config pas na /reset)

**Notities:**
- `skill_manage(action='patch')` verwijdert executable bit — chmod +x nodig na patch
- Print output in background processen moet flush=True voor capture door Hermes
- De Docker Chromium (poort 3000, Cloudflare, Caddy) is onaangeroerd — aparte headless instance op 9222
