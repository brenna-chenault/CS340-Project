--music band distributor
--database definitions 

-- remove old tables
DROP TABLE IF EXISTS `Ordered_Products`;
DROP TABLE IF EXISTS `Orders`;
DROP TABLE IF EXISTS `Products`;
DROP TABLE IF EXISTS `Warehouses`;
DROP TABLE IF EXISTS `Manufacturers`;
DROP TABLE IF EXISTS `Shippers`;

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

CREATE TABLE `Orders` (
    `order_id` int(11) NOT NULL AUTO_INCREMENT,
    `manufacturer_id` int(11) NOT NULL,
    `shipper_id` int(11),
    `time_placed` TIMESTAMP NOT NULL,
    `status` ENUM('placed', 'confirmed-unpaid', 'confirmed-paid', 'fulfilled-unpaid', 'fulfilled-paid') NOT NULL,
    `warehouse_id` int(11),

    PRIMARY KEY (`order_id`),
    CONSTRAINT `order_fk1` FOREIGN KEY (`manufacturer_id`) REFERENCES `Manufacturers` (`manufacturer_id`),
    CONSTRAINT `order_fk2` FOREIGN KEY (`shipper_id`) REFERENCES `Shippers` (`shipper_id`),
    CONSTRAINT `order_fk3` FOREIGN KEY (`warehouse_id`) REFERENCES `Warehouses` (`warehouse_id`)
);

CREATE TABLE `Products` (
    `product_id` int(11) NOT NULL AUTO_INCREMENT,
    `manufacturer_id` int(11) NOT NULL,
    `product_name` varchar(255) NOT NULL,
    `product_type` ENUM('skateboards', 'crutches', 'shirts') NOT NULL,
    `product_cost` int(11) NOT NULL,
    `product_description` varchar(255) NOT NULL,

    PRIMARY KEY (`product_id`),
    CONSTRAINT `product_fk1` FOREIGN KEY (`manufacturer_id`) REFERENCES `Manufacturers` (`manufacturer_id`)
);

-- DELETE from Products will cascade to Ordered_Products
CREATE TABLE `Ordered_Products` (
    `order_product_id` int(11) NOT NULL AUTO_INCREMENT,
    `order_id` int(11) NOT NULL,
    `product_id` int(11) NOT NULL,
    `number_ordered` int(11) NOT NULL,
    `ordered_cost` int(11) NOT NULL,

    PRIMARY KEY (`order_product_id`),
    CONSTRAINT `ordered_product_fk1` FOREIGN KEY (`order_id`) REFERENCES `Orders` (`order_id`),
    CONSTRAINT `ordered_product_fk2` FOREIGN KEY (`product_id`) REFERENCES `Products` (`product_id`) ON DELETE CASCADE
);


-- instert into tables
INSERT INTO Warehouses (street_address, city, state, zip) 
VALUES ('4390 Skateboard Lane', 'Houston', 'Texas', '77001'),
('201 Band Street', 'Seattle', 'Washington', '98101'),
('4543 Docks Ave', 'New York', 'New York', '10022');

INSERT INTO Manufacturers (manufacturer_name, email, phone_number, street_address, city, state, zip) 
VALUES ('Cool Wheelz Skateboards', 'info@coolwheelz.com', '999-999-9999', '201 Wheelz Circle', 'Los Angeles', 'California', '90001'),
('Just Shirtz', 'design@justshirtz.com', '888-888-8888', '101 Main Street', 'Cleveland', 'Ohio', '44101'),
('A+ Bulk Medical Supply Co.', 'office@aplusmeds.com', '777-777-7777', '345 Ouch Lane', 'Corvallis', 'Oregon', '97330');

INSERT INTO Shippers (shipper_name, shipper_account_num, shipper_contact_name, shipper_contact_email)
VALUES ('FedEx', '5346532', 'Jane Person', 'jane@fedex.com'),
('UPS', '234890-A32', 'John Person', 'jperson@ups.com'),
('DHL', '987235987', 'Some Name', 'some.name@DHL.com');

INSERT INTO Products (manufacturer_id, product_name, product_type, product_cost, product_description) 
VALUES (2, 'Sick Air Unisex Tee', 'shirts', 24.99, 'blue tee with coughing skater sizes S-3XL'),
(1, 'Radtronic 1800z', 'skateboards', 493.52, 'can''t do ollies'),
(3, 'Sensible Titanium Crutches', 'crutches', 50000.01, 'FSA eligible');

INSERT INTO Orders (manufacturer_id, shipper_id, time_placed, status, warehouse_id) 
VALUES (2, NULL, '2022-02-01 23:19:11',	'confirmed-paid', NULL),
(1, 1, '2002-01-01 13:15:15', 'confirmed-unpaid',	NULL),
(3, 3, '2037-07-04 17:56:09', 'placed', 2);

INSERT INTO Ordered_Products (order_id, product_id, number_ordered, ordered_cost)
VALUES (1, 2, 465, 11620.35),
(3, 1, 8, 3948.16),
(2, 3, 19455, 972750194.55);
