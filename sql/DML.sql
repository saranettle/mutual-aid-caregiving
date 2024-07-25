
-- Certifications-related DML
-- get a single Certification's data for the Update Certifications form
SELECT certificationID, certificationTitle FROM Certifications WHERE certificationID = :certificationIDSelected;

-- get all Neighbor's data to populate a dropdown for associating with a Certification
SELECT neighborID, firstName, lastName, neighborPhone FROM Neighbors;

-- get all Certifications to populate a dropdown for associating with Neighbors
SELECT certificationID, certificationTitle FROM Certifications;

-- add a new Certification
INSERT INTO Certifications (certificationTitle) VALUES (:certificationTitleInput);

-- associate a Neighbor with a Certification (M-to-M relationship addition) from Neighbor Certifications page
INSERT INTO NeighborHasCertifications (neighbor, certification) VALUES (:neighborFromCertify, :certificationFromCertify);

-- update a Certification's data based on submission of the Update Certification page
UPDATE Certifications SET certificationTitle = :certificationTitleInput WHERE certificationID= :certificationFromUpdate;

-- delete a Certification from the Display Certification page
DELETE FROM Certifications WHERE  certificationID= :certificationFromDelete;

-- dis-associate a Certification from a Neighbor (M-to-M relationship deletion)
DELETE FROM NeighborHasCertifications
WHERE neighbor = :neighborFromCertify AND certification = :certificationFromCertify;

-- get all Neighbors with their current associated Certifications to list
SELECT neighbor, certification, CONCAT(firstName,' ',lastName) AS name, neighborPhone, certificationTitle
FROM Neighbors
INNER JOIN NeighborHasCertifications ON neighborID = neighbor
INNER JOIN Certifications ON certificationID = certification
ORDER BY name, certificationTitle;


-- Communities-related DML
-- get a single Community's data for the Update Communities form
SELECT communityID, communityName FROM Communities WHERE communityID = :communityIDSelected;

-- get all Neighbor's data to populate a dropdown for associating with a Community
SELECT neighborID, firstName, lastName, neighborPhone FROM Neighbors;

-- get all Communities to populate a dropdown for associating with Neighbors
SELECT communityID, communityName FROM Communities;

-- add a new Communities
INSERT INTO Communities (communityName) VALUES (:communityNameInput);

-- associate a Neighbor with a Community (M-to-M relationship addition) from Community Neighbors page
INSERT INTO CommunityHasNeighbors (neighbor, community) VALUES (:neighborSelected, :commuitySelected);

-- update a Community's data based on submission of the Update Communities page
UPDATE Communities SET communityName = :communityNameInput WHERE communityID= :communityFromUpdate;

-- delete a Community from the Display Community page
DELETE FROM Communities WHERE  communityID= :communityFromDelete;

-- dis-associate a Certification from a Neighbor (M-to-M relationship deletion)
DELETE FROM CommunityHasNeighbors WHERE neighbor = :neighborSelected AND community = :commuitySelected;

-- get all Neighbors with their current associated Communities to list
SELECT neighbor, community, CONCAT(firstName,' ',lastName) AS name, neighborPhone, communityName
FROM Neighbors
INNER JOIN CommunityHasNeighbors ON neighborID = neighbor
INNER JOIN Communities ON communityID = community
ORDER BY name, communityName;


-- VistTypes-related DML
-- get a single VisitType's data for the Update Visit Types form
SELECT visitTypeID, typeName, typeDescription FROM VisitTypes WHERE visitTypeID = :visitTypeIDSelected;

-- get all VisitTypes data to populate a dropdown for associating with a Visit
SELECT visitTypeID, typeName, typeDescription FROM VisitTypes;

-- add a new VisitType
INSERT INTO VisitType (typeName, typeDescription) VALUES (:typeNameInput, :typeDescriptionInput);

-- update a VisitType's data based on submission of the Update Visit Types page
UPDATE VisitTypes SET typeName = :communityNameInput, typeDescription = :typeDescriptionInput
WHERE visitTypeID= :visitTypeIDFromUpdate;

-- delete a VistType from the Display Visit Types page
DELETE FROM VistType WHERE  isitTypeID= :visitTypeIDFromDelete;

-- get all Visits with their associated VisitTypes to list
SELECT CONCAT(caregivers.firstName,' ',caregivers.lastName) AS "careGiverName",
CONCAT(carereceivers.firstName,' ',carereceivers.lastName) AS "careReceiverName",
startTime, durationHours, locationName, visitNotes, fulfilled, typeName
FROM Visits
INNER JOIN Neighbors AS caregivers ON caregiver = caregivers.neighborID
INNER JOIN Neighbors AS carereceivers ON neighbor = carereceivers.neighborID
INNER JOIN Locations ON location = locationID
INNER JOIN VisitTypes ON visitTypeID = visitType
ORDER BY startTime DESC;
