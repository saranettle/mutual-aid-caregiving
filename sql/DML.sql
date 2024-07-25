-- Schema has 8 Tables and there are 8 Forms implemented with CRUD statements for each form:
-- 1 Neighbors
-- 2 Locations
-- 3 Communities
-- 4 Visits
-- 5 Certifications
-- 6 Visit Types
-- 7 Certify Neighbors
-- 8 Community Neighbors

----------------------------------------- 1 -----------------------------------------------------------
-- Neighbors Form DML
-- get all Neighbor's data to browse all Neighbors
SELECT neighborID, firstName, lastName, neighborPhone
FROM Neighbors
ORDER BY neighborID;

-- add a new Neighbor
INSERT INTO Neighbors (firstName, lastName, neighborPhne)
VALUES (:firstNameInsert, :lastNameInsert, :neighborPhoneInsert);

-- get a single Neighbor's data for the Update Neighbor form
SELECT neighborID, firstName, lastName, neighborPhone
FROM Neighbors
WHERE neighborID = :neighborIDSelected;

-- update a Neighbor's data based on submission of the Update Neighbor page
UPDATE Neighbor
SET firstName = :firstNameUpdate, lastName = :lastNameUpdate, neighborPhone = :neighborPhoneUpdate
WHERE neighborID = :neighborIDUpdate;

-- get a single Neighbor's data for the Delete Neighbor form
SELECT neighborID, firstName, lastName, neighborPhone
FROM Neighbors
WHERE neighborID = :neighborIDDelete;

-- delete a Neighbor from the Delete Neighbor Form
DELETE
FROM Neighbors
WHERE neighborID = :neighborIDDelete;


------------------------------------------ 2 ----------------------------------------------------------
-- Locations Form DML
-- get all Locations' data to browse all Locations
SELECT locationID, locationName, address1, address2, locationCity, locationState, locationZip, communityName
FROM Locations
INNER JOIN Communities ON communityID = community
ORDER BY locationID;

-- add a new Location
INSERT INTO Locations (locationName, address1, address2, locationCity, locationState, locationZip, communityID)
VALUES (:locationNameInsert, :locationaddress1Insert, :locationaddress2Insert, :locationCityInsert,
        :locationaStateInsert, :locationZipCodeInsert, :communityIDInsert);

-- get all Communities to populate a dropdown for associating with Locations on Add Location and Update Location forms
SELECT communityID, communityName
FROM Communities
ORDER BY communityID;

-- get a single Location's data for the Update Location form
SELECT locationID, locationName, address1, address2, locationCity, locationState, locationZip, communityName
FROM Locations
INNER JOIN Communities ON communityID = community
WHERE neighborID = :locationIDUpdate;

-- update a Location's data based on submission of the Update Location page
UPDATE Location
SET locationName = :locationNameUpdate,  address1 = :locationaddress1Update, address2 = :locationaddress2Update,
    locationCity = :locationCityUpdate, locationState = :locationStateUpdate, locationZip = :locationZipUpdate,
    communityID = :communityIDUpdate
WHERE neighborID = :locationIDUpdate;

-- get a single Location's data for the Delete Location form
SELECT locationID, locationName, address1, address2, locationCity, locationState, locationZip, communityName
FROM Locations
INNER JOIN Communities ON communityID = community
WHERE locationID = :locationIDDelete;

DELETE
FROM Locations
WHERE locationID = :locationIDDelete;


----------------------------------------- 3 -----------------------------------------------------------
-- Communities Form DML
-- get all Communities' data to browse all Communities
SELECT communityID, communityName
FROM Communities
ORDER BY communityID;

-- add a new Community
INSERT INTO Communities (communityName)
VALUES (:communityNameInsert);

-- get a single Community's data for the Update Community form
SELECT communityName
FROM Communities
WHERE communityID = :communityIDUpdate;

-- update a Community's data based on submission of the Update Communities page
UPDATE Communities
SET communityName = :communityNameUpdate
WHERE communityID= :communityIDUpdate;

-- get a single Community's data for the Delete Community form
SELECT communityName
FROM Communities
WHERE communityID = :communityIDDelete;

-- delete a Community from the Delete Community form
DELETE FROM Communities
WHERE communityID = :communityDelete;


---------------------------------------- 4 ------------------------------------------------------------
-- Visits Form DML
-- get all Visits' data to browse all Visits
SELECT visitID, CONCAT(carereceivers.firstName,' ',carereceivers.lastName) AS "neighbor",
       CONCAT(caregivers.firstName,' ',caregivers.lastName) AS "careGiverName",
       startTime, durationHours, typeName visitType, locationName  location, visitNotes, fulfilled
