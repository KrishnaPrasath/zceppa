from flask import Flask,jsonify,request,redirect
from flaskext.mysql import MySQL
import requests
import yaml
import json,re
import time,datetime,math

db = yaml.load(open("db.yaml"))

app = Flask(__name__)

 
mysql = MySQL()
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = db['mysql_user']
app.config['MYSQL_DATABASE_PASSWORD'] = db['mysql_pwd']
app.config['MYSQL_DATABASE_DB'] = db['mysql_db']
app.config['MYSQL_DATABASE_HOST'] = db['mysql_host']

try:
    mysql.init_app(app)
except:
    print("MySQL connection failed!")
@app.route("/api/fetch-news/<string:category>/<string:fromDate>/<string:toDate>",methods=["GET"])
def list_category(category,fromDate,toDate):
    page_limit = 5
    result = []
    for index in range(page_limit):
        content = requests.get("http://newsapi.org/v2/top-headlines?category="+category+"&from="+fromDate+"&to="+toDate+"&page="+str(index+1)+"&apiKey=1af997e5c92047d589ebdf65480ed4b5")
        
        parsed_content = content.json()
        result.append(parsed_content)
    return jsonify({"content":result})

@app.route('/')
def api_root():
    return jsonify({
        "Attention": "Avaiable api for the application",
        "For_Categories": "/categories",
        "To_Fetch-News": "/api/fetch-news?category={available-Category}&from={yyyy-mm-dd}&to={yyyy-mm-dd}",
        "To_List-News": "/api/list-news?category={available-Category}&from={yyyy-mm-dd}&to={yyyy-mm-dd}",
        "Z-Note": "Required params to be passed to get valid response"
    })

@app.route("/api/fetch-news",methods=["GET","POST"])
def fetch():
    con = mysql.connect();
    cur = con.cursor()
    category = request.args.get('category')
    fromDate = request.args.get('from')
    toDate = request.args.get('to')
    check_table()
    newsData = fetch_news(category,fromDate,toDate);
    for data in newsData:
        if(len(data)>0):
            update_table(data,cur,con,category)
    cur.close()
    return jsonify({
            "A-success": "News data successfully fetched",
            "content": newsData
        })


@app.route("/api/list-news",methods=["GET","POST"])
def fetch_list_news():
    con = mysql.connect();
    cur = con.cursor()
    category = request.args.get('category')
    fromDate = request.args.get('from')
    toDate = request.args.get('to')
    category_str = []
    result = list_news(cur,con,category,fromDate,toDate)
    return jsonify({ "newsData" : result })

@app.route("/api/categories",methods=["GET"])
def list_categories():
    con = mysql.connect();
    cur = con.cursor()
    if(request.method == 'GET'):
        result = fetch_categories(cur,con)
        return jsonify({"categories": result})
    


def fetch_categories(cur,con):
    query = "SELECT DISTINCT category FROM test_new ORDER BY category desc;"
    columns = cur.execute(query)
    if(columns>0):
        result = cur.fetchall()
    return result;

def list_news(cur,con,category,fromDate,toDate):
    from_stamp = time.mktime(datetime.datetime.strptime(fromDate, "%Y-%m-%d").timetuple())
    to_stamp = time.mktime(datetime.datetime.strptime(toDate, "%Y-%m-%d").timetuple())
    query = "SELECT * FROM test_new WHERE category = '"+category+"' AND pubAt BETWEEN '"+str(math.floor(from_stamp))+"' AND '"+str(math.floor(to_stamp))+"' ORDER BY pubAt desc;"
    final_res = []
    try:
        columns = cur.execute(query)
        if(columns>0):
            result = cur.fetchall()
            return result
    except:
        print("Error")


def update_table(data,cur,con,category):
    page_limit = len(data)
    for index in range(page_limit):
        element = data[index]
        query = "INSERT INTO test_new VALUES(%s,%s,%s,%s,%s,%s,%s);"
        if(element["author"] != None):
            u_key = element["author"].replace(" ","")[:3] +"/"+str(element["title"].replace(" ",""))[:5]
        else:
            u_key = 'non' + "/"+str(element["title"].replace(" ",""))[:5]
        key_list = ["author","title","description","publishedAt","urlToImage"];
        timestamp = time.mktime(datetime.datetime.strptime(element["publishedAt"][:10], "%Y-%m-%d").timetuple())
        for each in element:
            if(each in key_list and element[each]==None):
                element[each]="None"
        val = (""+element['author']+"",""+element['title']+"",""+element["description"]+"",""+str(math.floor(timestamp))+"",""+element["urlToImage"]+"",""+category+"",""+u_key+"")
        try:
            cur.execute(query,val)
        except:
            print(u_key)
    con.commit()

        

def check_table():
    con = mysql.connect()
    cur = con.cursor()
    tableName = 'News'
    table_check_query = "SELECT *  FROM information_schema.tables WHERE table_schema = 'NewsData' AND table_name = 'test_new' LIMIT 1;"
    table_exist = cur.execute(table_check_query)
    if(table_exist > 0):
        return True
    else:
        query = "CREATE TABLE test_new (  author TINYTEXT , title TINYTEXT NOT NULL, description TEXT NOT NULL, pubAt VARCHAR(255) NOT NULL, urlImg TEXT , category VARCHAR(40) NOT NULL, u_key VARCHAR(40) NOT NULL, UNIQUE KEY (u_key));"
        cur.execute(query)
    return True
    

def fetch_news(q,fromDate,toDate):
    result = []
    page_limit = 5
    for index in range(page_limit):
        apiStr = "http://newsapi.org/v2/top-headlines?q="+q+"&from="+fromDate+"&to="+toDate+"&page="+str(index+1)+"&apiKey=1af997e5c92047d589ebdf65480ed4b5"
        content = requests.get(apiStr)
        parsed_content = content.json()
        result.append(parsed_content["articles"])
    return (result)

if(__name__ == '__main__'):
    app.run(debug=True)

