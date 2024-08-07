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
app.config['MYSQL_USER'] = 'cs340_blumch'
app.config['MYSQL_PASSWORD'] = 'rxVlhZmxgVhD' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_blumch'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)


# Routes 

@app.route('/')
@app.route('/index.html')
@app.route('/index')
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


@app.route('/locations', methods=["POST", "GET"])
def locations():
    # grab all possible certifications
    if request.method == "GET":
        query = (" SELECT locationID, locationName, address1, address2, locationCity, locationState, "
                 " locationZip, communityName "
                 " FROM Locations "
                 " INNER JOIN Communities ON communityID = community "
                 " ORDER BY locationID;")
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # query for populating list of communities in dropdown
        query2 = "SELECT * FROM Communities ORDER BY communityID;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        community_data = cur.fetchall()
        return render_template("locations.j2", data=data, community_data=community_data)

    if request.method == "POST":
        locationName = request.form["locationName"]
        address1 = request.form["address1"]
        address2 = request.form["address2"]
        locationCity = request.form["locationCity"]
        locationState = request.form["locationState"]
        locationZip = request.form["locationZip"]
        communityID = request.form["communityID"]
        query = ("INSERT INTO Locations (locationName, address1, address2, locationCity, locationState, "
                 "locationZip, community) VALUES (%s, %s, %s, %s, %s, %s, %s)")
        cur = mysql.connection.cursor()
        cur.execute(query, (locationName, address1, address2, locationCity, locationState, locationZip, communityID))
        mysql.connection.commit()
        return redirect("/locations")


@app.route("/delete_location/<int:locationID>")
def delete_location(locationID):
    query = "DELETE FROM Locations WHERE locationID = %s" % (locationID)
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()
    return redirect("/locations")


@app.route('/edit_location/<int:locationID>', methods=["POST", "GET"])
def edit_location(locationID):
    if request.method == "GET":
        query = ("SELECT locationID, locationName, address1, address2, locationCity, locationState, "
                 " locationZip, community, communityName "
                 " FROM Locations "
                 " INNER JOIN Communities ON communityID = community "
                 " WHERE locationID = %s" % (locationID))
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        # query for populating list of communities in dropdown
        query2 = "SELECT * FROM Communities ORDER BY communityID;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        community_data = cur.fetchall()
        return render_template("edit_location.j2", data=data, community_data=community_data)

    if request.method == "POST":
        locationID = request.form["locationID"]
        locationName = request.form["locationName"]
        address1 = request.form["address1"]
        address2 = request.form["address2"]
        if address2 == 'None':
            address2 = ''
        locationCity = request.form["locationCity"]
        locationState = request.form["locationState"]
        locationZip = request.form["locationZip"]
        communityID = request.form["communityID"]
        query = ("UPDATE Locations SET "
                 "locationName = %s, "
                 "address1 = %s, "
                 "address2 = %s, "
                 "locationCity = %s, "
                 "locationState = %s, "
                 "locationZip = %s, "
                 "community = %s "
                 "WHERE locationID = %s")
        cur = mysql.connection.cursor()
        cur.execute(query, (locationName, address1, address2, locationCity, locationState, locationZip, communityID,
                            locationID))
        mysql.connection.commit()
        return redirect("/locations")


@app.route('/communities', methods=["POST", "GET"])
def communities():
    # grab all possible certifications
    if request.method == "GET":
        query = "SELECT * FROM Communities ORDER BY communityID;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("communities.j2", data=data)

    if request.method == "POST":
        communityName = request.form["communityName"]
        query = "INSERT INTO Communities (communityName) VALUES ('%s')" % communityName
        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
        return redirect("/communities")


@app.route("/delete_community/<int:communityID>")
def delete_community(communityID):
    query = "DELETE FROM Communities WHERE communityID = %s" % (communityID)
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()
    return redirect("/communities")


