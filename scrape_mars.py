from bs4 import BeautifulSoup as bs
from splinter import Browser
import time
import pandas as pd

def init_browser():
    executable_path = {"executable_path":"chromedriver"}
    browser = Browser("chrome", **executable_path, headless = False)
    

def scrape_info():
    browser = init_browser()
  
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    NASA_title = soup.find('div', 'content_title', 'a').text
    NASA_descrip = soup.find('div', 'rollover_description_inner').text



#JPL Mars Space Images - Featured Image
    executable_path = {"executable_path":"chromedriver"}
    browser = Browser("chrome", **executable_path, headless = False)
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(5)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(5)
    browser.click_link_by_partial_text('more info')
    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    results = soup.find('article')
    extension = results.find('figure', 'lede').a['href']
    featured_image_url = f'https://www.jpl.nasa.gov{extension}'


    #Mars Weather
    twitter_response = requests.get("https://twitter.com/marswxreport?lang=en")
    twitter_soup = BeautifulSoup(twitter_response.text, 'html.parser')
    tweet_containers = twitter_soup.find_all('div', class_="js-tweet-text-container")


    df = pd.read_html('http://space-facts.com/mars/', attrs = {'id': 'tablepress-mars'})[0]
    df = df.set_index(0).rename(columns={1:"value"})
    del df.index.name
    mars_facts = df.to_html()

    # Mars Hemispheres
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_hemisphere = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        mars_hemisphere.append({"title": title, "img_url": image_url})
    mars_hemisphere

    browser.quit()

