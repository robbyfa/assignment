from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/proxy_genNum', methods=['GET', 'POST'])
def proxy_genNum():
    response = requests.get('https://api-dot-cis3111-2023-class.ew.r.appspot.com/genNum')
    return jsonify(response.json())

@app.route('/proxy_db')
def proxy_db():
    response = requests.get('https://api-dot-cis3111-2023-class.ew.r.appspot.com/db')
    return response.text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