@app.route('/edit_community/<int:communityID>', methods=["POST", "GET"])
def edit_community(communityID):
    if request.method == "GET":
        query = "SELECT * FROM Communities WHERE communityID = %s" % (communityID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("edit_community.j2", data=data)

    if request.method == "POST":
        communityName = request.form["communityName"]
        communityID = request.form["communityID"]
        query = ("UPDATE Communities SET communityName = %s "
                 "WHERE communityID = %s")
        cur = mysql.connection.cursor()
        cur.execute(query, (communityName, communityID))
        mysql.connection.commit()
        return redirect("/communities")


@app.route('/certifications', methods=["POST", "GET"])
def certifications():
    # grab all possible certifications
    if request.method == "GET":
        query = "SELECT * FROM Certifications ORDER BY certificationID;"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("certifications.j2", data=data)

    if request.method == "POST":
        certificationTitle = request.form["certificationTitle"]
        query = "INSERT INTO Certifications (certificationTitle) VALUES ('%s')" % certificationTitle
        cur = mysql.connection.cursor()
        cur.execute(query)
        mysql.connection.commit()
        return redirect("/certifications")


@app.route("/delete_certification/<int:certificationID>")
def delete_certification(certificationID):
    query = "DELETE FROM Certifications WHERE certificationID = %s" % (certificationID)
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()
    return redirect("/certifications")


@app.route('/edit_certification/<int:certificationID>', methods=["POST", "GET"])
def edit_certification(certificationID):
    if request.method == "GET":
        query = "SELECT * FROM Certifications WHERE certificationID = %s" % (certificationID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
        return render_template("edit_certification.j2", data=data)

    if request.method == "POST":
        certificationTitle = request.form["certificationTitle"]
        certificationID = request.form["certificationID"]
        query = ("UPDATE Certifications SET certificationTitle = %s "
                 "WHERE certificationID = %s")
        cur = mysql.connection.cursor()
        cur.execute(query, (certificationTitle, certificationID))
        mysql.connection.commit()
        return redirect("/certifications")


@app.route('/certify_neighbors', methods=["POST", "GET"])
def certify_neighbors():
    # grab all possible certifications
    if request.method == "GET":
        query = ("SELECT neighborHasCertificationID, CONCAT(firstName,' ',lastName) AS neighbor, certificationTitle AS certification "
                 "FROM Neighbors INNER JOIN NeighborHasCertifications "
                 "ON neighborID = neighbor INNER JOIN Certifications ON certificationID = certification "
                 "ORDER BY neighbor, certificationTitle;")
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # get all Neighbors' data to populate a dropdown for associating with a Certification
        query2 = "SELECT neighborID, CONCAT(firstName,' ',lastName) AS name FROM Neighbors ORDER BY name;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        neighbors_data = cur.fetchall()

        # get all Certifications' data to populate a dropdown for associating with a Neighbor
        query3 = "SELECT certificationID, certificationTitle FROM Certifications ORDER BY certificationID;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        certifications_data = cur.fetchall()

        return render_template("certify_neighbors.j2", certify_neighbors=data, neighbors=neighbors_data,
                               certifications=certifications_data)

    if request.method == "POST":
        # fire off if user clicks the 'Edit Person' button
        if request.form.get("addNeighborCertificationBtn"):
            neighbor = request.form["neighbor"]
            certification = request.form["certification"]
            query = "INSERT INTO NeighborHasCertifications (neighbor, certification) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (neighbor, certification))
            mysql.connection.commit()
            return redirect("/certify_neighbors")


@app.route('/edit_certify_neighbors/<int:neighborHasCertificationID>', methods=["POST", "GET"])
def edit_certify_neighbors(neighborHasCertificationID):
    if request.method == "GET":
        query = "SELECT * FROM NeighborHasCertifications WHERE neighborHasCertificationID = %s" % (neighborHasCertificationID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # get all Neighbors' data to populate a dropdown for associating with a Certification
        query2 = "SELECT neighborID, CONCAT(firstName,' ',lastName) AS name FROM Neighbors ORDER BY name;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        neighbors_data = cur.fetchall()

        # get all Certifications' data to populate a dropdown for associating with a Neighbor
        query3 = "SELECT certificationID, certificationTitle FROM Certifications ORDER BY certificationID;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        certifications_data = cur.fetchall()

        return render_template("edit_certify_neighbors.j2", certify_neighbors=data, neighbors=neighbors_data,
                               certifications=certifications_data)

    if request.method == "POST":
        neighborHasCertificationID = request.form["neighborCertification"]
        neighbor = request.form["neighborUpdate"]
        certification = request.form["certificationUpdate"]

        query = ("UPDATE NeighborHasCertifications SET neighbor = %s, certification = %s "
                 "WHERE neighborHasCertificationID = %s")
        cur = mysql.connection.cursor()
        cur.execute(query, (neighbor, certification, neighborHasCertificationID))
        mysql.connection.commit()
        return redirect("/certify_neighbors")


@app.route("/delete_certify_neighbors/<int:neighborHasCertificationID>")
def delete_certify_neighbors(neighborHasCertificationID):
    query = "DELETE FROM NeighborHasCertifications WHERE neighborHasCertificationID = %s" % (neighborHasCertificationID)
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()
    return redirect("/certify_neighbors")


@app.route('/community_neighbors', methods=["POST", "GET"])
def community_neighbors():
    # grab all community neighbor relationships
    if request.method == "GET":
        query = ("SELECT "
                    "communityHasNeighborID, "
                    "communityName AS community, "
                    "CONCAT(firstName,' ',lastName) AS neighbor "
                 "FROM CommunityHasNeighbors "
                 "INNER JOIN Neighbors ON neighborID = neighbor "
                 "INNER JOIN Communities ON community = communityID "
                 "ORDER BY community, neighbor;")
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # get all Neighbors' data to populate a dropdown for associating with a Community
        query2 = "SELECT neighborID, CONCAT(firstName,' ',lastName) AS name FROM Neighbors ORDER BY name;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        neighbors_data = cur.fetchall()

        # get all Communities' data to populate a dropdown for associating with a Neighbor
        query3 = "SELECT communityID, communityName FROM Communities ORDER BY communityName;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        communities_data = cur.fetchall()

        return render_template("community_neighbors.j2", data=data, neighbors=neighbors_data,
                               communities=communities_data)

    if request.method == "POST":
        neighborID = request.form["neighborID"]
        communityID = request.form["communityID"]
        query = "INSERT INTO CommunityHasNeighbors (neighbor, community) VALUES (%s, %s)"
        cur = mysql.connection.cursor()
        cur.execute(query, (neighborID, communityID))
        mysql.connection.commit()
        return redirect("/community_neighbors")


@app.route('/edit_community_neighbors/<int:communityHasNeighborID>', methods=["POST", "GET"])
def edit_community_neighbors(communityHasNeighborID):
    if request.method == "GET":
        query = "SELECT * FROM CommunityHasNeighbors WHERE communityHasNeighborID = %s" % (communityHasNeighborID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # get all Neighbors' data to populate a dropdown for associating with a Community
        query2 = "SELECT neighborID, CONCAT(firstName,' ',lastName) AS name FROM Neighbors ORDER BY name;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        neighbors_data = cur.fetchall()

        # get all Communities' data to populate a dropdown for associating with a Neighbor
        query3 = "SELECT communityID, communityName FROM Communities ORDER BY communityID;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        communities_data = cur.fetchall()

        return render_template("edit_community_neighbors.j2", data=data, neighbors=neighbors_data,
                               communities=communities_data)

    if request.method == "POST":
        communityHasNeighborID = request.form["communityHasNeighborID"]
        neighborID = request.form["neighborID"]
        communityID = request.form["communityID"]

        query = ("UPDATE CommunityHasNeighbors SET neighbor = %s, community = %s "
                 "WHERE communityHasNeighborID = %s")
        cur = mysql.connection.cursor()
        cur.execute(query, (neighborID, communityID, communityHasNeighborID))
        mysql.connection.commit()
        return redirect("/community_neighbors")


@app.route("/delete_community_neighbors/<int:communityHasNeighborID>")
def delete_community_neighbors(communityHasNeighborID):
    query = "DELETE FROM CommunityHasNeighbors WHERE communityHasNeighborID = %s" % (communityHasNeighborID)
    cur = mysql.connection.cursor()
    cur.execute(query)
    mysql.connection.commit()
    return redirect("/community_neighbors")


@app.route('/about', methods=["GET"])
def about():
    # grab all possible certifications
    if request.method == "GET":
        return render_template("about.j2")


# Listener
if __name__ == "__main__":
    # Start the app on port 3000, it will be different once hosted
    app.run(port=3000, debug=True)