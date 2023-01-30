import asyncio
from pyppeteer import launch
import re

async def extract_website(url):
    browser = await launch()
    page = await browser.newPage()
    await page.goto(url)
    
    element = await page.querySelector('html')
    text = await element.getProperty("textContent")
    
    
    links = []

    scrapedLinkElems = await page.querySelectorAll('a')
    for linkElem in scrapedLinkElems:
        url_text = await page.evaluate('(el) => el.textContent', linkElem)
        url = await page.evaluate('(el) => el.href', linkElem)
        
        links.append(url)
    import ipdb
    ipdb.set_trace()
    
    
    await browser.close()


asyncio.get_event_loop().run_until_complete(extract_website("https://www.gaonnurinyc.com/"))