FROM Visits
INNER JOIN Neighbors AS carereceivers ON neighbor = carereceivers.neighborID
LEFT OUTER JOIN Neighbors AS caregivers ON caregiver = caregivers.neighborID
INNER JOIN Locations ON location = locationID
INNER JOIN VisitTypes ON visitTypeID = visitType
ORDER BY visitID;

-- get all Neighbors data to populate two different dropdowns for associating
-- caregivers and carereceivers with a Visit on the Add Visit Form
-- and on the Update Visit Form
SELECT neighborID, CONCAT(firstName,' ',lastName) AS "fullName"
FROM Neighbors
ORDER BY neighborID;

-- get all VisitTypes data to populate a dropdown for associating with a Visit on both
-- Add Visit Form and
-- Update Visit Form
SELECT visitTypeID, typeName
FROM VisitTypes
ORDER BY visitTypeID;

-- get all Locations data to populate a dropdown for associating with a Visit on both
-- Add Visit Form and
-- Update Visit Form
SELECT locationID, locationName
FROM Locations
ORDER BY locationID;

-- add a new Visit
INSERT INTO Visits (neighbor, caregiver, startTime, durationHours, visitType, location, visitNotes, fulfilled)
VALUES (:neighborIDInsert, :caregiverIDInsert, :startTimeInsert, :durationHoursInsert, :visitTypeInsert,
        :locationInsert, :visitNotesInsert, :fulfilledInsert);

-- select Visit for Update
SELECT CONCAT(carereceivers.firstName,' ',carereceivers.lastName) AS "neighbor",
       CONCAT(caregivers.firstName,' ',caregivers.lastName) AS "careGiverName",
       startTime, durationHours, typeName visitType, locationName  location, visitNotes, fulfilled
FROM Visits
INNER JOIN Neighbors AS carereceivers ON neighbor = carereceivers.neighborID
LEFT OUTER JOIN Neighbors AS caregivers ON caregiver = caregivers.neighborID
INNER JOIN Locations ON location = locationID
INNER JOIN VisitTypes ON visitTypeID = visitType
WHERE visitID = :visitIDUpdate;

-- update a Visit
UPDATE Visits
SET neighbor = :neighborIDUpdate, caregiver = :caregiverIDUpdate, startTime = :startTimeUpdate,
    durationHours = :durationHoursUpdate, visitType = :visitTypeUpdate, location = :locationUpdate,
    visitNotes = :visitNotesUpdate, fulfilled = :fulfilledUpdate
WHERE visitID = :visitIDUpdate;

-- select Visit for Delete
SELECT CONCAT(carereceivers.firstName,' ',carereceivers.lastName) AS "neighbor",
       CONCAT(caregivers.firstName,' ',caregivers.lastName) AS "careGiverName",
       startTime, durationHours, typeName visitType, locationName  location, visitNotes, fulfilled
FROM Visits
INNER JOIN Neighbors AS carereceivers ON neighbor = carereceivers.neighborID
LEFT OUTER JOIN Neighbors AS caregivers ON caregiver = caregivers.neighborID
INNER JOIN Locations ON location = locationID
INNER JOIN VisitTypes ON visitTypeID = visitType
WHERE visitID = :visitIDDelete;

-- delete a Visit
DELETE FROM Vists
WHERE visitID = :visitIDDelete;


----------------------------------------- 5 -----------------------------------------------------------
-- Certifications Form DML
-- get all certifications to browse
SELECT certificationID, certificationTitle
FROM Certifications;

-- add a new Certification
INSERT INTO Certifications (certificationTitle)
VALUES (:certificationTitleInsert);

-- get a single Certification's data for the Update Certifications form
SELECT certificationTitle
FROM Certifications
WHERE certificationID = :certificationIDUpdate;

-- update a Certification's data based on submission of the Update Certification page
UPDATE Certifications
SET certificationTitle = :certificationTitleUpdate
WHERE certificationID= :certificationIDUpdate;

-- get a single Certification's data for the Delete Certifications form
SELECT certificationTitle
FROM Certifications
WHERE certificationID = :certificationIDDelete;

-- delete a Certification from the Display Certification page
DELETE FROM Certifications
WHERE certificationID= :certificationIDDelete;


---------------------------------------- 6 ------------------------------------------------------------
-- Vist Types Form DML
-- get all VisitTypes data to browse
SELECT visitTypeID, typeName, typeDescription FROM VisitTypes;

-- add a new VisitType
INSERT INTO VisitType (typeName, typeDescription) VALUES (:typeNameInput, :typeDescriptionInput);

-- get a single VisitType's data for the Update Visit Types form
SELECT typeName, typeDescription FROM VisitTypes WHERE visitTypeID = :visitTypeIDUpdate;

