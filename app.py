from flask import Flask, render_template, redirect
from flask_mysqldb import MySQL
from flask import request

# Configuration
app = Flask(__name__)

# database connection - from template
app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_chenaulb"
app.config["MYSQL_PASSWORD"] = "7566"
app.config["MYSQL_DB"] = "cs340_chenaulb"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

## Routes 

# Homepage
@app.route('/index.html')
@app.route('/')
def root():
    return render_template("/index.j2")

# Orders
@app.route('/orders.html', methods=["POST", "GET"])
def orders():
    """ 
    Route for the Orders page. Has Create, Read, and Update functionality.
    """
    # Add or update an Order to the database 
    if request.method == "POST":                    
        if request.form.get("insert_order_submit"):
            manufacturer_id = request.form["manufacturer_id"]
            shipper_id = request.form["shipper_id"]
            time_placed = request.form["time_placed"]
            status = request.form["status"]
            warehouse_id = request.form["warehouse_id"]

            # NULL shipper_id AND warehouse_id
            if shipper_id == "" and warehouse_id == "":
                query = "INSERT INTO Orders (manufacturer_id, time_placed, status) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, [manufacturer_id, time_placed, status])
                mysql.connection.commit()

            # NULL shipper_id only
            elif shipper_id == "":
                query = "INSERT INTO Orders (manufacturer_id, time_placed, status, warehouse_id) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, [manufacturer_id, time_placed, status, warehouse_id])
                mysql.connection.commit()

            # NULL warehouse_id only
            elif warehouse_id == "":
                query = "INSERT INTO Orders (manufacturer_id, shipper_id, time_placed, status) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, [manufacturer_id, shipper_id, time_placed, status])
                mysql.connection.commit()

            # All input fields given
            else:
                query = "INSERT INTO Orders (manufacturer_id, shipper_id, time_placed, status, warehouse_id) VALUES (%s, %s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, [manufacturer_id, shipper_id, time_placed, status, warehouse_id])
                mysql.connection.commit()

        # Update data associated with the given order_id
        if request.form.get("update_order_submit"):
            order_id = request.form["update_order_id"]
            shipper_id = request.form["update_order_shipper_id"]
            status = request.form["update_order_status"]
            warehouse_id = request.form["update_order_warehouse_id"]

            query = "UPDATE Orders SET shipper_id = %s, status= %s, warehouse_id = %s, WHERE order_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, [order_id, shipper_id, status, warehouse_id])
            mysql.connection.commit()

        # redirect back to Orders page
        return redirect("/orders.html")

    # Get data to display in table and insert/update dropdowns
    if request.method == "GET":
        # Query to populate table
        query_table = "SELECT * FROM Orders"
        cur = mysql.connection.cursor()
        cur.execute(query_table)
        orders_table = cur.fetchall()

        # Query to fill update dropdown with order_id
        query_id_dropdown = "SELECT order_id FROM Orders"
        cur = mysql.connection.cursor()
        cur.execute(query_id_dropdown)
        order_nums = cur.fetchall()

        # Query to fill insert dropdown with manufacturer_id
        query_mid_dropdown = "SELECT manufacturer_id FROM Manufacturers"
        cur = mysql.connection.cursor()
        cur.execute(query_mid_dropdown)
        order_mid_dropdown = cur.fetchall()

        # Query to fill insert/update dropdown with shipper_id
        query_sid_dropdown = "SELECT shipper_id FROM Shippers"
        cur = mysql.connection.cursor()
        cur.execute(query_sid_dropdown)
        order_sid_dropdown = cur.fetchall()

        # Query to fill insert/update dropdown with warehouse_id
        query_wid_dropdown = "SELECT warehouse_id FROM Warehouses"
        cur = mysql.connection.cursor()
        cur.execute(query_wid_dropdown)
        order_wid_dropdown = cur.fetchall()

        # Render the Orders page with the fetched data
        return render_template("orders.j2", order_data = orders_table, order_nums = order_nums, 
                    order_mid_dropdown = order_mid_dropdown, order_sid_dropdown = order_sid_dropdown, order_wid_dropdown = order_wid_dropdown )

