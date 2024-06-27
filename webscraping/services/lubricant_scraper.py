# Loading necessary packages

from playwright.sync_api import sync_playwright
import json

LUBRICATION_LISTINGS_URL = "https://keeb-finder.com/accessories/lubrications"


with sync_playwright() as p:

    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    listings_page = context.new_page()
    listings_page.goto(LUBRICATION_LISTINGS_URL)
    
    data = []
    articles = len(listings_page.query_selector_all("article"))
    pages = int(listings_page.query_selector("body > div.flex.flex-wrap.justify-center > div.max-w-lg.w-full.px-4.my-2.z-0 > div.MuiBox-root.mui-0 > nav > ul > li:nth-child(3) > a").inner_text()) # type: ignore
    for pagination in range(1, pages + 1, 1):
        listings_page.goto(f"https://keeb-finder.com/accessories/lubrications?page={pagination}")

        # To do: Fix lubricant scraper (name)
        
        for article in range(1, articles + 1, 1):
            name = listings_page.query_selector(f'body > div.flex.flex-wrap.justify-center > div.max-w-lg.w-full.px-4.my-2.z-0 > div.grid.gap-4.grid-cols-2.xs\:grid-cols-2.sd\:grid-cols-3.lg\:grid-cols-4 > article:nth-child({article}) > \
                                                div.flex.flex-wrap.items-center.justify-between.mt-1.mb-1\.5 > a.font-h4.text-h4.text-gray-900.dark\:text-gray-100.p-1.text-left.cursor-pointer.webkit-box.overflow-hidden.no-underline.line-clamp-2').inner_text() # type: ignore
            
            price = listings_page.query_selector(f'body > div.flex.flex-wrap.justify-center > div.max-w-lg.w-full.px-4.my-2.z-0 > div.grid.gap-4.grid-cols-2.xs\:grid-cols-2.sd\:grid-cols-3.lg\:grid-cols-4 > article:nth-child(1) > \
                                                 div.aspect-\[1\/1\].relative.w-full.overflow-hidden.rounded-lg.bg-gray-200.undefined > div').inner_text() # type: ignore
            try:
                availability = listings_page.query_selector(f'body > div.flex.flex-wrap.justify-center > div.max-w-lg.w-full.px-4.my-2.z-0 > div.grid.gap-4.grid-cols-2.xs\:grid-cols-2.sd\:grid-cols-3.lg\:grid-cols-4 > article:nth-child(23) > div.aspect-\[1\/1\].relative.w-full.overflow-hidden.rounded-lg.bg-gray-200.undefined > \
                                                            div.absolute.inset-0.bg-black.bg-opacity-30.z-10.pointer-events-none > div > div').inner_text() # type: ignore      
    
            except AttributeError:
                availability = "In stock"

            data.append({
                "name": name,
                "price": price,
                "availability": availability
            })

    context.close()
    browser.close()

    with open('webscraping/data/lubricants.json', 'w') as f:
            json.dump(data, f, indent=4)
