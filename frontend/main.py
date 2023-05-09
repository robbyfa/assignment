from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/db')
def db_route():
    api_url = 'https://api-dot-cis3111-2023-class.ew.r.appspot.com/db'
    response = requests.get(api_url)
    
    if response.status_code == 200:
        return response.text
    else:
        return f"Error: {response.status_code}"

@app.route('/genNum')
def gen_num_route():
    api_url = 'https://api-dot-cis3111-2023-class.ew.r.appspot.com/genNum'
    response = requests.get(api_url)
    
    if response.status_code == 200:
        return response.text
    else:
        return f"Error: {response.status_code}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
