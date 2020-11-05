from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import Mars_scrape
app = Flask(__name__)

# # Create a db
# db = client.Mars_db
# collection = db.Mars_info

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/Mars_db"
mongo = PyMongo(app)


@app.route("/")
def index():
    mars_results = mongo.db.Mars_info.find_one()
    return render_template("index.html", mars_results=mars_results)


@app.route("/scrape")
def scraper():
    mars = mongo.db.Mars_info
    marss_data = Mars_scrape.scrape_NASA_Mars()
    # print(marss_data) - To make sure you have a dictionary
    mars.update({}, marss_data, upsert=True)
    # Use Flask's redirect function to send us to a different route once this task has completed.
    return redirect("/")
    # return marss_data


if __name__ == "__main__":
    app.run(debug=True)
