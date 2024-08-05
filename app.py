from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_nettles'
app.config['MYSQL_PASSWORD'] = '4130' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_nettles'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"


mysql = MySQL(app)


# Routes 

@app.route('/')
def root():
    return render_template("main.j2")

@app.route('/visits')
def visits():
    return render_template("visits.j2")

@app.route('/visit_types')
def visit_types():
    return render_template("visit_types.j2")


@app.route('/neighbors', methods=["GET"])
def neighbors():

    if request.method == "GET":
        query = "SELECT neighborID, firstName, lastName, neighborPhone FROM Neighbors ORDER BY neighborID"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

    return render_template("neighbors.j2", data=data)

@app.route('/add_neighbor', methods=["GET", "POST"])
def add_neighbor():

    if request.method == "POST":

        if request.form.get("add_neighbor"):
            # grab user form inputs
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            neighborPhone = request.form["neighborPhone"]
            
            query = "INSERT INTO Neighbors (firstName, lastName, neighborPhone) VALUES (%s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (firstName, lastName, neighborPhone))
            mysql.connection.commit()

    return render_template("add_neighbor.j2")

# Listener
if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    app.run(port=31193, debug=True)