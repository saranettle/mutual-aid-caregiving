-- Visits page/Home Page --

-- Query for adding a row to the Visits table as a new request
INSERT INTO Visits (
    neighbor, 
    startTime, 
    durationHours, 
    visitType,
    location,
    visitNotes
    )
VALUES (
    (SELECT Neighbors.neighborID FROM Neighbors WHERE {inputted value}=Neighbors.firstName AND {inputted value}=Neighbors.lastName;),
    {inputted start time},
    {inputted integer},
    (SELECT VisitTypes.visitTypeID FROM VisitTypes WHERE {inputted value}=VisitTypes.typeName;),
    (SELECT Locations.locationID FROM Locations WHERE {inputted value}=Locations.locationName),
    {inputted visit notes}
)

-- Query for displaying unfulfilled visit requests
SELECT Communities.communityID, Neighbors.firstName, Neighbors.lastName, Locations.locationName, Visits.startTime, Visits.durationHours, VisitTypes.typeName, Visits.visitNotes, Visits.fulfilled
	FROM Visits
    INNER JOIN Locations ON Visits.location = Locations.locationID
    INNER JOIN Neighbors ON Visits.neighbor = Neighbors.neighborID
    INNER JOIN VisitTypes ON Visits.visitType = VisitTypes.visitTypeID
    INNER JOIN Communities on Locations.community = Communities.communityID
    WHERE Visits.fulfilled = False;
    -- to filter by Community, add another clause to WHERE statement:
    -- AND Communities.communityID = {value that was selected above}

-- Query for updating the Visits table (to fulfill a request)
UPDATE Visits SET fulfilled=true -- WHERE Visits.visitID={selected value}
UPDATE Visits SET caregiver={selected value} -- WHERE Visits.visitID={selected value}

-- Query for viewing past requests
-- First query is for getting the name of the caregiver
SELECT Visits.caregiver, Neighbors.firstName, Neighbors.lastName
	FROM Visits
    INNER JOIN Neighbors ON Visits.caregiver = Neighbors.neighborID;

-- second query is for displaying the rest of the visit information
SELECT Communities.communityID, Neighbors.firstName, Neighbors.lastName, Visits.caregiver, Locations.locationName, Visits.startTime, Visits.durationHours, VisitTypes.typeName, Visits.visitNotes, Visits.fulfilled
	FROM Visits
    INNER JOIN Locations ON Visits.location = Locations.locationID
    INNER JOIN Neighbors ON Visits.neighbor = Neighbors.neighborID
    INNER JOIN VisitTypes ON Visits.visitType = VisitTypes.visitTypeID
    INNER JOIN Communities on Locations.community = Communities.communityID
    WHERE Visits.fulfilled = True;