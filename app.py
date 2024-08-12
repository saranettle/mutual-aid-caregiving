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
app.config['MYSQL_PASSWORD'] = 'rxVlhZmxgVhD'  # last 4 of onid
app.config['MYSQL_DB'] = 'cs340_blumch'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

# Routes 

# ------------------------------------------------------------------------------------------
# Main page: viewing visits, answering requests, and making a request, filtered by community
# ------------------------------------------------------------------------------------------
@app.route('/')
@app.route('/index.html')
@app.route('/index')
def root():
    
    if request.method == "GET":
        query = "SELECT communityID, communityName FROM Communities"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
    
        return render_template("main.j2", community_data=data)

@app.route("/view_community_visits_<int:communityID>", methods=["POST", "GET"])
def view_community_visits(communityID):

    if request.method == "GET":
        query = "SELECT * FROM Communities WHERE communityID = %s" % (communityID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # query 2 for the fulfilled visits

        query2 = "SELECT CONCAT(Neighbors.firstName, ' ', Neighbors.lastName) AS Neighbor, Visits.caregiver AS Caregiver, Locations.locationName AS Location, Visits.startTime AS Time, Visits.durationHours AS Hours, VisitTypes.typeName AS Category, Visits.visitNotes AS Notes FROM Visits INNER JOIN Locations ON Visits.location = Locations.locationID INNER JOIN Neighbors ON Visits.neighbor = Neighbors.neighborID INNER JOIN VisitTypes ON Visits.visitType = VisitTypes.visitTypeID INNER JOIN Communities on Locations.community = Communities.communityID WHERE Visits.fulfilled = 1 AND Communities.communityID = %s" % (communityID)
        cur = mysql.connection.cursor()
        cur.execute(query2)
        fulfilled_visit_data = cur.fetchall()

        # query 3 for the unfulfilled visits names
        query3 = "SELECT Visits.visitID, CONCAT(Neighbors.firstName, ' ', Neighbors.lastName) AS Neighbor, Locations.locationName AS Location, Visits.startTime AS Time, Visits.durationHours AS Hours, VisitTypes.typeName AS Category, Visits.visitNotes AS Notes FROM Visits INNER JOIN Locations ON Visits.location = Locations.locationID INNER JOIN Neighbors ON Visits.neighbor = Neighbors.neighborID INNER JOIN VisitTypes ON Visits.visitType = VisitTypes.visitTypeID INNER JOIN Communities on Locations.community = Communities.communityID WHERE Visits.fulfilled = 0 AND Communities.communityID = %s" % (communityID)
        cur = mysql.connection.cursor()
        cur.execute(query3)
        unfulfilled_visit_data = cur.fetchall()

        # query 4 for neighbor drop down
        query4 = "SELECT Neighbors.neighborID, CONCAT(Neighbors.firstName, ' ', Neighbors.lastName) AS neighborName FROM Neighbors INNER JOIN CommunityHasNeighbors ON Neighbors.neighborID = CommunityHasNeighbors.neighbor INNER JOIN Communities ON CommunityHasNeighbors.community = Communities.communityID WHERE Communities.communityID = %s" % (communityID)
        cur = mysql.connection.cursor()
        cur.execute(query4)
        neighbor_data = cur.fetchall()

        # query 5 for location drop down
        query5 = "SELECT Locations.locationID, Locations.locationName FROM Locations INNER JOIN Communities ON Locations.community = Communities.communityID WHERE Communities.communityID = %s" % (communityID)
        cur = mysql.connection.cursor()
        cur.execute(query5)
        location_data = cur.fetchall()

        # query 6 for visit_type drop down
        query6 = "SELECT VisitTypes.visitTypeID, VisitTypes.typeName FROM VisitTypes"
        cur = mysql.connection.cursor()
        cur.execute(query6)
        visit_type_data = cur.fetchall()

        return render_template("view_community_visits.j2", community_data=data, fulfilled_visits=fulfilled_visit_data, unfulfilled_visits= unfulfilled_visit_data, neighbors=neighbor_data, locations=location_data, visit_types=visit_type_data)
    
    if request.method == "POST":
        if request.form.get("request_visit"):
            neighborName = request.form["neighborName"]
            locationName = request.form["locationName"]
            startTime = request.form["startTime"]
            durationHours = request.form["durationHours"]
            visitType = request.form["visitType"]
            visitNotes = request.form["visitNotes"]
            query = "INSERT INTO Visits (neighbor, location, startTime, durationHours, visitType, visitNotes) VALUES (%s, %s, %s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (neighborName, locationName, startTime, durationHours, visitType, visitNotes))
            mysql.connection.commit()
            return redirect("/")
        
@app.route("/answer_request/<int:visitID>", methods=["POST", "GET"])
def answer_request(visitID):
    
    # query to pull info about visit based on visit ID
    if request.method == "GET":
        query = "SELECT Visits.visitID, CONCAT(Neighbors.firstName, ' ', Neighbors.lastName) AS Neighbor, Locations.locationName AS Location, Visits.startTime AS Time, Visits.durationHours AS Hours, VisitTypes.typeName AS Category, Visits.visitNotes AS Notes FROM Visits INNER JOIN Locations ON Visits.location = Locations.locationID INNER JOIN Neighbors ON Visits.neighbor = Neighbors.neighborID INNER JOIN VisitTypes ON Visits.visitType = VisitTypes.visitTypeID WHERE Visits.visitID =  %s" % (visitID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
    
        # query to pull neighbors for drop down
        query2 = "SELECT Neighbors.neighborID, CONCAT(Neighbors.firstName, ' ', Neighbors.lastName) AS neighborName FROM Neighbors INNER JOIN CommunityHasNeighbors ON Neighbors.neighborID = CommunityHasNeighbors.neighbor INNER JOIN Communities ON CommunityHasNeighbors.community = Communities.communityID INNER JOIN Locations ON Communities.communityID = Locations.community INNER JOIN Visits ON Locations.locationID = Visits.location WHERE Visits.visitID = %s" % (visitID)
        cur = mysql.connection.cursor()
        cur.execute(query2)
        neighbor_data = cur.fetchall()

        return render_template('/answer_request.j2', data=data, neighbors=neighbor_data)
    
    if request.method == "POST":
        if request.form.get("answer_request"):
            visitID = request.form["visitID"]
            neighborName = request.form["neighborName"]
            fulfilled = request.form["fulfilled"]
            
            query = ("UPDATE Visits SET Visits.caregiver = %s, Visits.fulfilled = %s WHERE Visits.visitID = %s")
            cur = mysql.connection.cursor()
            cur.execute(query, (neighborName, fulfilled, visitID))
            mysql.connection.commit()

            return redirect("/")

# ------------------------------------------------------------------------------------------
# Visits page: Viewing all visits, editing and deleting them (adding visits on Main page)
# ------------------------------------------------------------------------------------------
@app.route('/visits', methods=["GET"])
def visits():

    if request.method == "GET":
        query = "SELECT visitID, CONCAT(carereceivers.firstName,' ',carereceivers.lastName) AS \"Neighbor\", CONCAT(caregivers.firstName,' ',caregivers.lastName) AS \"careGiverName\", startTime, durationHours, typeName visitType, locationName location, visitNotes, fulfilled FROM Visits INNER JOIN Neighbors AS carereceivers ON neighbor = carereceivers.neighborID LEFT OUTER JOIN Neighbors AS caregivers ON caregiver = caregivers.neighborID INNER JOIN Locations ON location = locationID INNER JOIN VisitTypes ON visitTypeID = visitType ORDER BY visitID"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

    return render_template("visits.j2", data=data)

@app.route("/delete_visit/<int:visitID>")
def delete_visit(visitID):
    query = "DELETE FROM Visits WHERE visitID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (visitID,))
    mysql.connection.commit()

    return redirect("/visits")

@app.route("/edit_visit/<int:visitID>", methods=["POST", "GET"])
def edit_visit(visitID):
    if request.method == "GET":
        query = "SELECT visitID, Visits.neighbor AS neighborID, Locations.locationID AS locationID, CONCAT(carereceivers.firstName,' ',carereceivers.lastName) AS Neighbor, CONCAT(caregivers.firstName,' ',caregivers.lastName) AS \"careGiverName\", startTime, durationHours, typeName visitType, locationName location, visitNotes, fulfilled FROM Visits INNER JOIN Neighbors AS carereceivers ON neighbor = carereceivers.neighborID LEFT OUTER JOIN Neighbors AS caregivers ON caregiver = caregivers.neighborID INNER JOIN Locations ON location = locationID INNER JOIN VisitTypes ON visitTypeID = visitType WHERE visitID = %s" % (visitID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

    # query for visitTypes dropdown
        query2 = "SELECT VisitTypes.visitTypeID, VisitTypes.typeName FROM VisitTypes"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        visit_type_data = cur.fetchall()

    # query for locations dropdown
        query3 = "SELECT Locations.locationID, Locations.locationName FROM Locations"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        location_data = cur.fetchall()

    # query for neighbors dropdown
        query4 = "SELECT Neighbors.neighborID, CONCAT(Neighbors.firstName, ' ', Neighbors.lastName) AS neighborName FROM Neighbors"
        cur = mysql.connection.cursor()
        cur.execute(query4)
        neighbor_data = cur.fetchall()

        return render_template("edit_visit.j2", data=data, visit_types=visit_type_data, locations=location_data, neighbors=neighbor_data)
    
    # for the form submission
    if request.method == "POST":

        if request.form.get("edit_visit"):
            visitID = request.form["visitID"]
            neighbor = request.form["neighborName"]
            location = request.form["locationName"]
            startTime = request.form["startTime"]
            durationHours = request.form["durationHours"]
            visitType = request.form["visitType"]            

            query = "UPDATE Visits SET Visits.neighbor = %s, Visits.location = %s, Visits.startTime = %s, Visits.durationHours = %s, visitType = %s WHERE Visits.visitID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (neighbor, location, startTime, durationHours, visitType, visitID))
            mysql.connection.commit()

            return redirect("/visits")

# ------------------------------------------------------------------------------------------
# Visit Types page: Viewing all visit types, editing/deleting/adding
# ------------------------------------------------------------------------------------------
@app.route('/visit_types', methods=["GET"])
def visit_types():
    
    if request.method == "GET":
        query = "SELECT visitTypeID, typeName, typeDescription FROM VisitTypes ORDER BY visitTypeID"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()
    
    return render_template("visit_types.j2", data=data)

@app.route('/add_visit_type', methods=["GET", "POST"])
def add_visit_type():

    if request.method == "POST":

        if request.form.get("add_visit_type"):
            typeName = request.form["typeName"]
            typeDescription = request.form["typeDescription"]

            query = "INSERT INTO VisitTypes (typeName, typeDescription) VALUES (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (typeName, typeDescription))
            mysql.connection.commit()
            return redirect("/visit_types")

    return render_template("add_visit_type.j2")

@app.route("/delete_visit_type/<int:visitTypeID>")
def delete_visit_type(visitTypeID):

    query = "DELETE FROM VisitTypes WHERE visitTypeID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (visitTypeID,))
    mysql.connection.commit()

    return redirect("/visit_types")

@app.route("/edit_visit_type/<int:visitTypeID>", methods=["POST", "GET"])
def edit_visit_type(visitTypeID):

    if request.method == "GET":
        query = "SELECT * FROM VisitTypes WHERE visitTypeID = %s" % (visitTypeID)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("edit_visit_type.j2", data=data)

    if request.method == "POST":

        # for editing the visit type
        if request.form.get("edit_visit_type"):
            visitTypeID = request.form["visitTypeID"]
            typeName = request.form["typeName"]
            typeDescription = request.form["typeDescription"]

            query = "UPDATE VisitTypes SET VisitTypes.typeName = %s, VisitTypes.typeDescription = %s WHERE VisitTypes.visitTypeID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (typeName, typeDescription, visitTypeID))
            mysql.connection.commit()

            return redirect("/visit_types")

# ------------------------------------------------------------------------------------------
# Neighbors page: Viewing all neighbors, editing/deleting/adding
# ------------------------------------------------------------------------------------------
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

# ------------------------------------------------------------------------------------------
# Locations page: Viewing all locations, editing/deleting/adding
# ------------------------------------------------------------------------------------------
@app.route('/locations', methods=["POST", "GET"])
def locations():
    # grab all possible locations
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

# ------------------------------------------------------------------------------------------
# Communities page: Viewing all communities, editing/deleting/adding
# ------------------------------------------------------------------------------------------
@app.route('/communities', methods=["POST", "GET"])
def communities():
    # grab all possible communities
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

# ------------------------------------------------------------------------------------------
# Certifications page: Viewing all certifications, editing/deleting/adding
# ------------------------------------------------------------------------------------------
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

# ------------------------------------------------------------------------------------------
# Certify Neighbors page: Viewing all certification/neighbor relationships, editing/deleting/adding
# ------------------------------------------------------------------------------------------
@app.route('/certify_neighbors', methods=["POST", "GET"])
def certify_neighbors():
    # grab all possible certification/neighbor combos
    if request.method == "GET":
        query = (
            "SELECT neighborHasCertificationID, CONCAT(firstName,' ',lastName) AS neighbor, certificationTitle AS certification "
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
        query = "SELECT * FROM NeighborHasCertifications WHERE neighborHasCertificationID = %s" % (
            neighborHasCertificationID)
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

# ------------------------------------------------------------------------------------------
# Communities Neighbors page: Viewing all community/neighbor relationships, editing/deleting/adding
# ------------------------------------------------------------------------------------------
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

# ------------------------------------------------------------------------------------------
# About page: Static page
# ------------------------------------------------------------------------------------------
@app.route('/about', methods=["GET"])
def about():
    
    if request.method == "GET":
        return render_template("about.j2")


# ------------------------------------------------------------------------------------------
# Listener
# ------------------------------------------------------------------------------------------
if __name__ == "__main__":
    # Start the app on port 3000, it will be different once hosted
    app.run(port=31193, debug=True)

