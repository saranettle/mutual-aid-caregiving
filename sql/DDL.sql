SET FOREIGN_KEY_CHECKS = 0;
SET AUTOCOMMIT = 0;

DROP TABLE IF EXISTS Visits;
DROP TABLE IF EXISTS VisitTypes;
DROP TABLE IF EXISTS Locations;
DROP TABLE IF EXISTS NeighborHasCertifications;
DROP TABLE IF EXISTS Certifications;
DROP TABLE IF EXISTS CommunityHasNeighbors;
DROP TABLE IF EXISTS Neighbors;
DROP TABLE IF EXISTS Communities;

--
-- TABLE CREATION
--

-- Create table for Communities
CREATE OR REPLACE TABLE Communities (
    communityID int(11) UNIQUE NOT NULL AUTO_INCREMENT,
    communityName varchar(50) NOT NULL,
    PRIMARY KEY(communityID)
);

-- Create table for Neighbors
CREATE OR REPLACE TABLE Neighbors (
    neighborID int(11) UNIQUE NOT NULL AUTO_INCREMENT,
    firstName varchar(50) NOT NULL,
    lastName varchar(50) NOT NULL,
    neighborPhone varchar(50) NOT NULL,
    CONSTRAINT full_name UNIQUE (firstName, lastName, neighborPhone),
    PRIMARY KEY(neighborID)
);

-- Create table for CommunityHasNeighbors (intersection table)
CREATE OR REPLACE TABLE CommunityHasNeighbors (
    communityHasNeighborID int(11) UNIQUE NOT NULL AUTO_INCREMENT,
    neighbor int(11) NOT NULL,
    community int(11) NOT NULL,
    CONSTRAINT FOREIGN KEY (neighbor)
    REFERENCES Neighbors(neighborID),
    CONSTRAINT FOREIGN KEY (community)
    REFERENCES Communities(communityID),
    PRIMARY KEY(communityHasNeighborID)
);

-- Create table for Certifications
CREATE OR REPLACE TABLE Certifications (
    certificationID int(11) UNIQUE NOT NULL AUTO_INCREMENT,
    certificationTitle varchar(50) UNIQUE NOT NULL,
    PRIMARY KEY (certificationID)
);

-- Create table for NeighborHasCertifications (intersection table)
CREATE OR REPLACE TABLE NeighborHasCertifications (
    neighborHasCertificationID int(11) UNIQUE NOT NULL AUTO_INCREMENT,
    neighbor int(11) NOT NULL,
    certification int(11) NOT NULL,
    CONSTRAINT FOREIGN KEY (neighbor)
    REFERENCES Neighbors(neighborID),
    CONSTRAINT FOREIGN KEY (certification)
    REFERENCES Certifications(certificationID),
    PRIMARY KEY (neighborHasCertificationID)
);

-- Create table for Locations
CREATE OR REPLACE TABLE Locations (
    locationID int(11) UNIQUE NOT NULL AUTO_INCREMENT,
    locationName varchar(50) UNIQUE NOT NULL,
    address1 varchar(50) NOT NULL,
    address2 varchar(50),
    locationCity varchar(50) NOT NULL,
    locationState varchar(50) NOT NULL,
    locationZip varchar(50) NOT NULL,
    community int(11) NOT NULL,
    CONSTRAINT FOREIGN KEY (community)
    REFERENCES Communities(communityID),
    PRIMARY KEY (locationID)
);

-- Create table for VisitTypes
CREATE OR REPLACE TABLE VisitTypes (
    visitTypeID int(11) UNIQUE NOT NULL AUTO_INCREMENT,
    typeName varchar(50) UNIQUE NOT NULL,
    typeDescription varchar(250) NOT NULL,
    PRIMARY KEY (visitTypeID)
);

-- Create table for Visits
CREATE OR REPLACE TABLE Visits (
    visitID int(11) UNIQUE NOT NULL AUTO_INCREMENT,
    neighbor int(11) NOT NULL,
    caregiver int(11) DEFAULT NULL,
    startTime datetime NOT NULL,
    durationHours int(11) NOT NULL,
    visitType int(11) NOT NULL,
    location int(11) NOT NULL,
    visitNotes varchar(250),
    fulfilled boolean NOT NULL DEFAULT FALSE,
    CONSTRAINT FOREIGN KEY (neighbor)
    REFERENCES Neighbors(neighborID),
    CONSTRAINT FOREIGN KEY (caregiver)
    REFERENCES Neighbors(neighborID),
    CONSTRAINT FOREIGN KEY (visitType)
    REFERENCES VisitTypes(visitTypeID),
    CONSTRAINT FOREIGN KEY (location)
    REFERENCES Locations(locationID),
    PRIMARY KEY (visitID)
);

