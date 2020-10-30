from flask import Flask, render_template

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo

# Create an instance of our Flask app.
app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)

# Create a db
db = client.Mars_db
# for debugging NOT to be used in production stuff
db.roster.drop()
# Create a collection inside my db and insert stuff in it
db.roster.insert_many(
    [
        {
            'news_title': news_title,
            'news_paragraph': news_para
        },
    ]
)

@app.route("/")
def home():
    players = list(db.roster.find())

    return render_template("index.html", players=players)

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
