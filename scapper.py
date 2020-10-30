from flask import Flask, jsonify
from sqlalchemy import and_
import numpy as np
import pandas as pd
import datetime as dt
from datetime import datetime, timedelta
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from splinter import Browser
from bs4 import BeautifulSoup as bsoup
import requests
import pymongo
import datetime as dt
import time

# # reflect an existing database into a new model
# Base = automap_base()

# # reflect the tables
# Base.prepare(engine, reflect=True)

# # We can view all of the classes that automap found
# Base.classes.keys()

# # Save references to each table
# Measurements = Base.classes.measurement
# Station = Base.classes.station

# Measurements.__table__.columns.values()

# Station.__table__.columns.values()


app = Flask(__name__)

@app.route("/")
def index():
    return (
        f"<h1>Welcome! <br/><br/></h1>"
        f"Available Routes:<br/>"
        f"/api/v1.0/scrape_News_title<br/>"
        f"/api/v1.0/scrape_featured_image<br/>"
        f"/api/v1.0/scrape_mars_facts<br/>"
        f"/api/v1.0/scrape_Hemispheres<br/>"
        f"/api/v1.0/Final_scrape<br/>"
    )
@app.route("/api/v1.0/scrape_News_title")
def scrape_News_title():
    # session = Session(engine)
    # connection = engine.connect()
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    soup = bsoup(html,'html.parser')

    results = soup.select_one("ul.item_list li.slide")
    news_title = results.find("div", class_= "content_title").get_text()
    news_para = results.find('div', class_='article_teaser_body').get_text()

    # Create a dictionary for Flask
    NASA_News_dict = {}
    NASA_News_dict = {"news_title": news_title, "news_paragraph": news_para}
    # connection.close()
    # session.close()
    return jsonify(NASA_News_dict)

@app.route("/api/v1.0/scrape_featured_image")
def scrape_featured_image():
    # session = Session(engine)
    # connection = engine.connect()
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

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
    # connection.close()
    # session.close()
    return jsonify(NASA_image_dict)

@app.route("/api/v1.0/scrape_mars_facts")
def scrape_mars_facts():
    session = Session(engine)
    connection = engine.connect()
    # Design a query to show how many stations are available in this dataset?
    df = pd.read_html("https://space-facts.com/mars/")
    Mars_facts_df = df[0]
    NASA_Mars_html = Mars_facts_df.to_html
    connection.close()
    session.close()
    return jsonify(NASA_Mars_html)

@app.route("/api/v1.0/scrape_Hemispheres")
def scrape_Hemispheres():
    # session = Session(engine)
    # connection = engine.connect()
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    Hemisphere_List = ["Cerberus Hemisphere Enhanced", "Schiaparelli Hemisphere Enhanced", "Syrtis Major Hemisphere Enhanced", "Valles Marineris Hemisphere Enhanced"]
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
    # connection.close()
    # session.close()
    return jsonify(NASA_Mars_Hemisphere_Dict)

@app.route("/api/v1.0/Final_scrape")
def /api/v1.0/Final_scrape():
    Mars_data = {
        'Mars_News_title': NASA_News_dict['news_title'],
        'Mars_News_paragraph': NASA_News_dict['news_paragraph'],
        'Mars_featured_pics': NASA_image_dict,
        'Mars_facts_table': NASA_Mars_html,
        'Mars_hemisphere_pics': NASA_Mars_Hemisphere_Dict
    }

    return jsonify(Mars_data)
#     return "This is home. This is where the heart is"

# @app.route("/api/v1.0/<start>/<end>")
# def end():
#     return "This is home. This is where the heart is"

if __name__=="__main__":
    app.run(debug=True)