# Products
@app.route('/products.html', methods=["POST", "GET"])
def products():
    """ 
    Route for the Products page. Has Create, Read, and Delete functionality.
    """
    # Add or delete a Product
    if request.method == "POST":                    
        
        # Add form POST request
        if request.form.get("insert_product_submit"):
            manufacturer_id = request.form["manufacturer_id"]
            product_name = request.form["product_name"]
            product_type = request.form["product_type"]
            product_cost = request.form["product_cost"]
            product_description = request.form["product_description"]

            # No NULLable attributes
            query = "INSERT INTO Products (manufacturer_id, product_name, product_type, product_cost, product_description) VALUES (%s, %s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, [manufacturer_id, product_name, product_type, product_cost, product_description])
            mysql.connection.commit()

        # Delete form POST request
        if request.form.get("delete_product_submit"):
            product_id = request.form["product_id"]
            query = "DELETE FROM Products WHERE product_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, [product_id])
            mysql.connection.commit()

        # redirect back to Products page
        return redirect("/products.html")

    # Get data to display in table and delete dropdown
    if request.method == "GET":
        # Query to populate table
        query_table = "SELECT * FROM Products"
        cur = mysql.connection.cursor()
        cur.execute(query_table)
        prod_table = cur.fetchall()
    
        # Query to fill delete dropdown with product_id
        query_id_dropdown = "SELECT product_id FROM Products"
        cur = mysql.connection.cursor()
        cur.execute(query_id_dropdown)
        prod_nums = cur.fetchall()

        # Query to fill insert dropdown with manufacturer_id
        mid_dropdown = "SELECT manufacturer_id FROM Manufacturers"
        cur = mysql.connection.cursor()
        cur.execute(mid_dropdown)
        mid_dropdown = cur.fetchall()

        # Render the Products page with the fetched data
        return render_template("products.j2", prod_data = prod_table, prod_nums = prod_nums, mid_dropdown = mid_dropdown)

# Ordered_Products
@app.route('/ordered_products.html', methods=["POST", "GET"])
def ordered_products():
    """ 
    Route for the Ordered_Products page. Has Create, Read, and Delete functionality.
    """
    # Add or delete an Ordered_Product to the database 
    if request.method == "POST":

        # Add form POST request                 
        if request.form.get("insert_order_product_submit"):
            order_id = request.form["order_id"]
            product_id = request.form["product_id"]
            number_ordered = request.form["number_ordered"]
            ordered_cost = request.form["ordered_cost"]

            # No NULLable attributes
            query = "INSERT INTO Ordered_Products (order_id, product_id, number_ordered, ordered_cost) VALUES (%s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, [order_id, product_id, number_ordered, ordered_cost])
            mysql.connection.commit()

        # Delete form POST request
        if request.form.get("delete_order_product_submit"):
            order_product_id = request.form["order_product_id"]
            query = "DELETE FROM Ordered_Products WHERE order_product_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, [order_product_id])
            mysql.connection.commit()

        # redirect back to Ordered_Products page
        return redirect("/ordered_products.html")

    # Get data to display in table and delete dropdown
    if request.method == "GET":
        # Query to populate table
        query_table = "SELECT * FROM Ordered_Products"
        cur = mysql.connection.cursor()
        cur.execute(query_table)
        order_prod_table = cur.fetchall()
    
        # Query to fill delete dropdown with order_product_id
        query_id_dropdown = "SELECT order_product_id FROM Ordered_Products"
        cur = mysql.connection.cursor()
        cur.execute(query_id_dropdown)
        order_prod_nums = cur.fetchall()

        # Query to fill insert dropdown with order_id
        ord_id_dropdown = "SELECT order_id FROM Orders"
        cur = mysql.connection.cursor()
        cur.execute(ord_id_dropdown)
        oid_dropdown = cur.fetchall()

        # Query to fill insert dropdown with product_id
        prod_id_dropdown = "SELECT product_id FROM Products"
        cur = mysql.connection.cursor()
        cur.execute(prod_id_dropdown)
        pid_dropdown = cur.fetchall()

        # Render the Ordered_Products page with the fetched data
        return render_template("ordered_products.j2", order_prod_data = order_prod_table, order_prod_nums = order_prod_nums, pid_dropdown = pid_dropdown, oid_dropdown = oid_dropdown)

