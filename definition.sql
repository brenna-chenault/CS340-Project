--music band distributor
--database definitions 

-- create tables
CREATE TABLE `Warehouses` (
    `warehouse_id` int(11) AUTO_INCREMENT,
    `street_address` varchar(255) NOT NULL,
    `city` varchar(255) NOT NULL,
    `state` varchar(255) NOT NULL,
    `zip` varchar(255) NOT NULL,

    PRIMARY KEY (`warehouse_id`)
);

CREATE TABLE `Manufacturers` (
    `manufacturer_id` int(11) AUTO_INCREMENT,
    `manufacturer_name` varchar(255) NOT NULL,
    `email` varchar(255) NOT NULL,
    `phone_number` varchar(255) NOT NULL,
    `street_address` varchar(255) NOT NULL,
    `city` varchar(255) NOT NULL,
    `state` varchar(255) NOT NULL,
    `zip` varchar(255) NOT NULL,

    PRIMARY KEY (`manufacturer_id`)
);

CREATE TABLE `Shippers` (
    `shipper_id` int(11) AUTO_INCREMENT,
    `shipper_name` varchar(255) NOT NULL,
    `shipper_account_num` varchar(255) NOT NULL,
    `shipper_contact_name` varchar(255) NOT NULL,
    `shipper_contact_email` varchar(255) NOT NULL,

    PRIMARY KEY (`shipper_id`)
);

-- instert into tables
INSERT INTO Warehouses (street_address, city, state, zip) VALUES ('4390 Skateboard Lane', 'Houston', 'Texas', '77001');
INSERT INTO Warehouses (street_address, city, state, zip) VALUES ('201 Band Street', 'Seattle', 'Washington', '98101');
INSERT INTO Warehouses (street_address, city, state, zip) VALUES ('4543 Docks Ave', 'New York', 'New York', '10022');

INSERT INTO Manufacturers (manufacturer_name, email, phone_number, street_address, city, state, zip) 
VALUES ('Cool Wheelz Skateboards', 'info@coolwheelz.com', '999-999-9999', '201 Wheelz Circle', 'Los Angeles', 'California', '90001');
INSERT INTO Manufacturers (manufacturer_name, email, phone_number, street_address, city, state, zip) 
VALUES ('Just Shirtz', 'design@justshirtz.com', '888-888-8888', '101 Main Street', 'Cleveland', 'Ohio', '44101');
INSERT INTO Manufacturers (manufacturer_name, email, phone_number, street_address, city, state, zip) 
VALUES ('A+ Bulk Medical Supply Co.', 'office@aplusmeds.com', '777-777-7777', '345 Ouch Lane', 'Corvallis', 'Oregon', '97330');

INSERT INTO Shippers (shipper_name, shipper_account_num, shipper_contact_name, shipper_contact_email)
VALUES ('FedEx', '5346532', 'Jane Person', 'jane@fedex.com');
INSERT INTO Shippers (shipper_name, shipper_account_num, shipper_contact_name, shipper_contact_email)
VALUES ('UPS', '234890-A32', 'John Person', 'jperson@ups.com');
INSERT INTO Shippers (shipper_name, shipper_account_num, shipper_contact_name, shipper_contact_email)
VALUES ('DHL', '987235987', 'Some Name', 'some.name@DHL.com');
