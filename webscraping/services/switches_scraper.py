# Loading necessary packages

from playwright.sync_api import sync_playwright
import json

SWITCH_LISTINGS_URL = "https://keeb-finder.com/switches"


with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    listings_page = context.new_page()
    details = context.new_page()
    listings_page.goto(SWITCH_LISTINGS_URL)
    
    data = []
    articles = len(listings_page.query_selector_all("article"))
    pages = int(listings_page.query_selector("body > div.flex.flex-wrap.justify-center > div.max-w-lg.w-full.px-4.my-2.z-0 > \
                                    div.MuiBox-root.mui-0 > nav > ul > li:nth-child(8) > a").inner_text()) # type: ignore
    for pagination in range(1, 20, 1):
        listings_page.goto(f"https://keeb-finder.com/switches?page={pagination}")
        listings_page.screenshot(path="example_switches.png", full_page=True)
        for article in range(1, articles + 1, 1):
            name = listings_page.query_selector(f'body > div.flex.flex-wrap.justify-center > div.max-w-lg.w-full.px-4.my-2.z-0 > \
                                                div.grid.gap-4.grid-cols-2.xs\:grid-cols-2.sd\:grid-cols-3.lg\:grid-cols-4 > \
                                                article:nth-child({article}) > div.flex.flex-wrap.items-center.justify-between.mt-1.mb-1\.5 > \
                                                a.font-h4.text-h4.text-gray-900.dark\:text-gray-100.p-1.text-left.cursor-pointer.webkit-box.overflow-hidden.no-underline.line-clamp-2').inner_text() # type: ignore
            
            price = listings_page.query_selector(f'body > div.flex.flex-wrap.justify-center > div.max-w-lg.w-full.px-4.my-2.z-0 > div.grid.gap-4.grid-cols-2.xs\:grid-cols-2.sd\:grid-cols-3.lg\:grid-cols-4 > article:nth-child({article}) > \
                                                div.aspect-\[1\/1\].relative.w-full.overflow-hidden.rounded-lg.bg-gray-200.undefined > \
                                                div.absolute.right-1\.5.bottom-1\.5.flex.justify-end.bg-black.bg-opacity-70.p-1\.5.px-2.rounded.text-center.z-10.text-gray-100.font-medium').inner_text() # type: ignore
            
            link = listings_page.query_selector(f'body > div.flex.flex-wrap.justify-center > div.max-w-lg.w-full.px-4.my-2.z-0 > \
                                                div.grid.gap-4.grid-cols-2.xs\:grid-cols-2.sd\:grid-cols-3.lg\:grid-cols-4 > article:nth-child({article}) > \
                                                div.aspect-\[1\/1\].relative.w-full.overflow-hidden.rounded-lg.bg-gray-200.undefined > a').get_attribute('href') # type: ignore

            try:
                availability = listings_page.query_selector(f'body > div.flex.flex-wrap.justify-center > div.max-w-lg.w-full.px-4.my-2.z-0 > div.grid.gap-4.grid-cols-2.xs\:grid-cols-2.sd\:grid-cols-3.lg\:grid-cols-4 > article:nth-child({article}) > \
                                                    div.aspect-\[1\/1\].relative.w-full.overflow-hidden.rounded-lg.bg-gray-200.undefined > div.absolute.inset-0.bg-black.bg-opacity-30.z-10.pointer-events-none > div > div').inner_text() # type: ignore      
    
            except AttributeError:
                availability = "In stock"
        
            details.goto(f"https://keeb-finder.com{link}")
            details.screenshot(path="example_switches.png", full_page=True)
            
            vendors = []

            try:
                switch_type = details.query_selector('body > div.flex.flex-col.gap-4 > section:nth-child(1) > div > div.col-span-12.md\:col-span-5.md\:order-2.order-3 > \
                                                      div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div.flex > div').inner_text() # type: ignore
            except AttributeError:
                switch_type = None
            
            try:
                manufacturer = details.query_selector('body > div.flex.flex-col.gap-4 > section:nth-child(1) > div > div.col-span-12.md\:col-span-5.md\:order-2.order-3 > \
                                                      div:nth-child(1) > div:nth-child(2) > div:nth-child(1) > div.flex > div').inner_text() # type: ignore
            except AttributeError:
                manufacturer = None

            try:    
                actuation_force = details.query_selector('body > div.flex.flex-col.gap-4 > section:nth-child(1) > div > div.col-span-12.md\:col-span-5.md\:order-2.order-3 > \
                                                         div:nth-child(1) > div:nth-child(2) > div:nth-child(4) > div.flex > div').inner_text() # type: ignore
            except AttributeError:
                actuation_force = None

            try:    
                travel_distance = details.query_selector('body > div.flex.flex-col.gap-4 > section:nth-child(1) > div > div.col-span-12.md\:col-span-5.md\:order-2.order-3 > \
                                                         div:nth-child(1) > div:nth-child(2) > div:nth-child(6) > div.flex > div').inner_text() # type: ignore
            except AttributeError:
                travel_distance = None

            vendors_data = details.query_selector_all('body > div.flex.flex-col.gap-4 > section:nth-child(1) > div > div.col-span-12.order-2.md\:order-3.mt-2 > \
                                                    div.bg-gray-50.dark\:bg-gray-700.mt-4.rounded-lg.shadow-md.border.border-gray-200.dark\:border-gray-800 > table > tbody > tr:nth-child(4) > td.flex.items-center.p-2 > div > img')
            for i in vendors_data:
                vendors.append(i.get_attribute("alt"))


            data.append({
                "name": name,
                "price": price,
                "manufacturer": manufacturer,
                "switch_type": switch_type,
                "actuation_force": actuation_force,
                "travel_distance": travel_distance,
                "vendors": vendors,
                "availability": availability
            })


    context.close()
    browser.close()

    with open('webscraping/data/switches.json', 'w') as f:
            json.dump(data, f, indent=4)
