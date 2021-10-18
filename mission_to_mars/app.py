# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# Create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():
    # see if collection exists yet
    mars_data = mongo.db.mars.find()
    # check to see if any results are returned
    ret = list(mars_data)
    # If the collection was not found, do the scrape and upsert
    if len(ret)==0:
        mars_data = scrape_mars.scrape()
    else:
        mars_data = mongo.db.mars.find_one()

    # Return template and data
    return render_template("index.html", mars_data=mars_data)

# Route that will trigger scrape function
@app.route("/scrape")
def scrape():
    # Do the scraping
    mars_data = scrape_mars.scrape()   

    # Update the mongo database 
    mongo.db.mars.update(
             {},
             mars_data,
             upsert=True
             )
    
    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)