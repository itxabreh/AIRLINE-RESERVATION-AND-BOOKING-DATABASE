create database airline;

use airline;

CREATE TABLE FlightInformation 
(
    flight_id INT IDENTITY(1,1) PRIMARY KEY,
    airline_name VARCHAR(100),
    flight_number VARCHAR(20),
    departure_location VARCHAR(100),
    departure_date DATE,
    departure_time TIME,
    arrival_location VARCHAR(100),
    arrival_date DATE,
    arrival_time TIME,
    CONSTRAINT date_ch CHECK (departure_date < arrival_date),
	CONSTRAINT chk_arrival_time CHECK (arrival_time >= '00:00:00' AND arrival_time <= '23:59:59'),
	CONSTRAINT chk_departure_time CHECK (departure_time >= '00:00:00' AND departure_time <= '23:59:59')
);



CREATE TABLE FlightClass 
(
    flight_class_id INT IDENTITY(1,1) PRIMARY KEY,
    flight_id INT,
	class_type VARCHAR(255) NOT NULL,
    FOREIGN KEY (flight_id) REFERENCES FlightInformation(flight_id),
	CONSTRAINT CHK_ClassType CHECK (class_type IN ('Business', 'Economy', 'First Class'))
);


CREATE TABLE Price 
(
    flight_class_id INT,
    price money NOT NULL,
    effective_date DATE,
    FOREIGN KEY (flight_class_id) REFERENCES FlightClass(flight_class_id)
);


CREATE TABLE flightSeats (
    seat_id INT IDENTITY(1,1) PRIMARY KEY,
    flight_class_id INT,
    seat_number VARCHAR(10),
	flight_id INT,
    seat_status VARCHAR(20) CHECK (seat_status IN ('Available', 'Booked')),
    FOREIGN KEY (flight_class_id) REFERENCES FlightClass(flight_class_id),
	FOREIGN KEY (flight_id) REFERENCES FlightInformation(flight_id)

);


CREATE TABLE Passenger (
    passenger_id INT IDENTITY(1,1) PRIMARY KEY,
    full_name VARCHAR(100),
    identification_number VARCHAR(20),
    mobile_number VARCHAR(15),
    email VARCHAR(100),
    residential_address VARCHAR(255)
);

CREATE TABLE paymentStatus
(
    paymentStatusID INT IDENTITY(1,1) PRIMARY KEY,
    statusName VARCHAR(20) NOT NULL,
    CONSTRAINT CHK_PaymentStatusName CHECK (statusName IN ('Paid', 'Pending', 'Failed'))
);

CREATE TABLE Payment 
(
    payment_id INT IDENTITY(1,1) PRIMARY KEY,
	amount money,
    payment_date DATETIME,
	paymentStatusID INT,
    payment_method VARCHAR(50),
	FOREIGN KEY (paymentStatusID) REFERENCES paymentStatus(paymentStatusID)
);

CREATE TABLE reservationStatus (
    reservationStatusID INT IDENTITY(1,1) PRIMARY KEY,
    statusName VARCHAR(20) NOT NULL,
    CONSTRAINT CHK_StatusName CHECK (statusName IN ('Confirmed', 'Cancelled', 'Pending'))
);


CREATE TABLE Reservation
(
    reservation_id INT IDENTITY(1,1) PRIMARY KEY,
    passenger_id INT,
    seat_id INT,
    payment_id INT,
	reservationStatusID int,
    reservation_date DATETIME DEFAULT GETDATE(),
    FOREIGN KEY (passenger_id) REFERENCES Passenger(passenger_id),
    FOREIGN KEY (seat_id) REFERENCES flightSeats(seat_id),
	FOREIGN KEY (reservationStatusID) REFERENCES reservationStatus(reservationStatusID),
	FOREIGN KEY (payment_id) REFERENCES payment(payment_id),
);

create table bookingStatus
(
	bookingStatusID INT IDENTITY(1,1) PRIMARY KEY,
	statusName varchar(20) not null 
	CONSTRAINT CHK_BookingStatusName CHECK (statusName IN ('Booked', 'Canceled'))
);

CREATE TABLE Booking 
(
    booking_id INT IDENTITY(1,1) PRIMARY KEY,
	payment_id INT,
    booking_date DATETIME,
	bookingStatusID INT,
	FOREIGN KEY (bookingStatusID) REFERENCES bookingStatus(bookingStatusID),
	FOREIGN KEY (payment_id) REFERENCES payment(payment_id)

);

