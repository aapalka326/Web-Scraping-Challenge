# Part 2 - MongoDB and Flask Application
    # A. Use MongoDB with Flask templating to create a new HTML page that displays info scraped from URLs
        # Convert Jupyter notebook into Py script with scrape function that will execute scraping code and
        # return Python dictionary containing scraped data. This will help execute our BS stuff. 
    # Referenced videos and class activites 12.3 # "Mongo Scraping", # "Hockey Headers", and # Splinter

from splinter import Browser
import datetime
import pandas as pd
from bs4 import BeautifulSoup 
import requests
from webdriver_manager.chrome import ChromeDriverManager
# Initiate browser through chrome with splinter path
def init_browser():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path), headless=False)


# Scrape Nasa newsite and collect latest news title and paragraph text
# Assign to variables to reference later
def scrape():
    browser = init_browser()
    mars_dict = {}

    # Visit Mars news site
    news_url = 'http://mars.nasa.gov/news/'
    browser.visit(news_url)

    # Create bs object
    html = browser.html

    # Parse html with bs
    nasa_soup = BeautifulSoup(html, 'html.parser')

    # Collect latest news title
    news_title = nasa_soup.find("div", class_='content_title')

    # Collect latest paragraph text
    news_p = nasa_soup.find("div", class_='article_teaser_body')

    #################################################################
    # Visit URL for featured space image and navigate to find Featured Mars image 
    img_url = 'https://mars.nasa.gov/system/news_items/list_view_images/8860_25446_05_GuidedEntry-320.jpg'
    browser.visit(img_url)

    full_img = browser.find_by_id('full_image')
    browser.is_element_present_by_text('more info', wait_time= 2)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    ################################################################
    # Mars Facts 
    fact_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(fact_url)

    # Convert to DataFrame
    df = tables[0]
    df.head(10)

    # Rename Columns
    df.columns=['', 'Mars Facts']

    # Convert to html string
    html_table = df.to_html
  
    # Strip unwanted newlines to clean up table
    html_table.replace('\n', '')

    ################################################################
    # Hemispheres 
    # Obtain high resolution images for each of Mar's Hempispheres 
    # Save both image URL and title containing hemisphere name
    # Use py dict to store data using keys img_url and title
    # Append dictionary with image url string and hemi title to list

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find hemishperes image and title
    img_title = soup.find_all('div', class_="item")

    # Create empty list for hemisphere title and image URLs
    hemi_images = []
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    # Get list of browser hemispheres
    links = browser.find_by_css("a.product-item h3")

    # Loop through results
    for i in range(len(links)):
        hemisphere = {}
        
        # FInd elements on our page
        browser.find_by_css("a.product-item h3")[i].click()
        
        # Find our sample image tag
        # Pull href
        sample_elem = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
        
        # Get hemisphere title from page
        hemisphere['title'] = browser.find_by_css("h2.title").text
        
        # Append image objects to list
        hemi_images.append(hemisphere)

        # Append scrapes to mars_dict created at beginning of our code
        mars_dict = {
            "latest News Title": news_title,
            "Latest News Paragraph": news_p,
            "Full Image": full_img,
            "Mars Facts": html_table,
            "Hemispheres": hemi_images
        }
        
        browser.back()
        return mars_dict





