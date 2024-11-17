import re
import json
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
from playwright.sync_api import sync_playwright, Page, expect


with sync_playwright() as p:
    browser = p.firefox.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.duolingo.com/")
    expect(page).to_have_url("https://www.duolingo.com/learn", timeout = 1000000000)
    with open(os.path.join(os.path.dirname(__file__), "config.json")) as f:
        config = json.load(f)
    username = config["user_name"]
    page.goto(f"https://www.duolingo.com/api/1/users/show?username={username}")
    page.wait_for_load_state('networkidle');
    dat = page.content()
    dat = dat.removesuffix('</pre></body></html>')
    dat = dat.removeprefix('<html><head><link rel="stylesheet" href="resource://content-accessible/plaintext.css"></head><body><pre>')
    dat = json.loads(dat)
    inlang = dat["tracking_properties"]["direction"][:2]
    outlang = dat["tracking_properties"]["direction"][-2:]
    words = [inlang, outlang]
    for skill in dat["language_data"][inlang]["skills"]:
        if skill["learned"]:
            words += skill["words"]

    words = ",".join(words)


print(words)