CREATE TABLE DenormalizedFlightInfo (
    flight_id INT,
    flight_number VARCHAR(20),
    airline_name VARCHAR(100),
    departure_location VARCHAR(100),
    departure_date DATE,
    departure_time TIME,
    arrival_location VARCHAR(100),
    arrival_date DATE,
    arrival_time TIME,
    class_type VARCHAR(255),
    price MONEY,
    seat_number VARCHAR(10),
    seat_status VARCHAR(20),
    PRIMARY KEY (flight_id, seat_number)  -- Considering seat_number for unique identification�per�flight
);
-- Audit table for Payment
CREATE TABLE PaymentAudit (
    audit_id INT IDENTITY(1,1) PRIMARY KEY,
    payment_id INT,
    amount money,
    payment_date DATETIME,
    paymentStatusID INT,
    payment_method VARCHAR(50),
    audit_action VARCHAR(20),
    audit_timestamp DATETIME DEFAULT GETDATE(),
    audit_user VARCHAR(100)
);

-- Trigger to capture changes in Payment table
CREATE TRIGGER tr_PaymentAudit
ON Payment
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    IF EXISTS(SELECT * FROM inserted)
    BEGIN
        INSERT INTO PaymentAudit (payment_id, amount, payment_date, paymentStatusID, payment_method, audit_action, audit_user)
        SELECT payment_id, amount, payment_date, paymentStatusID, payment_method, 'INSERT/UPDATE', SUSER_SNAME()
        FROM inserted;
    END
    ELSE
    BEGIN
        INSERT INTO PaymentAudit (payment_id, amount, payment_date, paymentStatusID, payment_method, audit_action, audit_user)
        SELECT payment_id, amount, payment_date, paymentStatusID, payment_method, 'DELETE', SUSER_SNAME()
        FROM deleted;
    END
END;
GO

-- Audit table for Booking
CREATE TABLE BookingAudit (
    audit_id INT IDENTITY(1,1) PRIMARY KEY,
    booking_id INT,
    payment_id INT,
    booking_date DATETIME,
    bookingStatusID INT,
    audit_action VARCHAR(20),
    audit_timestamp DATETIME DEFAULT GETDATE(),
    audit_user VARCHAR(100)
);

-- Trigger to capture changes in Booking table
CREATE TRIGGER tr_BookingAudit
ON Booking
AFTER INSERT, UPDATE, DELETE
AS
BEGIN
    IF EXISTS(SELECT * FROM inserted)
    BEGIN
        INSERT INTO BookingAudit (booking_id, payment_id, booking_date, bookingStatusID, audit_action, audit_user)
        SELECT booking_id, payment_id, booking_date, bookingStatusID, 'INSERT/UPDATE', SUSER_SNAME()
        FROM inserted;
    END
    ELSE
    BEGIN
        INSERT INTO BookingAudit (booking_id, payment_id, booking_date, bookingStatusID, audit_action, audit_user)
        SELECT booking_id, payment_id, booking_date, bookingStatusID, 'DELETE', SUSER_SNAME()
        FROM deleted;
    END
END;
GO


-- Inserting a record into the Payment table
INSERT INTO Payment (amount, payment_date, paymentStatusID, payment_method)
VALUES (100.00, '2023-03-13', 1, 'Credit Card');

-- Updating a record in the Booking table
UPDATE Booking
SET payment_id = 2, bookingStatusID = 2
WHERE booking_id = 3;

DELETE FROM Booking
WHERE booking_id = 2;

select * from PaymentAudit;
--denormalized table
--Report 1: Total Flights and Seats Count

CREATE PROCEDURE GetTotalFlightsAndSeatsCounts
AS
BEGIN
    SELECT 
        COUNT(DISTINCT flight_id) AS Total_Flights,
        COUNT(*) AS Total_Seats
    FROM 
        DenormalizedFlightInfo;
END;

exec GetTotalFlightsAndSeatsCounts;
--denormalized

CREATE PROCEDURE GetFlightDepartureAndArrivalDetails
AS
BEGIN
    SELECT 
        flight_number, departure_location, arrival_location
    FROM 
        DenormalizedFlightInfo;
END;

exec GetFlightDepartureAndArrivalDetails;

--Report 2: Available Seats 

CREATE PROCEDURE GetAvailableSeatsOverview
AS
BEGIN
    SELECT 
        flight_id, flight_number, departure_location, arrival_location,
        COUNT(*) AS Total_Seats,
        SUM(CASE WHEN seat_status = 'Available' THEN 1 ELSE 0 END) AS Available_Seats
    FROM 
        DenormalizedFlightInfo
    GROUP BY 
        flight_id, flight_number, departure_location, arrival_location;
END;

--Report 1: Flights with Class Information
CREATE PROCEDURE GetFlightClassDetailsWithPrice
AS
BEGIN
    SELECT 
        FI.airline_name, FI.departure_location, FI.arrival_location, FC.class_type, P.price
    FROM 
        FlightInformation FI
    INNER JOIN 
        FlightClass FC ON FI.flight_id = FC.flight_id
    INNER JOIN 
        Price P ON FC.flight_class_id = P.flight_class_id;
