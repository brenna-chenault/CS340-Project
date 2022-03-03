from flask import Flask, render_template, redirect
from flask_mysqldb import MySQL
from flask import request

# Configuration
app = Flask(__name__)

# database connection - from template
app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_liumar"
app.config["MYSQL_PASSWORD"] = "3794"
app.config["MYSQL_DB"] = "cs340_liumar"
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
    # Add an Order to the database 
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
                cur.execute(query, (manufacturer_id, time_placed, status))
                mysql.connection.commit()

            # NULL shipper_id only
            elif shipper_id == "":
                query = "INSERT INTO Orders (manufacturer_id, time_placed, status, warehouse_id) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (manufacturer_id, time_placed, status, warehouse_id))
                mysql.connection.commit()

            # NULL warehouse_id only
            elif warehouse_id == "":
                query = "INSERT INTO Orders (manufacturer_id, shipper_id, time_placed, status) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (manufacturer_id, shipper_id, time_placed, status))
                mysql.connection.commit()

            # All input fields given
            else:
                query = "INSERT INTO Orders (manufacturer_id, shipper_id, time_placed, status, warehouse_id) VALUES (%s, %s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (manufacturer_id, shipper_id, time_placed, status, warehouse_id))
                mysql.connection.commit()

            # redirect back to people page
            return redirect("/orders.html")

    # Get data to display in table and update dropdown
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

        # Render the Orders page with the fetched data
        return render_template("orders.j2", order_data = orders_table, order_nums = order_nums)

# Products
@app.route('/products.html', methods=["POST", "GET"])
def products():
    """ 
    Route for the Products page. Has Create, Read, and Delete functionality.
    """
    # Add a Product to the database 
    if request.method == "POST":                    
        if request.form.get("insert_product_submit"):
            manufacturer_id = request.form["manufacturer_id"]
            product_name = request.form["product_name"]
            product_type = request.form["product_type"]
            product_cost = request.form["product_cost"]
            product_description = request.form["product_description"]

            # No NULLable attributes
            query = "INSERT INTO Products (manufacturer_id, product_name, product_type, product_cost, product_description) VALUES (%s, %s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (manufacturer_id, product_name, product_type, product_cost, product_description))
            mysql.connection.commit()

            # redirect back to people page
            return redirect("/products.html")

    # Get data to display in table and delete dropdown
    if request.method == "GET":
        # Query to populate table
        query_table = "SELECT * FROM Products"
        cur = mysql.connection.cursor()
        cur.execute(query_table)
        prod_table = cur.fetchall()
    
        # Query to fill delete dropdown with product_id
        query_id_dropdown = "SELECT order_id FROM Orders"
        cur = mysql.connection.cursor()
        cur.execute(query_id_dropdown)
        prod_nums = cur.fetchall()

        # Render the Products page with the fetched data
        return render_template("products.j2", prod_data = prod_table, prod_nums = prod_nums)

# Ordered_Products
@app.route('/ordered_products.html', methods=["POST", "GET"])
def ordered_products():
    """ 
    Route for the Ordered_Products page. Has Create, Read, and Delete functionality.
    """
    # Add an Ordered_Product to the database 
    if request.method == "POST":                    
        if request.form.get("insert_order_product_submit"):
            order_id = request.form["order_id"]
            product_id = request.form["product_id"]
            number_ordered = request.form["number_ordered"]
            ordered_cost = request.form["ordered_cost"]

            # No NULLable attributes
            query = "INSERT INTO Ordered_Products (order_id, product_id, number_ordered, ordered_cost) VALUES (%s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (order_id, product_id, number_ordered, ordered_cost))
            mysql.connection.commit()

            # redirect back to people page
            return redirect("/ordered_products.html")

    # Get data to display in table and delete dropdown
    if request.method == "GET":
        # Query to populate table
        query_table = "SELECT * FROM Ordered_Products"
        cur = mysql.connection.cursor()
        cur.execute(query_table)
        order_prod_table = cur.fetchall()
    
        # Query to fill delete dropdown with product_id
        query_id_dropdown = "SELECT order_product_id FROM Ordered_Products"
        cur = mysql.connection.cursor()
        cur.execute(query_id_dropdown)
        order_prod_nums = cur.fetchall()

        # Render the Products page with the fetched data
        return render_template("ordered_products.j2", order_prod_data = order_prod_table, order_prod_nums = order_prod_nums)

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

            # No NULLable attributes
            query = "INSERT INTO Manufacturers (manufacturer_name, email, phone_number, street_address, city, state, zip) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (manufacturer_name, email, phone_number, street_address, city, state, zip))
            mysql.connection.commit()

            # redirect back to people page
            return redirect("/manufacturers.html")

    # Get data to display in table
    if request.method == "GET":
        # Query to populate table
        query_table = "SELECT * FROM Manufacturers"
        cur = mysql.connection.cursor()
        cur.execute(query_table)
        man_table = cur.fetchall()

        # Render the Products page with the fetched data
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

            # No NULLable attributes
            query = "INSERT INTO Shippers (shipper_name, shipper_account_num, shipper_contact_name, shipper_contact_email) VALUES (%s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (shipper_name, shipper_account_num, shipper_contact_name, shipper_contact_email))
            mysql.connection.commit()

            # redirect back to people page
            return redirect("/shippers.html")

    # Get data to display in table
    if request.method == "GET":
        # Query to populate table
        query_table = "SELECT * FROM Shippers"
        cur = mysql.connection.cursor()
        cur.execute(query_table)
        ship_table = cur.fetchall()

        # Render the Products page with the fetched data
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

            # No NULLable attributes
            query = "INSERT INTO Warehouses (street_address, city, state, zip) VALUES (%s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (street_address, city, state, zip))
            mysql.connection.commit()

            # redirect back to people page
            return redirect("/warehouses.html")

    # Get data to display in table
    if request.method == "GET":
            
        # Query to populate table with all warehouse data
        if state_option is None or state_option == "Show+All+States":
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

        # Render the Products page with the fetched data
        return render_template("warehouses.j2", ware_data = ware_table, state_data = state_list)

# Listener
if __name__ == "__main__":
    app.run(host="flip2.engr.oregonstate.edu", port=32480, debug=True)