-- update a VisitType's data based on submission of the Update Visit Types page
UPDATE VisitTypes
SET typeName = :communityNameInput, typeDescription = :typeDescriptionInput
WHERE visitTypeID= :visitTypeIDUpdate;

-- get a single VisitType's data for the Delete Visit Types form
SELECT typeName, typeDescription FROM VisitTypes WHERE visitTypeID = :visitTypeIDDelete;

-- delete a VistType from the Display Visit Types page
DELETE FROM VistType WHERE visitTypeID= :visitTypeIDDelete;


---------------------------------------- 7 ------------------------------------------------------------
-- Certify Neighbor Form DML
-- get all Neighbors with their current associated Certifications to browse
SELECT neighbor, certification, CONCAT(firstName,' ',lastName) AS name, neighborPhone, certificationTitle
FROM Neighbors
INNER JOIN NeighborHasCertifications ON neighborID = neighbor
INNER JOIN Certifications ON certificationID = certification
ORDER BY name, certificationTitle;

-- get all Neighbor's data to populate a dropdown for associating with a Certification
-- used on both
-- Add Certification to Neighbor form and
-- Update Neighbor Certification form
SELECT neighborID, firstName, lastName, neighborPhone
FROM Neighbors
ORDER BY neighborID;


-- get all Certifications to populate a dropdown for associating with Neighbors
-- used on both
-- Add Certification to Neighbor form and
-- Update Neighbor Certification form
SELECT certificationID, certificationTitle
FROM Certifications
ORDER BY certificationID;

-- associate a Neighbor with a Certification (M-to-M relationship addition) from
-- Add Certification to Neighbor page
INSERT INTO NeighborHasCertifications (neighbor, certification)
VALUES (:neighborFromCertify, :certificationFromCertify);

-- select NeighborHasCertifications for Update
SELECT neighbor, certification
FROM NeighborHasCertifications
WHERE neighborHasCertificationID = :neighborHasCertificationIDUpdate;

UPDATE NeighborHasCertifications
SET neighbor = :neighborUpdate and certification = :certificationUpdate
WHERE neighborHasCertificationID = :neighborHasCertificationIDUpdate;

-- select NeighborHasCertifications for Delete
SELECT neighbor, certification
FROM NeighborHasCertifications
WHERE neighborHasCertificationID = :neighborHasCertificationIDDelete;

-- dis-associate a Certification from a Neighbor (M-to-M relationship deletion)
DELETE FROM NeighborHasCertifications
WHERE neighborHasCertificationID = :neighborHasCertificationIDDelete;


-------------------------------------- 8 --------------------------------------------------------------
-- Community Neighbors Form DML
-- get all Neighbors with their current associated Communities to browse
SELECT communityName as community, CONCAT(firstName,' ',lastName) AS neighbor
FROM CommunityHasNeighbors
INNER JOIN Neighbors ON Neighbors.neighborID = CommunityHasNeighbors.neighbor
INNER JOIN Communities ON Communities.communityID = CommunityHasNeighbors.community
ORDER BY communityName;

-- get all Neighbor's data to populate a dropdown on  for associating with a Community on both
-- Add Community to Neighbor Form and
-- Update Community Neighbor Form
SELECT neighborID, firstName, lastName, neighborPhone
FROM Neighbors
ORDER BY neighborID;

-- get all Communities to populate a dropdown for associating with Neighbors on both
-- -- Add Community to Neighbor Form and
-- -- Update Community Neighbor Form
SELECT communityID, communityName
FROM Communities
ORDER BY communityID;

-- associate a Neighbor with a Community (M-to-M relationship addition) on
-- Add Community to Neighbor form
INSERT INTO CommunityHasNeighbors (neighbor, community)
VALUES (:neighborSelected, :commuitySelected);

-- get a single Community/Neighbor association for the Update Neighbor Community form
SELECT communityHasNeighborID
FROM CommunityHasNeighbors
WHERE community = :communityIDUpdate and neighbor = :neighborUpdate;

-- update a single Community/Neighbor association from the Update Neighbor Community form
UPDATE CommunityHasNeighbors
SET community = :communityIDUpdate and neighbor = :neighborUpdate
WHERE communityHasNeighborID = :communityHasNeighborIDUpdate;

-- get a single Community/Neighbor association for the Delete Neighbor Community form
SELECT communityHasNeighborID
FROM CommunityHasNeighbors
WHERE community = :communityIDDelete and neighbor = :neighborDelete;

-- Delete a Community from a Neighbor (M-to-M relationship deletion)
DELETE FROM CommunityHasNeighbors
WHERE communityHasNeighborID = :communityHasNeighborIDDelete;
