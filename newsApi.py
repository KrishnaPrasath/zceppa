from flask import Flask,jsonify,request
import requests
#news api key 1af997e5c92047d589ebdf65480ed4b5

app = Flask(__name__)

@app.route("/",methods=["GET","POST"])
def get_news():
    if(request.method=='GET'):
        content = requests.get("http://newsapi.org/v2/everything?q=trump&from=2020-06-01&to=2020-06-01&apiKey=1af997e5c92047d589ebdf65480ed4b5")
        parsed_content = content.json()
        return jsonify({"content":parsed_content})
    else:
        return jsonify({"type":"post"})





if (__name__ == '__main__'):
    app.run(debug=True)