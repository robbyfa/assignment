from flask import Flask, render_template, jsonify, request
import random
import os
from sqlalchemy import create_engine, Column, Integer, String, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_cors import CORS 

db_user = "rob"
db_pass = "uWzKUp8YtnLuRqJP/dbeZLdV"
db_name = "numbersdb"
db_socket_dir = "/cloudsql"
cloud_sql_instance_name = "cis3111-2023-class:europe-west1:db-instance"

# Create database engine
db_url = f"mysql+pymysql://{db_user}:{db_pass}@/{db_name}?unix_socket={db_socket_dir}"
engine = create_engine(db_url)

# Define your database model
Base = declarative_base()

class NumberEntry(Base):
    __tablename__ = "random_number_table"

    id = Column(Integer, primary_key=True)
    InstanceName = Column(String(255))
    randomNumber = Column(Integer)

# Create the table if it doesn't exist
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    home_page = 'Home Page'
    return render_template('index.html', home=home_page)

@app.route('/genNum', methods=['GET', 'POST'])
def genNumFunc():
    if request.method == 'GET':
        number = random.randint(0, 100000)
        name = os.environ.get('GAE_INSTANCE')
        entry = NumberEntry(InstanceName=name, randomNumber=number)
        
        # Insert the data into the table
        session = Session()
        session.add(entry)
        session.commit()
        session.close()
        
        message = {'name': name, 'number': number}
        return jsonify(message)

@app.route('/db')
def showdb():
    session = Session()
    allName = session.query(NumberEntry.InstanceName).distinct().all()
    allDetails = session.query(NumberEntry).all()
    maxNum = session.query(NumberEntry).order_by(NumberEntry.randomNumber.desc()).first()
    minNum = session.query(NumberEntry).order_by(NumberEntry.randomNumber.asc()).first()
    session.close()

    return render_template('dbans.html', InsName=allName, All=allDetails, Max=maxNum, Min=minNum)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)