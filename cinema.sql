
DROP DATABASE IF EXISTS cinema;

CREATE DATABASE cinema;

USE cinema;

CREATE TABLE Seats
            (seatNo VARCHAR(20) PRIMARY KEY NOT NULL,
             status VARCHAR(10) NOT NULL,
             price INTEGER NOT NULL);


CREATE TABLE Users(
             seatNo VARCHAR(20) NOT NULL,
             name VARCHAR(20) NOT NULL,
             gender VARCHAR(10) NOT NULL,
             phoneNo VARCHAR(50) NOT NULL,
             age INTEGER NOT NULL,
             PRIMARY KEY (seatNo),
             FOREIGN KEY (seatNo) REFERENCES Seats(seatNo)
);
