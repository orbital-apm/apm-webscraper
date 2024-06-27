from playwright.sync_api import sync_playwright
import json

KIT_LISTINGS_URL = "https://keeb-finder.com/keyboards/acgam-fancyalice66-qmk-via-diy-kit"


with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    listings_page = context.new_page()
    listings_page.goto(KIT_LISTINGS_URL)

    pg = listings_page.query_selector('body > div.flex.flex-col.gap-4 > section:nth-child(1) > div > div.col-span-12.md\:col-span-5.md\:order-2.order-3 > \
                                      div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div.flex > div.text-green-400 > svg').get_attribute('data-testid')
    
    print(pg)

    context.close()
    browser.close()