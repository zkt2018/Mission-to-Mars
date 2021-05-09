# Import flask to render a template, redirecting to another url, and creating a URL.
from flask import Flask, render_template, redirect, url_for
# Import PyMongo to interact with Mongo database
from flask_pymongo import PyMongo
# Convert from jupyter notebook to Python for scraping the code
import scraping

# Set up flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Tells Flask what to display when we're looking at the home page, index.html
@app.route("/")
def index():

    # uses PyMongo to find the "mars" collection in database
    # and assign that path to the mars variable
    mars = mongo.db.mars.find_one()
    # Tells Flask to return an HTML template using an index.html file,
    # to be created after building the Flask routes.
    # mars=mars to use the "mars" collection in MongoDB
    return render_template("index.html", mars=mars)

# Define the route that Flask will be using
@app.route("/scrape")
def scrape():
    # New variable that points to Mongo database
    mars = mongo.db.mars
    # Create a new variable to hold the newly scraped data
    # Reference the scrape_all function in the scraping.py file exported from Jupyter Notebook
    mars_data = scraping.scrape_all()
    # Update data
    mars.update({}, mars_data, upsert=True)
    # Navigate the page back to / where we can see the updated content
    return redirect('/', code=302)

# Run the code
if __name__ == "__main__":
   app.run()
