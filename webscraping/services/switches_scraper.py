# Loading necessary packages

from playwright.sync_api import sync_playwright
import json


KEYCAP_URL = "https://keeb-finder.com/keycaps"
LUBRICANT_URL = "https://keeb-finder.com/accessories/lubrications"
KIT_URL = "https://keeb-finder.com/keyboards"
SWITCH_URL = "https://keeb-finder.com/switches"


with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page1 = browser.new_page()

    page.goto(SWITCH_URL)
    page_number = int(page.query_selector('body > div.flex.flex-wrap.justify-center > div.max-w-lg.w-full.px-4.my-2.z-0 > div.MuiBox-root.mui-0 > nav > ul > li:nth-child(8) > a').inner_text())
    data = []

    for page_no in range(1, page_number + 1, 1):
        page.goto(f"https://keeb-finder.com/switches?page={page_no}")
        number_of_listings = len(page.query_selector_all("article"))
        for i in range(1, number_of_listings + 1, 1):
            name = page.query_selector(f'body > div.flex.flex-wrap.justify-center > div.max-w-lg.w-full.px-4.my-2.z-0 > div.grid.gap-4.grid-cols-2.xs\:grid-cols-2.sd\:grid-cols-3.lg\:grid-cols-4 > article:nth-child({i}) > \
                                    div.flex.flex-wrap.items-center.justify-between.mt-1.mb-1\.5.group > a.font-h4.text-h4.text-gray-900.dark\:text-gray-100.p-1.text-left.cursor-pointer.webkit-box.overflow-hidden.no-underline.line-clamp-2').inner_text()
            price = page.query_selector(f'body > div.flex.flex-wrap.justify-center > div.max-w-lg.w-full.px-4.my-2.z-0 > div.grid.gap-4.grid-cols-2.xs\:grid-cols-2.sd\:grid-cols-3.lg\:grid-cols-4 > article:nth-child({i}) > \
                                        div.aspect-\[1\/1\].relative.w-full.overflow-hidden.rounded-lg.bg-gray-200.undefined > div.absolute.right-1\.5.bottom-1\.5.flex.justify-end.bg-black.bg-opacity-70.p-1\.5.px-2.rounded.text-center.z-10.text-gray-100.font-medium').inner_text()
            
            try:
                availability = page.query_selector(f'body > div.flex.flex-wrap.justify-center > div.max-w-lg.w-full.px-4.my-2.z-0 > div.grid.gap-4.grid-cols-2.xs\:grid-cols-2.sd\:grid-cols-3.lg\:grid-cols-4 > article:nth-child({i}) > \
                                                    div.aspect-\[1\/1\].relative.w-full.overflow-hidden.rounded-lg.bg-gray-200.undefined > div.absolute.inset-0.bg-black.bg-opacity-30.z-10.pointer-events-none > div > div').inner_text()          
    
            except AttributeError:
                availability = "In stock"
            
            link = page.get_by_role('link', name=name).first().get_attribute('href')
            page1.goto(f"https://keeb-finder.com{link}")

            switch_type = page1.query_selector(r'body > div.flex.flex-col.gap-4 > section:nth-child(1) > div > div.col-span-12.md\:col-span-5.md\:order-2.order-3 > div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div.flex > div').inner_text()
            brand = page1.query_selector(r'body > div.flex.flex-col.gap-4 > section:nth-child(1) > div > div.col-span-12.md\:col-span-5.md\:order-2.order-3 > div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div.flex').inner_text()
                   
            data.append({
                "name": name,
                "price_per_unit": price,
                "switch_type": switch_type,
                "availability": availability,
                "brand": brand
            })

            

    browser.close()

    with open('app/services/webscraper/data/switches.json', 'w') as f:
            json.dump(data, f, indent=4)