# Manufacturers
@app.route('/manufacturers.html', methods=["POST", "GET"])
def manufacturers():
    """ 
    Route for the Manufacturers page. Has Create and Read functionality.
    """
    # Add a Manufacturer to the database 
    if request.method == "POST":                    
        if request.form.get("insert_manufacturer_submit"):
            manufacturer_name = request.form["manufacturer_name"]
            email = request.form["email"]
            phone_number = request.form["phone_number"]
            street_address = request.form["street_address"]
            city = request.form["city"]
            state = request.form["state"]
            zip = request.form["zip"]

            # No NULLable attributes, run the query if user provided all data
            if manufacturer_name and email and phone_number and street_address and city and state and zip:
                query = "INSERT INTO Manufacturers (manufacturer_name, email, phone_number, street_address, city, state, zip) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, [manufacturer_name, email, phone_number, street_address, city, state, zip])
                mysql.connection.commit()

        # redirect back to Manufacturers page
        return redirect("/manufacturers.html")

    # Get data to display in table
    if request.method == "GET":
        # Query to populate table
        query_table = "SELECT * FROM Manufacturers"
        cur = mysql.connection.cursor()
        cur.execute(query_table)
        man_table = cur.fetchall()

        # Render the Manufacturers page with the fetched data
        return render_template("manufacturers.j2", man_data = man_table)

# Shippers
@app.route('/shippers.html', methods=["POST", "GET"])
def shippers():
    """ 
    Route for the Shippers page. Has Create and Read functionality.
    """
    # Add a Shippers to the database 
    if request.method == "POST":                    
        if request.form.get("insert_shipper_submit"):
            shipper_name = request.form["shipper_name"]
            shipper_account_num = request.form["shipper_account_num"]
            shipper_contact_name = request.form["shipper_contact_name"]
            shipper_contact_email = request.form["shipper_contact_email"]

            # No NULLable attributes, run the query if user provided all data
            if shipper_name and shipper_account_num and shipper_contact_name and shipper_contact_email:
                query = "INSERT INTO Shippers (shipper_name, shipper_account_num, shipper_contact_name, shipper_contact_email) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, [shipper_name, shipper_account_num, shipper_contact_name, shipper_contact_email])
                mysql.connection.commit()

        # redirect back to Shippers page
        return redirect("/shippers.html")

    # Get data to display in table
    if request.method == "GET":
        # Query to populate table
        query_table = "SELECT * FROM Shippers"
        cur = mysql.connection.cursor()
        cur.execute(query_table)
        ship_table = cur.fetchall()

        # Render the Shippers page with the fetched data
        return render_template("shippers.j2", ship_data = ship_table)

# Warehouses
@app.route('/warehouses.html', methods=["POST", "GET"])
def warehouses():
    """ 
    Route for the Warehouses page. Has Create and Read functionality.
    """

    # pull parameter from query string in GET
    state_option = request.args.get('state_option')

    # Add a Warehouse to the database
    if request.method == "POST":                    
        
        if request.form.get("insert_warehouse_submit"):
            street_address = request.form["street_address"]
            city = request.form["city"]
            state = request.form["state"]
            zip = request.form["zip"]

            # No NULLable attributes, run the query if user provided all data
            if street_address and city and state and zip:
                query = "INSERT INTO Warehouses (street_address, city, state, zip) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, [street_address, city, state, zip])
                mysql.connection.commit()

        # redirect back to Warehouses page
        return redirect("/warehouses.html")

    # Get data to display in table
    if request.method == "GET":
            
        # Query to populate table with all warehouse data
        if state_option is None or state_option == "Show All States":
            query_table = "SELECT * FROM Warehouses"
            cur = mysql.connection.cursor()
            cur.execute(query_table)
            ware_table = cur.fetchall()

        # Query to populate table with selected state
        else:
            query_table = "SELECT * FROM Warehouses WHERE state=%s"
            cur = mysql.connection.cursor()
            cur.execute(query_table, [state_option])
            ware_table = cur.fetchall()

        # Query to fill filter select box with state
        query_id_dropdown = "SELECT state FROM Warehouses"
        cur = mysql.connection.cursor()
        cur.execute(query_id_dropdown)
        state_list = cur.fetchall()

        # Render the Warehouses page with the fetched data
        return render_template("warehouses.j2", ware_data = ware_table, state_data = state_list)

# Listener
if __name__ == "__main__":
    app.run(host="flip1.engr.oregonstate.edu", port=3568, debug=True)

   # app.run(host="flip2.engr.oregonstate.edu", port=32480, debug=True)
