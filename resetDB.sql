DROP TABLE IF EXISTS addresses;

CREATE TABLE addresses (
    user TEXT NOT NULL PRIMARY KEY,
    source TEXT NOT NULL,
    destination TEXT NOT NULL, 
    isDriver INTEGER, 
    numAvailableSeats INTEGER 
);