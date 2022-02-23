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

-- insert into Products
INSERT INTO Products (manufacturer_id, product_name, product_type, product_cost, product_description) 
VALUES (:input_manufacturer_id, :input_product_name, :input, product_type, :input_product_cost, :input_product_description);

-- insert into Orders
INSERT INTO Orders (manufacturer_id, shipper_id, time_placed, status, warehouse_id) 
VALUES (:input_manufacturer_id, :input_shipper_id, :input_time_placed, :input_status_from_dropdown, :input_warehouse_id);

-- associate a Product with an Order
INSERT INTO Ordered_Products (order_id, product_id, number_ordered, ordered_cost)
VALUES (:input_order_id, :input_product_id, :input_number_ordered, :input_ordered_cost);

-- update an Order's shipper_id, status, and warehouse_id based on the update Order form
UPDATE Orders SET shipper_id = :input_shipper_id, status= :input_status_from_dropdown, warehouse_id = :input_warehouse_id, WHERE id= :order_id_from_update;

-- delete a Product and also delete that product from any existing Orders containing it
DELETE FROM Products WHERE product_id = :selected_product_id
DELETE FROM Ordered_Products WHERE product_id = :selected_product_id

-- remove a Product from an Order
DELETE FROM Ordered_Products WHERE order_product_id = :selected_order_product_id