END;


EXEC GetFlightClassDetailsWithPrice;


--Report 2: Passenger Reservations with Payment Information

CREATE PROCEDURE GetPassengerReservationPaymentStatus
AS
BEGIN
    SELECT 
        P.full_name, R.reservation_date, PS.statusName AS Payment_Status
    FROM 
        Passenger P
    INNER JOIN 
        Reservation R ON P.passenger_id = R.passenger_id
    INNER JOIN 
        paymentStatus PS ON R.payment_id = PS.paymentStatusID;
END;
EXEC GetPassengerReservationPaymentStatus;

--Report 3: Booking Status with Payment Details

CREATE PROCEDURE GetBookingStatusWithPaymentDetails
AS
BEGIN
    SELECT 
        BS.statusName AS Booking_Status, P.amount, P.payment_date
    FROM 
        Booking B
    INNER JOIN 
        bookingStatus BS ON B.bookingStatusID = BS.bookingStatusID
    INNER JOIN 
        Payment P ON B.payment_id = P.payment_id;
END;
EXEC GetBookingStatusWithPaymentDetails;

--Report 4: Number of Reservations having reservation > 2 

CREATE PROCEDURE GetPassengersWithMultipleReservations
AS
BEGIN
    SELECT 
        P.full_name, COUNT(R.reservation_id) AS Reservation_Count
    FROM 
        Passenger P
    INNER JOIN 
        Reservation R ON P.passenger_id = R.passenger_id
    GROUP BY 
        P.full_name
    HAVING 
        COUNT(R.reservation_id) > 2;
END;

EXEC GetPassengersWithMultipleReservations;




--Report 6: Number of Seats Reserved per Flight Class

CREATE PROCEDURE GetReservedSeatsPerFlightClass
AS
BEGIN
    SELECT 
        FC.class_type, COUNT(R.seat_id) AS Reserved_Seats
    FROM 
        FlightClass FC
    INNER JOIN 
        flightSeats FS ON FC.flight_class_id = FS.flight_class_id
    INNER JOIN 
        Reservation R ON FS.seat_id = R.seat_id
    GROUP BY 
        FC.class_type;
END;

EXEC GetReservedSeatsPerFlightClass;

--Report 7: Flights by Specific Airlines and departure date

CREATE PROCEDURE GetFlightsBySpecificAirlinesAndLocations
AS
BEGIN
    SELECT 
        *
    FROM 
        FlightInformation
    WHERE 
         (airline_name = 'Japan Airlines' 
        OR airline_name = 'Royal Airlines' 
        OR airline_name = 'AirBlue'
        )
        AND departure_location = 'Japan'
        AND arrival_location = 'Qatar'
        AND departure_date = '2024-03-14' 
END;

EXEC GetFlightsBySpecificAirlinesAndLocations;

--Report 8: Flights by Specific Airlines and arrival date


CREATE PROCEDURE GetFlightsBySpecificAirlines
AS
BEGIN
    SELECT 
        *
    FROM 
        FlightInformation
    WHERE 
         (airline_name = 'PIA' 
        OR airline_name = 'Qatar Airways' 
        OR airline_name = 'AirAsia'
        )
        AND departure_location = 'India'
        AND arrival_location = 'Iraq'
        AND arrival_date = '2026-03-06'
END;

EXEC GetFlightsBySpecificAirlines;

--Report 5: Average Price per Airline
CREATE PROCEDURE GetAveragePricePerAirline
AS
BEGIN
    SELECT 
        FI.airline_name, AVG(PR.price) AS Average_Price
    FROM 
        FlightInformation FI
    INNER JOIN 
        FlightClass FC ON FI.flight_id = FC.flight_id
    INNER JOIN 
        Price PR ON FC.flight_class_id = PR.flight_class_id
    GROUP BY 
        FI.airline_name;
END;
exec GetAveragePricePerAirline;


--count of payment methods

CREATE PROCEDURE CountPaymentsByPaymentMethod
AS
BEGIN
    SELECT 
        payment_method AS Payment_Method,
        COUNT(payment_id) AS Payment_Count
    FROM 
        Payment
    WHERE 
        payment_method IN ('Credit Card', 'Debit Card', 'PayPal')
    GROUP BY 
        payment_method;
END;


exec CountPaymentsByPaymentMethod;



select * from FlightInformation;
select * from FlightClass;
select * from Price;
select * from flightSeats;
select * from Passenger;
select * from paymentStatus;
select * from Payment;
select * from reservationStatus;
select * from Reservation;
select * from bookingStatus;
select * from Booking;

select * from DenormalizedFlightInformation;




