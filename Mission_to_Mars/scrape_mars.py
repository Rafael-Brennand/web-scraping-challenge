#Dependencies
import os
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

#Scrapping --------------------------------------------------------------------------------------------------------
#Mars News

def mars_news(browser):
    #URL used to scrape
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    n_soup = bs(html, 'html.parser')

    try:
        #Find the title of the first news article
        title_elem = n_soup.select_one('ul.item_list li.slide')
        title_elem = title_elem.find('div', class_='content_title').get_text()

        #Get the paragraph for the news article found
        paragraph_elem = n_soup.select_one('ul.item_list li.slide')
        paragraph_elem = paragraph_elem.find('div', class_='article_teaser_body').get_text()

    except:
        return None, None

    return title_elem, paragraph_elem

def mars_feat(browser):
    #URL used to scrape
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    #Find the image called full_image
    featured_image_url = browser.find_by_id("full_image")
    featured_image_url.click()

    #Go through the More Info button
    moreinfo = browser.links.find_by_partial_text('more info')
    moreinfo.click()
    html = browser.html
    img_soup = bs(html,'html.parser')

    #Assign the url
    img_url = img_soup.find('figure',class_='lede').find('a').get('href')

    featured_url = 'https://www.jpl.nasa.gov' + img_url

    return featured_url

def mars_facts(browser):
    #URL used to scrape
    url = 'https://space-facts.com/mars/'
    browser.visit(url)

    table = pd.read_html(url)

    #Make it into a pandas column
    fact_table = table[0]
    fact_table.columns = ["Category", "Unit"]

    #Convert it back to HTML
    fact_html = fact_table.to_html()
    fact_html.replace('\n','')

    return fact_table

def hems_imgs(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html = browser.html
    hemispheres_soup = bs(html, 'html.parser')
    hemispheres_url = hemispheres_soup.find_all('div', class_='item')

    hem_dict = []

    for hem in range(len(hemispheres_url)):
        hem_item = {}    
        
        # click on each of the links
        browser.find_by_css('a.product-item h3')[hem].click()
        
        # get the enhanced image title
        hem_item["img_title"] = browser.find_by_css('h2.title').text
        # get the enhanced image link
        hem_item["img_url"] = browser.links.find_by_text('Sample')['href']
            
        # add it to the hemisphere dictionary
        hem_dict.append(hem_item)
        
        # have to go back to the main browser page
        browser.back()

    return hem_dict

def scrape():
    title_elem, paragraph_elem = mars_news(browser)
    featured_url = mars_feat(browser)
    fact_table = mars_facts(browser)
    hem_dict = hems_imgs(browser)

    data_dict = {
        "news_title":title_elem,
        "news_paragraph": paragraph_elem,
        "featured_image_url":featured_url,
        "facts":fact_table,
        "hemisphere_images":hem_dict
    }

    browser.quit()
    return data_dict

print(scrape())





