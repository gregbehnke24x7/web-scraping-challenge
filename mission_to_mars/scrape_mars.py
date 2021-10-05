# Import Dependencies
#import numpy as np
import pandas as pd
import time as time
from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager

# function to setup browser
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

# function to scrape data
def scrape():

# ping first page with splinter for the most recent news article
    url = 'https://redplanetscience.com/'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    #browser.quit()

# parse news html for datas
    Data = BeautifulSoup(html, "html.parser")
    news_date = Data.find('div',class_="list_date").text
    news_title = Data.find('div',class_="content_title").text
    news_text = Data.find('div',class_="article_teaser_body").text

# ping next page with splinter for featured image
    #browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    #browser.quit()

# parse html for featured image
    Data = BeautifulSoup(html, "html.parser")
    images = Data.find_all('img')
    featured_image_url =  url + images[1]['src']
    #print(featured_image_url)

# ping factoid page with pandas for some interesting facts
    url = 'https://galaxyfacts-mars.com'
    mars_data = pd.read_html(url)
    mars_df1 = pd.DataFrame(mars_data[0])
    #mars_df1

# drop header, rename columns, clean it up a bit
    head = mars_df1.index[[0]]
    mars_df1.drop(head, inplace=True)
    mars_df1.drop(columns=[2], inplace=True)
    mars_df1.reset_index()
    mars_df1.rename(columns={0: "Attribute", 1: "Value"}, inplace=True)
    #mars_df1.head()

# get the rest of the interesting factoids 
    mars_df2 = pd.DataFrame(mars_data[1])
    mars_df2.rename(columns={0: "Attribute", 1: "Value"}, inplace=True)
    #mars_df2

# combine the two sets of facts and convert to html
    mars_df = mars_df1.append(mars_df2, ignore_index=True).copy()
    #mars_df
    fact_table_html = mars_df.to_html()
    #print(fact_table_html)

# now lets get some pretty pictures of the hemispheres of Mars with splinter
    #browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    time.sleep(1)
    html = browser.html
    #browser.quit()
    Data = BeautifulSoup(html, "html.parser")

# save the image descriptions
    image_descr = []
    for descr in Data.find_all('h3'):
        image_descr.append(descr.text)
    
    hemi_descr_df = pd.DataFrame(image_descr)
    hemi_descr_df

# go fetch the url 'tail' for each of the images
    image_urls = []
    for line in Data.find_all('a', href=True):
        href_str = str(line['href'])
        extn = "html"
        if extn in href_str:
            image_urls.append(href_str)

    image_df = pd.DataFrame(image_urls)
    image_df.drop_duplicates(inplace=True)
    image_df.rename(columns={0: "tail"}, inplace=True)
    image_df

# using the image url 'tail' and the base url, get each full image url
    #browser = Browser('chrome', **executable_path, headless=False)
    base_url = 'https://marshemispheres.com/'
    hemi_image_urls = []

    for i, hemi in image_df.iterrows():
        tail = hemi["tail"]
        url = base_url + tail
        #print(f"{url}")
        browser.visit(url)
        time.sleep(1)
        html = browser.html
        Data = BeautifulSoup(html, "html.parser")
        image = Data.find_all(class_='wide-image')
        hemi_image_url =  url + image[0]['src']
        hemi_image_urls.append(hemi_image_url)
    
    browser.quit()
    hemi_image_df = pd.DataFrame(hemi_image_urls)
    #hemi_image_df

    hemi_df = hemi_descr_df.copy()
    hemi_df[["img_url"]] = hemi_image_df[[0]]
    hemi_df.rename(columns={0: "title"}, inplace=True)
    hemi_df.dropna(axis=0, inplace=True)
    #hemi_df
    hemisphere_image_urls = hemi_df.to_dict('records')
    #hemisphere_image_urls

    mars_dict ={
         'news_title'      : news_title,
         'news_date'       : news_date,
         'news_text'       : news_text,
         'featured_image'  : featured_image_url,
         'fact_table_html' : fact_table_html,
         'mars_hemispheres': hemisphere_image_urls                    
     }

    return mars_dict



