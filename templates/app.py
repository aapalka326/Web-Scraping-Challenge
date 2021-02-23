# Create a route called /scrape that will import python file
# Referenced 12.3 activity #9 heavily
# flask_pymongo lets us search for elements with integrations and helpers. 

from flask import Flask, render_template, redirect
from flask_pymongo import pyMongo
# import our mars_scrape.py file
import mars_scrape

app = Flask(__name__)

# Use PyMongo to establish Mongo connection using database name
# Inline syntax
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

# Root Route to render index.html template
@app.route("/")
def index():
    # Find one record of data from the mongo database
    # This finds a collection from our database and renders the template
    # The render_template function looks for templates folder with our app.py file
    mars = mongo.db.mars.find_one()
    # Render template and data
    return render_template("index.html", mars=mars)

# Create /scrape route
# Scrapper calles the functions below
@app.route("/scrape")
def scrape():

    mars = mongo.db.mars
    mars_data = scrape_mars.scrape_all()
    # The update function updates everything for data that it finds--and upsert will not add it again if it already exists
    mars.update({}, mars_data, upsert=True)
    return "Yay Scraping successful!"


if __name__ == "__main__":
    app.run(debug=True)