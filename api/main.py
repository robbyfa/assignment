from flask import Flask,render_template,jsonify,request
import random
import os
import mysql.connector
from mysql.connector.constants import ClientFlag


config = {
    'user': 'rob',
    'password': 'uWzKUp8YtnLuRqJP/dbeZLdV',
    'host': '34.77.136.123',
    'cloud_sql_instance_name': 'cis3111-2023-class:europe-west1:db-instance'
    
}
# #Setting the database we want to work in
config['database'] = 'numbersdb'  # add new database to config dict


# establish  connection
connection = mysql.connector.connect(**config)
cursor = connection.cursor()



# Creating the table
query1 = ("CREATE TABLE random_number_table (InstanceName VARCHAR(50) , randomNumber int UNSIGNED) ")
cursor.execute(query1)


# #Delete all rows in table
delete = "DELETE FROM random_number_table"
cursor.execute(delete)
connection.commit()


app = Flask(__name__)


@app.route("/")
def home():
    home_page = 'Home Page'
    return render_template('index.html', home=home_page)

nameList = []
numList = []
@app.route('/genNum', methods=['GET', 'POST'])
def genNumFunc():
    # #Setting the database we want to work in
    config['database'] = 'numbersdb'  # add new database to config dict
    # establish  connection
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

        # GET request
    if request.method == 'GET':
            number = random.randint(0, 100000)
            name = os.environ.get('GAE_INSTANCE')
            ins = "INSERT INTO random_number_table (InstanceName, randomNumber) VALUES (%s, %s)"
            values = (name, number)
            cursor.execute(ins, values)
            connection.commit()
            message = {'name': name,'number':number,}
            return jsonify(message)  # serialize and use JSON headers


@app.route('/db')
def showdb():
    # #Setting the database we want to work in
    config['database'] = 'numbersdb'  # add new database to config dict
    # establish  connection
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()


    query1 = ("SELECT DISTINCT InstanceName FROM random_number_table;")
    cursor.execute(query1)
    allName = cursor.fetchall()

    query2 = ("SELECT * FROM random_number_table")
    cursor.execute(query2)
    allDetails = cursor.fetchall()


    query3 = ("SELECT * FROM random_number_table WHERE randomNumber = (SELECT MAX(randomNumber) FROM random_number_table);")
    cursor.execute(query3)
    maxNum = cursor.fetchall()


    query4 = ("SELECT * FROM random_number_table WHERE randomNumber = (SELECT MIN(randomNumber) FROM random_number_table);")
    cursor.execute(query4)
    minNum = cursor.fetchall()


    return render_template('dbans.html',InsName = allName , All = allDetails, Max = maxNum ,Min = minNum)




connection.close()

if __name__ == '__main__':
        app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
