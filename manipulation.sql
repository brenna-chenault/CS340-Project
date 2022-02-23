--music band distributor
--database manipulation examples

-- populate tables on respective initial page laod
SELECT * FROM Manufacturers;
SELECT * FROM Shippers;
SELECT * FROM Warehouses;

-- get all states to populate Warehouses dropdown
SELECT state FROM Warehouses;

-- filtered select for Warehouses page from drop down
SELECT * FROM Warehouses WHERE state = :input_state;

-- insert into Shippers
INSERT INTO Shippers (shipper_name, shipper_account_num, shipper_contact_name, shipper_contact_email)
VALUES (:input_shipper_name, :input_shipper_account_num, :input_shipper_contact_name, :input_shipper_contact_email);

-- insert into Manufacturers
INSERT INTO Manufacturers (manufacturer_name, email, phone_number, street_address, city, state, zip) 
VALUES (:user_manufacturer_name, :input_email, :input_phone_number, :input_street_address, :input_city, :input_state, :input_zip);

-- insert into Warehouses
INSERT INTO Warehouses (street_address, city, state, zip) VALUES (:input_warehouse_address, :input_warehouse_city, :input_warehouse_state, :input_warehouse_zip);
