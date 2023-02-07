import asyncio
from pyppeteer import launch
import json

class Scraper():
    def __init__(self, url:str, page):
        self.url = url
        self.visited_urls = []
        self.page = page
        self.parsed = {
            'title':'',
            'base_url':url,
            'description':'',
            'pages':{},
            'contact':{
                'phone':'',
                'address':''
            },
            'social':{
                'facebook':[],
                'instagram':[],
                'twitter':[],
                'youtube':[],
                'tiktok':[]
            },
            'documents':[],
            'links':[]
        }
        
    async def close(self):
        self.browser.close()

    async def parsePage(self,url,page_limit):
        if len(self.parsed.get('pages').keys()) >= page_limit:
            return self.parsed
        print(url)
        await self.page.goto(url)
        
        # Scrape all links
        links = []
        
        scrapedLinkElems = await self.page.querySelectorAll('a')
        for linkElem in scrapedLinkElems:
            link_text = await self.page.evaluate('(el) => el.textContent', linkElem)
            link_url = await self.page.evaluate('(el) => el.href', linkElem)
            
            links.append(link_url)
        
        self.parsed['links'] = list(set(self.parsed.get('links') + links))
        
        facebook_links = [x for x in links if 'facebook.com' in x]
        instagram_links = [x for x in links if 'instagram.com' in x]
        twitter_links = [x for x in links if 'twitter.com' in x]
        youtube_links = [x for x in links if 'youtube.com' in x]
        tiktok_links = [x for x in links if 'tiktok.com' in x]
        

        self.parsed.get('social')['facebook'] = list(set(self.parsed.get('social').get('facebook') + facebook_links))
        self.parsed.get('social')['instagram'] = list(set(self.parsed.get('social').get('instagram') + instagram_links))
        self.parsed.get('social')['twitter'] = list(set(self.parsed.get('social').get('twitter') + twitter_links))
        self.parsed.get('social')['youtube'] = list(set(self.parsed.get('social').get('youtube') + twitter_links))
        self.parsed.get('social')['tiktok'] = list(set(self.parsed.get('social').get('tiktok') + twitter_links))
        


        # Pull out page content
        titleElem = await self.page.querySelector('title')
        title = await self.page.evaluate('(el) => el.textContent', titleElem)

        contents = []
        contentElems = await self.page.querySelectorAll('p')
        for contentElem in contentElems:
            content = await self.page.evaluate('(el) => el.textContent', contentElem)
            contents.append(content)

        images = []
        imgElems = await self.page.querySelectorAll('img')
        for imgElem in imgElems:
            image_url = await self.page.evaluate('(el) => el.src', imgElem)
            image_caption = await self.page.evaluate('(el) => el.alt', imgElem)
            
            images.append({
                'url':image_url,
                'caption':image_caption
            })


    
        document_links = [x for x in links if any(list(map(lambda y:y in x, ['.pdf','.txt','.csv','.json','.xlsx'])))]

        
        # Extract Contact info
        
        
        # Update Page info
        self.parsed.get('pages')[url] = {
            'title':title,    
            'content':contents,
            'images':images,
            'documents':document_links
        }

        
        # Recursively Parse subpages
        for link in links:
            # Ensure part of same site
            
            if self.parsed.get('base_url') in link:
        
                # Don't parse already parsed pages
                if link not in list(self.parsed.get('pages').keys()):
                    if link not in document_links:
                        await self.parsePage(link,page_limit) 


        

        return self.parsed
        



async def scrape(url, page_limit):
    browser = await launch()
    page = await browser.newPage()


    web_scraper = Scraper(url, page)
    try:
        result = await web_scraper.parsePage(url,page_limit)
    except:
        result = web_scraper.parsed
    await browser.close()

    return result 


def getWebsiteInfo(base_url,page_limit=10):
    result = asyncio.get_event_loop().run_until_complete(scrape(base_url,page_limit))
    return result