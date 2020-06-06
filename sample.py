from flask import Flask,jsonify

app = Flask(__name__)

@app.route("/")
def hello():
    return jsonify({"op":'Hello world!'})

if __name__ == '__main__':
    app.run(debug=True)


# 1. Zceppa Hiring..!

# Package : 4.5

# Website: https://www.zceppa.com/

# Rounds 1: Task

# Here is a coding problem that we'd like you to solve. You can tackle it in Django or Flask (preferably, Flask) and MySQL DB. [Build a REST API, we don't expect a front end]

# If you can keep your version control history for us to look at too, that would be great.

# This is a simple news management portal so use the https://newsapi.org website to fetch the latest news.

# 1. Register for an API key in the mentioned site.
# 2. Choose some five categories of news available in the API.
# 3. Develop an Endpoint which will fetch the news using newsapi.org API and store it in our database MySQL. You need to create the table for news and categories to store the data.
    # Fetch the news only for the selected date. Date should be passed as Query Param.
    # Pull out the news only for the selected categories from step 2.
    # Fetch the author, title, description, 0published at and url image from the news API and store it in our database.
# 4. Develop an next end point which will fetch the news from our database based on selected date and category. If you do pagination that will be great
    # Date can be passed as date range like from and to date in API
    # Multi categories can be selected as filter
    # Can sort by published time
# Develop an End Point for us to test:

# 1. /api/fetch-news -> fetch the news for selected date & category and store it in our database.
# 2. /api/list-news -> returns all the news stored in our database based on filters applied
# 3. /api/categories -> returns all the categories of the news

# Timeline: The task must be submitted before Monday EOD. Those who can finish this before the timeline will have more consideration.
# You can submit your task to  anitha@guvi.in as CC. 

