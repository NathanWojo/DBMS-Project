mysql <<EOFMYSQL
use nawojtow;

SET FOREIGN_KEY_CHECKS = 0;

DROP TABLE IF EXISTS SECTION;
DROP TABLE IF EXISTS PROFESSOR;
DROP TABLE IF EXISTS COURSE;
DROP TABLE IF EXISTS ROOM;
DROP TABLE IF EXISTS DEPT;
DROP TABLE IF EXISTS Bookstore;
DROP TABLE IF EXISTS Book;
DROP TABLE IF EXISTS Copy;
DROP TABLE IF EXISTS Purchase;
DROP TABLE IF EXISTS Plaza;
DROP TABLE IF EXISTS Driver;
DROP TABLE IF EXISTS Vehicle;
DROP TABLE IF EXISTS VehicleOwner;
DROP TABLE IF EXISTS Pass;

SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE Plaza (
    plazaNumber CHAR(4) PRIMARY KEY,
    state CHAR(2) NOT NULL
);

CREATE TABLE Driver (
    driverID CHAR(9) PRIMARY KEY,
    name CHAR(25) NOT NULL,
    age INT CHECK (age BETWEEN 15 AND 90)
);

CREATE TABLE Vehicle (
    licensePlate CHAR(6) PRIMARY KEY,
    make CHAR(20) NOT NULL,
    model CHAR(20) NOT NULL,
    axles INT CHECK (axles IN (2, 3))
);

CREATE TABLE VehicleOwner (
    licensePlate CHAR(6),
    driverID CHAR(9),
    PRIMARY KEY (licensePlate, driverID),
    FOREIGN KEY (licensePlate) REFERENCES Vehicle(licensePlate)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (driverID) REFERENCES Driver(driverID)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

CREATE TABLE Pass (
    passID INT PRIMARY KEY,
    licensePlate CHAR(6),
    driverID CHAR(9),
    plazaNumber CHAR(4),
    passDate DATE,
    passTime TIME,
    cost DECIMAL(4,2) CHECK (cost IN (3.99, 5.99)),
    FOREIGN KEY (licensePlate) REFERENCES Vehicle(licensePlate)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (driverID) REFERENCES Driver(driverID)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (plazaNumber) REFERENCES Plaza(plazaNumber)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
);

INSERT INTO Plaza (plazaNumber, state) VALUES
('A101', 'TX'),
('B202', 'CA'),
('C303', 'FL'),
('D404', 'NY'),
('E505', 'IL');

INSERT INTO Driver (driverID, name, age) VALUES
('D12345678', 'Alice Smith', 34),
('D23456789', 'Bob Johnson', 45),
('D34567890', 'Carlos Lopez', 28),
('D45678901', 'Diana Patel', 52),
('D56789012', 'Ethan Wong', 19);

INSERT INTO Vehicle (licensePlate, make, model, axles) VALUES
('TX1234', 'Toyota', 'Camry', 2),
('CA5678', 'Ford', 'F-150', 3),
('FL9988', 'Honda', 'Civic', 2),
('NY1122', 'Chevy', 'Silverado', 3),
('IL3344', 'Nissan', 'Altima', 2);

INSERT INTO VehicleOwner (licensePlate, driverID) VALUES
('TX1234', 'D12345678'),
('CA5678', 'D23456789'),
('FL9988', 'D34567890'),
('NY1122', 'D45678901'),
('IL3344', 'D56789012');

INSERT INTO Pass (passID, licensePlate, driverID, plazaNumber, passDate, passTime, cost) VALUES
(1, 'TX1234', 'D12345678', 'A101', '2025-03-10', '08:15:00', 3.99),
(2, 'CA5678', 'D23456789', 'B202', '2025-03-10', '09:20:00', 5.99),
(3, 'FL9988', 'D34567890', 'C303', '2025-03-11', '11:05:00', 3.99),
(4, 'NY1122', 'D45678901', 'D404', '2025-03-12', '15:45:00', 5.99),
(5, 'IL3344', 'D56789012', 'E505', '2025-03-12', '18:30:00', 3.99),
(6, 'CA5678', 'D23456789', 'A101', '2025-03-13', '07:10:00', 5.99),
(7, 'TX1234', 'D12345678', 'C303', '2025-03-14', '14:00:00', 3.99),
(8, 'NY1122', 'D45678901', 'B202', '2025-03-15', '10:25:00', 5.99);

EOFMYSQL