# Loading necessary packages

from playwright.sync_api import sync_playwright
import json

SWITCH_LISTINGS_URL = "https://keeb-finder.com/switches"


with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    listing_page = browser.new_page()
    details_page = browser.new_page()

    listing_page.goto(SWITCH_LISTINGS_URL)
    pages = int(listing_page.query_selector('body > div.flex.flex-wrap.justify-center > div.max-w-lg.w-full.px-4.my-2.z-0 > div.MuiBox-root.mui-0 > nav > ul > li:nth-child(8) > a').inner_text()) # type: ignore
    data = []

    for page in range(1, pages + 1, 1):
        listing_page.goto(f"https://keeb-finder.com/switches?page={page}")
        number_of_listings = len(listing_page.query_selector_all("article"))
        for i in range(1, number_of_listings + 1, 1):
            name = listing_page.query_selector(f'body > div.flex.flex-wrap.justify-center > div.max-w-lg.w-full.px-4.my-2.z-0 > div.grid.gap-4.grid-cols-2.xs\:grid-cols-2.sd\:grid-cols-3.lg\:grid-cols-4 > article:nth-child({i}) > \
                                               div.flex.flex-wrap.items-center.justify-between.mt-1.mb-1\.5 > a.font-h4.text-h4.text-gray-900.dark\:text-gray-100.p-1.text-left.cursor-pointer.webkit-box.overflow-hidden.no-underline.line-clamp-2').inner_text() # type: ignore
            price = listing_page.query_selector(f'body > div.flex.flex-wrap.justify-center > div.max-w-lg.w-full.px-4.my-2.z-0 > div.grid.gap-4.grid-cols-2.xs\:grid-cols-2.sd\:grid-cols-3.lg\:grid-cols-4 > article:nth-child({i}) > \
                                        div.aspect-\[1\/1\].relative.w-full.overflow-hidden.rounded-lg.bg-gray-200.undefined > div.absolute.right-1\.5.bottom-1\.5.flex.justify-end.bg-black.bg-opacity-70.p-1\.5.px-2.rounded.text-center.z-10.text-gray-100.font-medium').inner_text() # type: ignore
            link = listing_page.query_selector(f'body > div.flex.flex-wrap.justify-center > div.max-w-lg.w-full.px-4.my-2.z-0 > div.grid.gap-4.grid-cols-2.xs\:grid-cols-2.sd\:grid-cols-3.lg\:grid-cols-4 > article:nth-child({i}) > \
                                               div.aspect-\[1\/1\].relative.w-full.overflow-hidden.rounded-lg.bg-gray-200.undefined > a').get_attribute('href') # type: ignore

            try:
                availability = listing_page.query_selector(f'body > div.flex.flex-wrap.justify-center > div.max-w-lg.w-full.px-4.my-2.z-0 > div.grid.gap-4.grid-cols-2.xs\:grid-cols-2.sd\:grid-cols-3.lg\:grid-cols-4 > article:nth-child({i}) > \
                                                    div.aspect-\[1\/1\].relative.w-full.overflow-hidden.rounded-lg.bg-gray-200.undefined > div.absolute.inset-0.bg-black.bg-opacity-30.z-10.pointer-events-none > div > div').inner_text() # type: ignore      
    
            except AttributeError:
                availability = "In stock"
            
            details_page.goto(f"https://keeb-finder.com{link}")

            try:
                switch_type = details_page.query_selector('body > div.flex.flex-col.gap-4 > section:nth-child(1) > div > div.col-span-12.md\:col-span-5.md\:order-2.order-3 > \
                                                      div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div.flex > div').inner_text() # type: ignore
                
            except AttributeError:
                switch_type = "No type found."

            data.append({
                "name": name,
                "price": price,
                "switch_type": switch_type,
                "availability": availability
            })
            

    browser.close()

    with open('webscraping/data/switches.json', 'w') as f:
            json.dump(data, f, indent=4)


