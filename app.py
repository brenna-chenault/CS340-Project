from flask import Flask, render_template, redirect
import os
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



# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 9112))
    app.run(port=port, debug=True)