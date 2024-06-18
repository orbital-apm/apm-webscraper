from playwright.sync_api import sync_playwright
import json

with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.goto("https://keeb-finder.com/switches/gateron-x-sw-modern-gray-linear-switches")

    data = []
    switch_type = page.query_selector(r'body > div.flex.flex-col.gap-4 > section:nth-child(1) > div > div.col-span-12.md\:col-span-5.md\:order-2.order-3 > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div.flex > div').inner_text()
    brand = page.query_selector(r'body > div.flex.flex-col.gap-4 > section:nth-child(1) > div > div.col-span-12.md\:col-span-5.md\:order-2.order-3 > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div.flex').inner_text()
    data.append([switch_type, brand])
    print(data)
    browser.close()

