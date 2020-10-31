from splinter import Browser
from bs4 import BeautifulSoup as bsoup
import pandas as pd
import datetime as dt
import time


def scrape_NASA_Mars():
    executable_path = {'executable_path': 'chromedriver.exe'}
    # browser = Browser('chrome', **executable_path, headless=False)

    # You can set headless to True if you don't want an actual browser opened up to do the scrapping
    browser = Browser('chrome', **executable_path, headless=True)

    # Define url and send browser to visit the url and take the html from the browser
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    soup = bsoup(html, 'html.parser')

    results = soup.find_all('div', class_="content_title")
    title = (results[1].get_text().strip())
    results = browser.find_by_css('div[class="article_teaser_body"]')
    paragraph = (results.text)

    # Create a dictionary for Flask
    NASA_News_dict = {}
    NASA_News_dict = {"news_title": title, "news_paragraph": paragraph}

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    browser.click_link_by_partial_text('FULL IMAGE')

    # Update the CURRENT html code in the browser
    html = browser.html
    img_soup = bsoup(html, 'html.parser')

    time.sleep(3)
    results2 = browser.find_by_css('img[class="fancybox-image"]').first
    # Create a dictionary for Flask
    NASA_image_dict = {}
    NASA_image_dict["featured_image"] = (results2['src'])

    # Scrape table off the url and into a df
    df = pd.read_html("https://space-facts.com/mars/")
    Mars_facts_df = df[0]
    # Get table as a html for route
    NASA_Mars_html = Mars_facts_df.to_html()
    # Get table as a dict for route
    NASA_Mars_dict = Mars_facts_df.to_dict()

    Hemisphere_List = ["Cerberus Hemisphere Enhanced", "Schiaparelli Hemisphere Enhanced",
                       "Syrtis Major Hemisphere Enhanced", "Valles Marineris Hemisphere Enhanced"]
    NASA_Mars_Hemisphere_Dict = {}
    base_url = "https://astrogeology.usgs.gov/"
    for Hemisphere in Hemisphere_List:
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        time.sleep(2)
        browser.visit(url)
        time.sleep(2)
        browser.click_link_by_partial_text(Hemisphere)
        time.sleep(2)
        browser.click_link_by_partial_text("Open")
        time.sleep(2)

        # Update the CURRENT html code in the browser
        html = browser.html
        img_soup = bsoup(html, 'html.parser')
        time.sleep(2)
        # results3 = img_soup.find("img", {"class_": "wide-image"})
        results3 = img_soup.find('img', class_='wide-image')
        final_url = f"https://astrogeology.usgs.gov/{results3['src']}"
        NASA_Mars_Hemisphere_Dict[Hemisphere] = final_url

    Mars_data = {
        'Mars_News_title': NASA_News_dict['news_title'],
        'Mars_News_paragraph': NASA_News_dict['news_paragraph'],
        'Mars_featured_pics': NASA_image_dict,
        'Mars_facts_table': NASA_Mars_html,
        'Mars_facts_Dict': NASA_Mars_dict,
        'Mars_hemisphere_pics': NASA_Mars_Hemisphere_Dict
    }

    return Mars_data


if __name__ == "__main__":
    Mars_data = scrape_NASA_Mars()
    print(Mars_data)
