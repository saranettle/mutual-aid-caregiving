# Original UI design
# credit Prof. Danielle Safonte
# bsg_people_app
# https://github.com/osu-cs340-ecampus/flask-starter-app/tree/24f289773ee051ebb8c83822bd78441ccb1dad33/bsg_people_app

from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_xxxx'
app.config['MYSQL_PASSWORD'] = 'xxxx' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_xxxx'
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
        
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            neighborPhone = request.form["neighborPhone"]
            
            query = "INSERT INTO Neighbors (firstName, lastName, neighborPhone) VALUES (%s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (firstName, lastName, neighborPhone))
            mysql.connection.commit()
            return redirect("/neighbors")
        
    return render_template("add_neighbor.j2")

@app.route("/delete_neighbor/<int:neighborID>")
def delete_neighbor(neighborID):

    query = "DELETE FROM Neighbors WHERE NeighborID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (neighborID,))
    mysql.connection.commit()

    return redirect("/neighbors")


@app.route("/edit_neighbor/<int:neighborID>", methods=["POST", "GET"])
def edit_neighbor(neighborID):

    if request.method == "GET":
        query = "SELECT * FROM Neighbors WHERE neighborID = %s" % (neighborID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("edit_neighbor.j2", data=data)
    
    if request.method == "POST":

        # for editing the neighbor
        if request.form.get("edit_neighbor"):
            neighborID = request.form["neighborID"]
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            neighborPhone = request.form["neighborPhone"]

            query = "UPDATE Neighbors SET Neighbors.firstName = %s, Neighbors.lastName = %s, Neighbors.neighborPhone = %s WHERE Neighbors.neighborID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (firstName, lastName, neighborPhone, neighborID))
            mysql.connection.commit()

            return redirect("/neighbors")



# Listener
if __name__ == "__main__":

    #Start the app on port 3000, it will be different once hosted
    app.run(port=3000, debug=True)