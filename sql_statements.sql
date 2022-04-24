DROP database IF EXISTS `corona_archive`;

CREATE DATABASE `corona_archive`;

USE `corona_archive`;

CREATE TABLE Visitor (
    citizen_id INTEGER NOT NULL AUTO_INCREMENT,
    visitor_name CHAR(70),
    city CHAR(35),
    address VARCHAR(70),
    phone_number VARCHAR(20),
    email VARCHAR(64),
    device_id VARCHAR(70),
    infected BOOLEAN DEFAULT false,
    PRIMARY KEY (citizen_id)
);

CREATE TABLE PlaceOwner (
    place_id INTEGER NOT NULL AUTO_INCREMENT,
    place_name VARCHAR(70),
    phone_no VARCHAR(20),
    email VARCHAR(64),
    address VARCHAR(70),
    QRcode VARCHAR(70),
    PRIMARY KEY (place_id)
);

CREATE TABLE Agent (
    agent_id INTEGER NOT NULL AUTO_INCREMENT,
    username VARCHAR(20),
    password VARCHAR(70),
    PRIMARY KEY (agent_id)
);

CREATE TABLE Hospital (
    hospital_id INTEGER NOT NULL AUTO_INCREMENT,
    username VARCHAR(20),
    password VARCHAR(70),
    PRIMARY KEY (hospital_id)
);

CREATE TABLE VisitorToPlace(
    QRcode VARCHAR(70),
    device_id VARCHAR(70),
    entry_time DATETIME,
    exit_time DATETIME,
    PRIMARY KEY (QRcode, device_id, entry_time)
);

insert into
    Agent(username, password)
values
    ("testname", "testpassword");

insert into
    Hospital(username, password)
values
    ("testname", "testpassword");

-- for testing purposes
insert into 
    PlaceOwner(place_name, phone_no, email, address)
VALUES
    ('testplacename','651651651561', 'place@email.com', 'College Ring');