from playwright.sync_api import sync_playwright
import json

STABILIZERS_LISTINGS_URL = "https://keeb-finder.com/accessories/stabilizers"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    listings_page = context.new_page()
    listings_page.goto(STABILIZERS_LISTINGS_URL)
    
    data = []
    pages = int(listings_page.query_selector("body > div.flex.flex-wrap.justify-center > div.max-w-lg.w-full.px-4.my-2.z-0 > div.MuiBox-root.mui-0 > nav > ul > li:nth-child(3) > a").inner_text()) # type: ignore
    
    for pagination in range(1, pages, 1):
        listings_page.goto(f"{STABILIZERS_LISTINGS_URL}?page={pagination}")
        articles = listings_page.query_selector_all("article")
        
        for article in articles:
            name = article.query_selector('div.flex.flex-wrap.items-center.justify-between.mt-1.mb-1\\.5 > a.font-h4.text-h4.text-gray-900.dark\\:text-gray-100.p-1.text-left.cursor-pointer.webkit-box.overflow-hidden.no-underline.line-clamp-2').inner_text() # type: ignore
            
            price = article.query_selector('div.aspect-\\[1\\/1\\].relative.w-full.overflow-hidden.rounded-lg.bg-gray-200.undefined > div').inner_text() # type: ignore

            
            
            if price == "Out of stock":
                price = None

            try:
                stock_element = article.query_selector('div.aspect-\\[1\\/1\\].relative.w-full.overflow-hidden.rounded-lg.bg-gray-200.undefined > div.absolute.inset-0.bg-black.bg-opacity-30.z-10.pointer-events-none > div > div')
                availability = False if stock_element else True
            except AttributeError:
                availability = True

            img_element = article.query_selector('img')
            img_url = img_element.get_attribute('src') if img_element else None

            data.append({
                "name": name,
                "price": price,
                "img_url": img_url,
                "availability": availability
            })

    context.close()
    browser.close()

    with open('webscraping/data/lubricants.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

print("Data extraction for lubricants completed successfully.")