from flask import Flask,jsonify,request
#news api key 1af997e5c92047d589ebdf65480ed4b5

app = Flask(__name__)

@app.route('/',methods = (["GET","POST"]))
def index():
    if(request.method == "POST"):
        some_json = request.get_json()
        
        return jsonify({"You Sent": some_json}),201
    else:
        return jsonify({"Greet": "Hello World!"})

@app.route('/multi/<int:num>',methods = ['GET'])
def get_multiply(num):
    return jsonify({'result':num*10})

if __name__ == '__main__':
    app.run(debug=True)