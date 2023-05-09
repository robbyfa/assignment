from flask import Flask, render_template, jsonify, request
import random
import os
from sqlalchemy import create_engine, text

# Get environment variables
db_user = os.environ.get('DB_USER')
db_pass = os.environ.get('DB_PASSWORD')
db_name = os.environ.get('DB_NAME')
db_socket_dir = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

# Create database engine
db_url = f"mysql+pymysql://{db_user}:{db_pass}@/{db_name}?unix_socket={db_socket_dir}"
engine = create_engine(db_url)

# Creating the table
with engine.connect() as conn:
    conn.execute(text("CREATE TABLE IF NOT EXISTS random_number_table (InstanceName VARCHAR(50), randomNumber int UNSIGNED)"))

app = Flask(__name__)

@app.route("/")
def home():
    home_page = 'Home Page'
    return render_template('index.html', home=home_page)

@app.route('/genNum', methods=['GET', 'POST'])
def genNumFunc():
    if request.method == 'GET':
        number = random.randint(0, 100000)
        name = os.environ.get('GAE_INSTANCE')
        ins = text("INSERT INTO random_number_table (InstanceName, randomNumber) VALUES (:name, :number)")
        values = {'name': name, 'number': number}
        with engine.connect() as conn:
            conn.execute(ins, values)
        message = {'name': name, 'number': number}
        return jsonify(message)

@app.route('/db')
def showdb():
    with engine.connect() as conn:
        allName = conn.execute(text("SELECT DISTINCT InstanceName FROM random_number_table;")).fetchall()
        allDetails = conn.execute(text("SELECT * FROM random_number_table")).fetchall()
        maxNum = conn.execute(text("SELECT * FROM random_number_table WHERE randomNumber = (SELECT MAX(randomNumber) FROM random_number_table);")).fetchall()
        minNum = conn.execute(text("SELECT * FROM random_number_table WHERE randomNumber = (SELECT MIN(randomNumber) FROM random_number_table);")).fetchall()

    return render_template('dbans.html', InsName=allName, All=allDetails, Max=maxNum, Min=minNum)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
