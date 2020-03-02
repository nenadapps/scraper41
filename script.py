from bs4 import BeautifulSoup
import datetime
from random import randint
from random import shuffle
import requests
from time import sleep

base_url = 'https://garylyon.com'

def get_html(url):
    
    html_content = ''
    try:
        page = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        html_content = BeautifulSoup(page.content, "html.parser")
    except: 
        pass
    
    return html_content

def get_details(url):
    
    stamp = {}
    
    try:
        html = get_html(url)
    except:
        return stamp
    
    try:
        title = html.select('h1.product-page-header')[0].get_text().strip()
        stamp['title'] = title
    except:
        stamp['title'] = None      
    
    try:
        raw_text = html.select('#description')[0].get_text().strip()
        stamp['raw_text'] = raw_text
    except:
        stamp['raw_text'] = None
    
    try:
        price = html.select('.variant-price')[0].get_text().strip()
        price = price.replace('Price: $', '').replace(' (CAD)', '').strip()
        stamp['price'] = price
    except:
        stamp['price'] = None  
    
    try:
        category = html.select('a.SectionTitleText')[0].get_text().strip()
        stamp['category'] = category
    except:
        stamp['category'] = None  
       
    try:
        subcategory = html.select('a.SectionTitleText')[1].get_text().strip()
        stamp['subcategory'] = subcategory
    except:
        stamp['subcategory'] = None     
        
       

    stamp['currency'] = 'CAD'
    
    # image_urls should be a list
    images = []                    
    try:
        if len(html.select('.product-gallery-image')):
            image_items = html.select('.product-gallery-image')
        else:
            image_items = html.select('img.product-image')

        for image_item in image_items:
            img_src = image_item.get('src').replace('/medium/', '/large/').replace('/micro/', '/large/')
            img = base_url + img_src
            if img not in images:
                images.append(img)
    except:
        pass
    
    stamp['image_urls'] = images 
        
    # scrape date in format YYYY-MM-DD
    scrape_date = datetime.date.today().strftime('%Y-%m-%d')
    stamp['scrape_date'] = scrape_date
    
    stamp['url'] = url
    
    print(stamp)
    print('+++++++++++++')
    sleep(randint(25, 65))
           
    return stamp

def get_page_items(url):

    items = []
    next_url = ''

    try:
        html = get_html(url)
    except:
        return items, next_url

    try:
        for item in html.select('.entity-product-name-wrap a'):
            item_link = base_url + item.get('href')
            if item_link not in items:
                items.append(item_link)
    except:
        pass
    
    try:
        next_url_cont = html.find_all('a', attrs={'aria-label':'Next Page'})[0]
        next_url_href = next_url_cont.get('href')
        if next_url_href:
            next_url = base_url + next_url_href
    except:
        pass
   
    shuffle(list(set(items)))
    
    return items, next_url

def get_categories():
    
    url = 'https://garylyon.com'
   
    items = []

    try:
        html = get_html(url)
    except:
        return items

    try:
        for item in html.select('.category-menu a'):
            item_link = base_url  + '/' + item.get('href')
            if item_link not in items: 
                items.append(item_link)
    except: 
        pass
    
    shuffle(list(set(items)))
    
    return items

def get_subcategories(url):
   
    items = []

    try:
        html = get_html(url)
    except:
        return items

    try:
        for item in html.select('a.sub-entity-name-link'):
            item_link = base_url  + '/' + item.get('href')
            if item_link not in items: 
                items.append(item_link)
    except: 
        pass
    
    shuffle(list(set(items)))
    
    return items

categories = get_categories()   
for category in categories:
    subcategories = get_subcategories(category) 
    for subcategory in subcategories:
        page_url = subcategory
        while(page_url):
            page_items, page_url = get_page_items(page_url)
            for page_item in page_items:
                stamp = get_details(page_item) 