--
-- INSERTING SAMPLE DATA
--

-- Insert into Communities
INSERT INTO Communities (communityName) VALUES
    ('North Bay Hills'),
    ('Vista Apartments'),
    ('Gooseberry Collective');

-- Insert into Neighbors
INSERT INTO Neighbors (firstName, lastName, neighborPhone) VALUES
    ('Zaina', 'Hopkins', '333-111-1111'),
    ('Lorna', 'McClain', '333-222-2222'),
    ('Mikolaj', 'Frye', '333-333-3333'),
    ('Aliza', 'Moran', '333-444-4444'),
    ('Kyron', 'Lewis', '333-555-5555'),
    ('Maksymilian', 'Davila', '333-666-6666'),
    ('Lowri', 'Dillon', '333-777-7777'),
    ('Beau', 'Mckee', '333-888-8888'),
    ('Jac', 'Shepherd', '333-999-9999'),
    ('Krishan', 'Newman', '333-123-4567');

-- Insert into CommunityHasNeighbors
INSERT INTO CommunityHasNeighbors (neighbor, community) VALUES
    (1, 1),
    (1, 2),
    (1, 3),
    (1, 4),
    (2, 4),
    (2, 5),
    (2, 6),
    (2, 7),
    (2, 8),
    (3, 8),
    (3, 9),
    (3, 10);

-- Insert into Certifications
INSERT INTO Certifications (certificationTitle) VALUES
    ('CPR Certified'),
    ('First Aid Certification'),
    ('Certified Nursing Assistant');

-- Insert into NeighborHasCertifications
INSERT INTO NeighborHasCertifications (neighbor, certification) VALUES
    (2, 1),
    (3, 1),
    (3, 2),
    (6, 1),
    (8, 1),
    (8, 3),
    (10, 3);

-- Insert into Locations
INSERT INTO Locations (locationName, address1, address2, locationCity, locationState, locationZip, community) VALUES
    ('Lorna''s House', '42 NW 4th Ave', NULL, 'Friendly City', 'GA', '30002', 1),
    ('Zaina''s House',	'50 NW 4th Ave', NULL, 'Friendly City', 'GA', '30002', 1),
    ('The Frye Residence', '73 NW 4th Ave', NULL, 'Friendly City', 'GA', '30002', 1),
    ('Friendly City Public Library', '15 Main St', NULL, 'Friendly City', 'GA', '30002', 2),
    ('Apartment 217', '55 MLK Rd', 'Apt 217', 'Friendly City', 'GA', '30002', 2),
    ('Apartment Community Room', '55 MLK Rd', NULL, 'Friendly City', 'GA', '30002',	2),
    ('Bayside Community Center', '33 River St', NULL, 'Friendly City', 'GA', '30002', 3),
    ('The Newman Residence', '112 SE 23rd Ave', NULL, 'Friendly City', 'GA', '30002', 3),
    ('Jac''s Townhome',	'103 SE 20th Ave', 'Unit B', 'Friendly City', 'GA', '30002', 3);

-- Insert into VisitTypes
INSERT INTO VisitTypes (typeName, typeDescription) VALUES
    ('Childcare', 'Babysitting children under 12'),
    ('Eldercare', 'Eldercare for adults who require living assistance');

-- Insert into Visits
INSERT INTO Visits (neighbor, caregiver, startTime, durationHours, visitType, location, visitNotes, fulfilled) VALUES
    (5, 8, '2023-02-12 09:00:00', 6, 1,	5, 'Babysitting my 2 kids!', TRUE),
    (2, 1,	'2023-02-14 15:00:00', 6, 2, 1,	'Can you take care of my elderly dad while I''m at work?', TRUE),
    (8, NULL, '2023-02-15 14:00:00', 4, 1, 6,	'Help watch my kid after school', FALSE),
    (10, NULL, '2023-02-17 10:00:00', 4, 2, 8, 'I need help with my Mom this weekend', FALSE),
    (5,	NULL, '2023-02-17 16:00:00', 6, 1, 5,	'Help babysit my 2 kids during my evening shift!', FALSE);

SET FOREIGN_KEY_CHECKS = 1;
COMMIT;