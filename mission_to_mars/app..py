# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

# Create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Find data
    mars_from_mongo = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars_data=mars_from_mongo)
    # return "Page Has loaded"


# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():
    mars_data=scrape_mars.scrape()    
    mongo.db.collection.update({}, mars_data, upsert=True)
    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)