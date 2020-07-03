from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import requests

# path to chromedriver 
def init_browser(): 
    executable_path = {'executable_path':r'C:\Users\dofwj\Desktop\web-scraping-challenge\Mission_to_Mars\chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    listings = {}
 
    #Visit Mars News url
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    time.sleep(1)
    html = browser.html
    soup = bs(html, "html.parser")
    news_title = soup.find('div', class_='image_and_description_container').find('div', class_='content_title').get_text()
    news_paragraph = soup.find('div', class_='article_teaser_body').get_text()
    
    #Visit Mars News url
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(1)
    browser.click_link_by_partial_text('more info')

    html = browser.html
    img_soup = bs(html, "html.parser")
    
    #find path and make full path
    img_url_rel = img_soup.find('figure', class_='lede').find('img')['src']
    featured_image_url = "https://www.jpl.nasa.gov" + img_url_rel

    ## Mars Weather
    # weather url and html
    marsweather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(marsweather_url)
    weather_html = browser.html

    #get lastest tweet
    soup = bs(weather_html, 'html.parser')
    mars_weather = soup.find('div', attrs={"data-testid": "tweet"}).get_text()

    console.log(mars_weather)

    # # Mars Facts
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)

    #get html
    facts_html = browser.html
    soup = bs(facts_html, 'html.parser')

    #get the entire table
    table_data = soup.find('table', class_="tablepress tablepress-id-mars")

    #find all instances of table row
    table_all = table_data.find_all('tr')

    #set up lists to hold td elements which alternate between label and value
    labels = []
    values = []

    #for each tr element append the first td element to labels and the second to values
    for tr in table_all:
        td_elements = tr.find_all('td')
        labels.append(td_elements[0].text)
        values.append(td_elements[1].text)
            
    #make a data frame
    mars_facts_df = pd.DataFrame({
        "Label": labels,
        "Values": values
    })

    # get html code for DataFrame
    fact_table = mars_facts_df.to_html(header = False, index = False, escape=False)
    fact_table


 

    #Hemisphere Images Scraping
    hemispheres_url ="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    hemispheres_html = browser.html
    soup = bs(hemispheres_html, 'html.parser')
    mars_hemispheres = soup.find_all('h3')
    hemisphere_image_urls = []
    #Loop to scrape all hemispheres
    for row in mars_hemispheres:
        title= row.text
        browser.click_link_by_partial_text(title)
        time.sleep(1)
        img_html = browser.html
        soup_h = bs(img_html, 'html.parser')
        img_url = soup_h.find('div',class_='downloads').a['href']
        print ("Hemisphere Name :  "+ str(title))
        print ("Hemisphere URL:  " + str(img_url))

        img_dict = {}
        img_dict['title']= title
        img_dict['img_url']= img_url
        hemisphere_image_urls.append(img_dict)
        browser.visit(hemispheres_url)

    listings = {
        "id": 1,
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image_url": featured_image_url,
        "mars_weather": mars_weather,
        "fact_table": fact_table,
        "hemisphere_images": hemisphere_image_urls
    }

    
    #browser.quit()
 
    return listings