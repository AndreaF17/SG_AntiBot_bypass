# PoC — Bypass SiteGround AI Antibot Protection

A proof-of-concept script that bypasses SiteGround's AI-powered antibot protection using Selenium WebDriver (Firefox) and Python's `requests` library.

## How It Works

SiteGround triggers its antibot process when:

- The IP address has been reported as malicious.
- The IP address makes an excessive number of requests to an endpoint.

After reverse-engineering the mechanism, I found that SiteGround generates a `_I_` cookie tied to the request's `User-Agent`:

```
_I_=89d4b4400b603ce9ee6e1afecdbc09488b45aae90cbdcb5f9b63a5437fd8881c-1747298858
```

Once this cookie is established, SiteGround's antibot does not re-evaluate subsequent requests that carry it. The cookie remains valid for at least 12 hours.

## Prerequisites

- Python 3.x
- Firefox browser
- GeckoDriver (see install steps below)

## Setup

### 1. Install GeckoDriver

Download the appropriate release for your platform from [github.com/mozilla/geckodriver/releases](https://github.com/mozilla/geckodriver/releases/), then run:

```bash
tar -xvf geckodriver-*.tar.gz
sudo mv geckodriver /usr/local/bin/
sudo chmod +x /usr/local/bin/geckodriver
```

### 2. Install Python dependencies

```bash
git clone https://github.com/your-repo/SG_AntiBot_bypass.git
cd SG_AntiBot_bypass
pip install -r requirements.txt
```

## Usage

```
python main.py -t <TARGET_URL> [-ua <USER_AGENT>] [--geckodriver <PATH>]
```

| Argument | Required | Description |
|---|---|---|
| `-t, --target` | Yes | Target URL |
| `-ua, --user-agent` | No | Custom User-Agent string (defaults to a standard Firefox UA) |
| `--geckodriver` | No | Path to geckodriver binary (auto-detected if in PATH) |

### Examples

```bash
# Basic usage
python main.py -t https://example.com

# Custom User-Agent
python main.py -t https://example.com -ua "Mozilla/5.0 (compatible; Googlebot/2.1)"

# Custom geckodriver path
python main.py -t https://example.com --geckodriver /opt/geckodriver
```

### Output

On success:

```
Valid Cookie ID and User-Agent

Use in your future requests:
  Cookie:     _I_=<COOKIE_VALUE>
  User-Agent: <USER_AGENT>

Example:
  curl -I "https://example.com" -H "Cookie: _I_=<COOKIE_VALUE>" -H "User-Agent: <USER_AGENT>"
```

## Notes

- For educational and authorized testing purposes only.
- SiteGround's antibot protection may change over time. Use at your own risk.
