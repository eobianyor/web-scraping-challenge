from flask import Flask, render_template

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

# Create an instance of our Flask app.
app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Create a db
db = client.Mars_db
collection = db.Mars_info
# for debugging NOT to be used in production stuff
db.Mars_info.drop()
# Create a collection inside my db and insert stuff in it
db.Mars_info.insert_one(
    [
        {
            'news_title': news_title,
            'news_paragraph': news_para
        },
    ]
)

@app.route("/")
def index():
    listing_results = listings.find()
    return render_template("index.html", listing_results=listing_results)


@app.route("/Mars_scrape")
def Mars_scrape():
    final_mars_data = Final_scrape()
    mars.update(data)
# @app.route('/insert/<name>/<position>')
# def insert(name, position):
#     new_player =         {
#             'name': name,
#             'position': position
#     }
#     db.roster.insert_one(new_player)
#     return f"{name} has been inserted into the database."

if __name__ == "__main__":
    app.run(debug=True)
