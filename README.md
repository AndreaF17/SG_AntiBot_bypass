# PoC Bypass SiteGround AI Antibot Protection

This is a proof-of-concept (PoC) script designed to bypass SiteGround's AI-powered antibot protection. The script utilizes Selenium WebDriver and Python's `requests` library to automate a browser session on Firefox.

## Insight
Siteground triggers the Antibot process when:

* The IP address is reported.
* The IP address makes extensive interactions with the endpoint.

After performing some reverse-engineering, I observed that Siteground's antibot detection mechanism creates a cookie with the following format:

```
_I_: 89d4b4400b603ce9ee6e1afecdbc09488b45aae90cbdcb5f9b63a5437fd8881c-1747298858
```

The cookie's value is generated using the `User Agent` information extracted from the request being checked.

Once the `_I_` value has been established, Siteground's Antibot Detection does not further evaluate the subsequent request behavior.

The cookie can be used for at least 12 hours.

## Usage

To use this script, you'll need to have the following prerequisites installed:

- Python 3.x
- Selenium WebDriver for Firefox
- requests library

### Install GeckoDriver

**Step 1:** Download GeckoDriver
```bash
wget https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz
```
**Step 2:** Unzip the tar file
```bash
sudo tar -xvf geckodriver-v0.26.0-linux64.tar.gz
```
**Step 3:** Move GeckoDriver to binary location
```bash
sudo mv geckodriver /usr/local/bin/
```
**Step 4:** Make it executable
```bash
sudo chmod +x /usr/local/bin/geckodriver
```

GeckoDriver setup successful.

1. Clone or download this repository.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Update the `TARGET` variable in the script with your desired target URL.
## Usage Options

The script accepts two command-line arguments:

- `-t, --target`: The target URL to test against SiteGround's antibot protection.
- `-ua, --user-agent`: A custom User-Agent string (optional).
To run the script, execute it using Python:
```bash
python bypass_sitesground_antibot.py -t <TARGET_URL> [-ua <USER_AGENT_STRING>]
```

### Example Output

If the script is successful in bypassing SiteGround's antibot protection, you'll see the following output:
```bash
Valid Cookie ID and User-Agent

Use in your future requests:
Cookie: _I_: <COOKIE_ID>
Header: User-Agent: <USER_AGENT>

Example:
- curl -I "<TARGET_URL>" -H "Cookie: _I_=<COOKIE_ID>" -H "User-Agent: <USER_AGENT>"
```
##  Notes

- This script is for educational purposes only and should not be used to engage in malicious activities.
- SiteGround's antibot protection may change or evolve over time, making this PoC obsolete. Use at your own risk!
