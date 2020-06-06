from flask import Flask,jsonify,request,render_template
from flaskext.mysql import MySQL
import requests
import yaml
import json

db = yaml.load(open("db.yaml"))

app = Flask(__name__)

 
mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = db['mysql_user']
app.config['MYSQL_DATABASE_PASSWORD'] = db['mysql_pwd']
app.config['MYSQL_DATABASE_DB'] = db['mysql_db']
app.config['MYSQL_DATABASE_HOST'] = db['mysql_host']
mysql.init_app(app)

@app.route("/api/fetch-news/<string:category>/<string:fromDate>/<string:toDate>",methods=["GET"])
def list_category(category,fromDate,toDate):
    page_limit = 5
    result = []
    # parsed_content = "";
    for index in range(page_limit):
        content = requests.get("http://newsapi.org/v2/top-headlines?category="+category+"&from="+fromDate+"&to="+toDate+"&page="+str(index+1)+"&apiKey=1af997e5c92047d589ebdf65480ed4b5")
        parsed_content = content.json()
        result.append(parsed_content)
    return jsonify({"content":result})

@app.route('/')
def index():
    con = mysql.connect();
    cur = con.cursor()
    query = "SELECT * FROM user"
    result = cur.execute(query)
    if(result > 0):
        response = "data exist"
    else:
        response = "Table is empty"
    return render_template('./index.html')

@app.route("/api/fetch-news",methods=["GET","POST"])
def fetch():
    con = mysql.connect();
    cur = con.cursor()
    if(request.method == 'GET'):
        return render_template('index.html')
    else:
        requestData = request.form;
        category = {
            "0" : "business",
            "1" : "sports",
            "2" : "general",
            "3" : "entertainment",
            "4" : "health",
        }
        category_str = []
        
        for each in requestData:
            if(each == "0" or each == "1" or each == "2" or each == "3" or each == "4" ):
                # category_str.append()
                newsData = fetch_news(requestData[each],requestData["from"],requestData["to"]);
                print(len(newsData))
                if(check_table()):
                    for data in newsData:
                        if(len(data)>0):
                            update_table(data,cur,con,category[each])

                    # return jsonify({"result":each})
        # return jsonify({"result":newsData})
        cur.close()
        return jsonify({"result":newsData})
        # parsed_content = ""

        
def update_table(data,cur,con,category):
    page_limit = len(data)
    for index in range(page_limit):
        element = data[index]
        query = "INSERT INTO test VALUES(newsId,%s,%s,%s,%s,%s,%s,%s);"
        if(element["author"] != None):
            u_key = element["author"].replace(" ","")[:3] +"/"+str(element["title"].replace(" ",""))[:5]
        else:
            u_key = 'non' + "/"+str(element["title"].replace(" ",""))[:5]
        val = (element["author"],element["title"],element["description"],element["publishedAt"],element["urlToImage"],category, u_key)
        cur.execute(query,val)
    con.commit()

        

def check_table():
    con = mysql.connect()
    cur = con.cursor()
    tableName = 'News'
    table_check_query = "SELECT *  FROM information_schema.tables WHERE table_schema = 'NewsData' AND table_name = 'test_key' LIMIT 1;"
    table_exist = cur.execute(table_check_query)
    if(table_exist > 0):
        return True
    else:
        query = "CREATE TABLE test_key ( newsId INT NOT NULL AUTO_INCREMENT, author TINYTEXT , title TINYTEXT NOT NULL, description TEXT NOT NULL, pubAt VARCHAR(255) NOT NULL, urlImg TEXT , category VARCHAR(40) NOT NULL, u_key VARCHAR(40) NOT NULL,PRIMARY KEY(category), UNIQUE KEY (u_key), KEY (newsId));"
        cur.execute(query)
    return True
    # Fetch the author, title, description, 0published at and url image from the news API and store it in our database.
    

def fetch_news(q,fromDate,toDate):
    result = []
    page_limit = 5
    for index in range(page_limit):
        apiStr = "http://newsapi.org/v2/top-headlines?q="+q+"&from="+fromDate+"&to="+toDate+"&page="+str(index+1)+"&apiKey=1af997e5c92047d589ebdf65480ed4b5"
        content = requests.get(apiStr)
        parsed_content = content.json()
        result.append(parsed_content["articles"])
    # return jsonify({"res":result})
    return (result)

if(__name__ == '__main__'):
    app.run(debug=True)

