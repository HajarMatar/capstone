from flask import Flask, jsonify
from flask import Flask, flash, redirect, render_template, request, session,url_for, abort
import mysql.connector
import os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "*"])

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'capstone',
    'auth_plugin': 'mysql_native_password'
}
@app.route('/test')
def index():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Execute a query to fetch users
    query = "SELECT * FROM suppliers"
    cursor.execute(query)
    data = cursor.fetchall()

    # Close the database connection
    cursor.close()
    conn.close()
    return render_template('login.html',data=data)
#mysql = MySQL(app)
#conn = mysql.connect()
#Creating a connection cursor
#cursor = mysql.connection.cursor()
#cursor.execute("SELECT * from suppliers")
#data = cursor.fetchone()
#Executing SQL Statements#
#cursor.execute(''' CREATE TABLE test(field1, field2) ''')
 
#Saving the Actions performed on the DB
#mysql.connection.commit()
 
#Closing the cursor
#cursor.close()
 
#mysql = MySQL(app)

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello Boss!"

from flask import request

@app.route('/supplier_login', methods=['POST'])
def supplier_login():
    phone_number = request.json.get('phone_number')
    password = request.json.get('password')

    if not phone_number or not password:
        return jsonify({"result": 'Missing phone_number or password'}), 400

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)  # Use dictionary=True to fetch results as dictionaries

    query = "SELECT * FROM suppliers WHERE phone_number = %s"

    cursor.execute(query, (phone_number,))
    data = cursor.fetchone()

    if data is None:
        return jsonify({"result": 'User Not Found'}), 404
    else:
        stored_password = data['password']  # Access 'password' field using dictionary key
        if password == stored_password:
            return jsonify({"result": 'Successful', "supplier": data}), 200
        else:
            return jsonify({"result": 'Wrong Password'}), 401

    cursor.close()
    conn.close()

    return home()

@app.route('/add_supplier', methods=['POST'])
def add_supplier():
    input_data = request.json

    name = input_data.get('name')
    phone_number = input_data.get('phone_number')
    region = input_data.get('region')
    email = input_data.get('email')
    password = input_data.get('password')

    if not name or not phone_number or not region or not email or not password:
        return jsonify({"result": 'Missing required data'}), 400

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)  # Use dictionary=True to fetch results as dictionaries

    query = "SELECT phone_number FROM suppliers WHERE phone_number = %s"
    cursor.execute(query, (phone_number,))
    data = cursor.fetchone()

    if data is None:
        try:
            created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            add_supplier_query = (
                "INSERT INTO `suppliers` "
                "(`name`, `phone_number`, `Region`, `created_at`, `email`, `password`) "
                "VALUES (%s, %s, %s, %s, %s, %s)"
            )
            cursor.execute(add_supplier_query, (name, phone_number, region, created, email, password))
            conn.commit()

            get_supplier_query = "SELECT * FROM suppliers WHERE phone_number = %s"
            cursor.execute(get_supplier_query, (phone_number,))
            added_supplier = cursor.fetchone()

            cursor.close()
            conn.close()

            return jsonify({"result": "Supplier added successfully", "supplier": added_supplier})
        except mysql.connector.Error as err:
            cursor.close()
            conn.close()
            return jsonify({"result": 'Error'})
    else:
        cursor.close()
        conn.close()
        return jsonify({"result": "Used Phone Number"}), 409
    

@app.route('/edit_supplier', methods=['POST'])
def update_supplier():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    phone_number = request.args.get('phone_number')

    if not phone_number:
        return jsonify({"result": "Missing phone_number query parameter"}), 400

    check_query = "SELECT * FROM suppliers WHERE phone_number = %s"
    cursor.execute(check_query, (phone_number,))
    existing_supplier = cursor.fetchone()

    if existing_supplier:
        update_query = "UPDATE `suppliers` SET "
        update_params = []

        for field, value in request.json.items():
            update_query += f"`{field}` = %s, "
            update_params.append(value)

        # Remove the trailing comma and space
        update_query = update_query[:-2]

        update_query += " WHERE `phone_number` = %s"
        update_params.append(phone_number)

        cursor.execute(update_query, update_params)
        conn.commit()

        cursor.execute(check_query, (phone_number,))
        updated_supplier = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify({"result": "Supplier updated successfully!", "supplier": updated_supplier})
    else:
        return jsonify({"result": "Supplier not found"}), 404

@app.route('/view_tanks', methods=['GET'])
def view_tanks():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    id = request.args.get('id')

    tanks = "SELECT * from tanks where client_id = %s"
    cursor.execute(tanks, (id,))

    results = [{key: value for key, value in zip(cursor.column_names, row)} for row in cursor.fetchall()]
    cursor.close()
    conn.close()

    return jsonify(results)


@app.route('/client_login', methods=['POST','GET'])
def client_login():
    phone_number = request.json.get('phone_number')
    password = request.json.get('password')

    if not phone_number or not password:
        return jsonify({"result": 'Missing phone_number or password'}), 400

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)  # Use dictionary=True to fetch results as dictionaries

    query = "SELECT * FROM clients WHERE phone_number = %s"

    cursor.execute(query, (phone_number,))
    data = cursor.fetchone()

    if data is None:
        return jsonify({"result": 'User Not Found'}), 404
    else:
        stored_password = data['password']
        if password == stored_password:
            return jsonify({"result": 'Successful', "client": data}), 200
        else:
            return jsonify({"result": 'Wrong Password'}), 401


    cursor.close()
    conn.close()

    return home()

@app.route('/add_client', methods=['POST'])
def add_client():
    input_data = request.json

    name = input_data.get('name')
    phone_number = input_data.get('phone_number')
    email = input_data.get('email')
    password = input_data.get('password')

    if not name or not phone_number or not email or not password:
        return jsonify({"result": 'Missing required data'}), 400

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)  # Use dictionary=True to fetch results as dictionaries

    query = "SELECT phone_number FROM clients WHERE phone_number = %s"
    cursor.execute(query, (phone_number,))
    data = cursor.fetchone()

    if data is None:
        try:
            created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            add_client_query = (
                "INSERT INTO `clients` "
                "(`name`, `phone_number`, `created_at`, `email`, `password`) "
                "VALUES (%s, %s, %s, %s, %s)"
            )
            cursor.execute(add_client_query, (name, phone_number, created, email, password))
            conn.commit()

            get_client_query = "SELECT * FROM clients WHERE phone_number = %s"
            cursor.execute(get_client_query, (phone_number,))
            added_client = cursor.fetchone()

            cursor.close()
            conn.close()

            return jsonify({"result": "Client added successfully", "client": added_client})
        except mysql.connector.Error as err:
            cursor.close()
            conn.close()
            return jsonify({"result": 'Error'})
    else:
        cursor.close()
        conn.close()
        return jsonify({"result": "Used Phone Number"}), 409
    

@app.route('/edit_client', methods=['POST'])
def update_client():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    input_data = request.json

    phone_number = request.args.get('phone_number')

    if not phone_number:
        return jsonify({"result": "Missing phone_number query parameter"}), 400

    check_query = "SELECT * FROM clients WHERE phone_number = %s"
    cursor.execute(check_query, (phone_number,))
    existing_client = cursor.fetchone()

    if existing_client:
        update_query = "UPDATE `clients` SET "
        update_params = []

        for field, value in input_data.items():
            update_query += f"`{field}` = %s, "
            update_params.append(value)

        update_query = update_query[:-2]

        update_query += " WHERE `phone_number` = %s"
        update_params.append(phone_number)

        cursor.execute(update_query, update_params)
        conn.commit()

        cursor.execute(check_query, (phone_number,))
        updated_client = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify({"result": "User updated successfully!", "client": updated_client})
    else:
        return jsonify({"result": "Client not found"}), 404



@app.route('/change_client_password', methods =['POST','GET'])
def change_client_password (dataa=[{'phone_number':'71504530','password':'1234','new_password':'Mohamad'}]):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor() 
    input=dataa[0]
    existing= "SELECT id,phone_number,password FROM clients WHERE phone_number='"+input["phone_number"]+"'"

    cursor.execute(existing)
    old_pass=cursor.fetchone()
    if old_pass[2]==input['password']:
        id=old_pass[0]
        edit_pass= (
            "update `clients` set"
            "`password`='{}' where id={} "
            .format(
                input['new_password'], old_pass[0]
            )
            )
        cursor.execute(edit_pass)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify([{"result":"password updated successfully!"}])
    else: 
        return jsonify([{"result":"wrong old password"}])
    
@app.route('/change_supplier_password', methods =['POST','GET'])
def change_supplier_password (dataa=[{'phone_number':'717171','password':'1234','new_password':'321'}]):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor() 
    input=dataa[0]
    existing= "SELECT id,phone_number,password FROM suppliers WHERE phone_number='"+input["phone_number"]+"'"

    cursor.execute(existing)
    old_pass=cursor.fetchone()
    if old_pass[2]==input['password']:
        ID_num=old_pass[0]
        edit_pass= (
            "update `suppliers` set "
            "`password`='{}'  where id={} "
            .format(
                input['new_password'], ID_num
            )
        )
        cursor.execute(edit_pass)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify([{"result":"password updated successfully!"}])
    else: 
        return jsonify([{"result":"wrong old password"}])
    

@app.route('/view_all_suppliers' , methods=['POST','GET'])
def view_all_suppliers(dataa=[{'Saida','Beirut'}]):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor() 
    input=dataa[0]
    regions=','.join(input)
    regions = ', '.join([f"'{item}'" for item in input])

    supplier_in_region= "SELECT * FROM suppliers WHERE region in ("+regions+")"
    cursor.execute(supplier_in_region)
    results = [{key: value for key, value in zip(cursor.column_names, row)} for row in cursor.fetchall()]
    cursor.close()
    cursor.close()
    return results

@app.route('/view_single_supplier', methods=['GET'])
def view_single_supplier():
    phone_number = request.args.get('phone_number')

    if not phone_number:
        return jsonify({"error": "phone parameter is required"}), 400

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor() 
    single_supplier = "SELECT * FROM suppliers WHERE phone_number = %s"
    cursor.execute(single_supplier, (phone_number,))
    
    results = [{key: value for key, value in zip(cursor.column_names, row)} for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    
    return jsonify(results)

@app.route('/view_single_client', methods=['GET'])
def view_single_client():
    phone_number = request.args.get('phone_number')

    if not phone_number:
        return jsonify({"error": "phone parameter is required"}), 400

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor() 
    single_client = "SELECT * FROM clients WHERE phone_number = %s"
    cursor.execute(single_client, (phone_number,))
    
    results = [{key: value for key, value in zip(cursor.column_names, row)} for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    
    return jsonify(results)

@app.route('/add_order',methods=['POST','GET'])
def add_order():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    input = request.get_json()
    created=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    add= (
            "INSERT INTO `orders`"
            "(`client_id`, `tank_id`, `payment_method`, `state`,`created_at`) "
            "VALUES ('{}', '{}', '{}','{}', '{}')"
            .format(
                input['client_id'], input['tank_id'], input['payment_method'],
                'pending',created
            )
            )
    cursor.execute(add)
    conn.commit()
    order_id = cursor.lastrowid
    cursor.execute("SELECT * FROM `orders` WHERE `id` = %s", (order_id,))
    order_info = cursor.fetchone()
    
    cursor.close()
    conn.close()
    if order_info:
        return jsonify({"result": "order added successfully!", "order": order_info})
    else:
        return jsonify({"result": "Failed to retrieve order information."}), 500
    
@app.route('/delete_order',methods=['POST','GET'])
def delete_order():
    input = request.get_json()

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor() 
    delete= (
            "UPDATE `orders`set"
            "`state`='{}' where id={} "
            .format(
                'deleted',input['id']
            )
            )
    cursor.execute(delete)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify([{"result":"order deleted successfully!"}])

@app.route('/add_offer',methods=['POST','GET'])
def add_offer():
    input = request.get_json()
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor()
    created=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_offer= ("INSERT INTO `offers`"
            "(`order_id`, `supplier_id`, `tank_id` ,`payment_method`,`price`,`state`,`created_at`) "
            "VALUES ('{}', '{}', '{}','{}','{}', '{}','{}')"
            .format(
                input['order_id'], input['supplier_id'], input['tank_id'],
                input['payment_method'],input['price'],'pending', created
            )
            )
    cursor.execute(new_offer)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"result":"offer added successfully!"})


@app.route('/delete_offer', methods=['DELETE'])
def delete_offer():
    input_id = request.args.get('id')
    updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    if not input_id:
        return jsonify({"result": "Missing 'id' query parameter"}), 400

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        update_offer_query = "UPDATE offers SET state = 'rejected', updated_at = %s WHERE id = %s"
        cursor.execute(update_offer_query, (updated_at, input_id,))
        conn.commit()

        if cursor.rowcount > 0:
            cursor.close()
            conn.close()
            return jsonify({"result": "Offer deleted successfully!"})
        else:
            cursor.close()
            conn.close()
            return jsonify({"result": "Offer not found"}), 404

    except mysql.connector.Error as err:
        return jsonify({"result": "Error: " + str(err)}), 500

@app.route('/accept_offer', methods=['PUT'])
def accept_offer():

    input_id = request.args.get('id')
    input_supplier_id = request.args.get('supplier_id')
    input_order_id = request.args.get('order_id')
    input_price = request.args.get('price')
    updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    if not input_id:
        return jsonify({"result": "Missing 'id' query parameter"}), 400

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        update_offer_query = (
        "UPDATE `offers` SET `state`='accepted', `updated_at`='{}' WHERE `id`='{}'"
        .format(updated_at, input_id)
    )
        cursor.execute(update_offer_query)
        
        if cursor.rowcount > 0:
            update_order_query = (
                "UPDATE orders SET state = 'accepted', supplier_id = %s, price = %s, offer_id = %s, updated_at = %s WHERE id = %s"
            )
            cursor.execute(update_order_query, (input_supplier_id, input_price, input_id, updated_at, input_order_id))

            print(cursor.statement)

            conn.commit()
            cursor.close()
            conn.close()
            return jsonify({"result": "Offer accepted successfully!"})
        else:
            cursor.close()
            conn.close()
            return jsonify({"result": "Offer not found"}), 404

    except mysql.connector.Error as err:
        return jsonify({"result": "Error: " + str(err)}), 500


@app.route("/complete_order", methods=['POST','GET'])
def complete_order():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    id = request.args.get('id')

    updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    update_order = (
        "UPDATE `orders` SET `state`='completed', `updated_at`='{}' WHERE `id`='{}'"
        .format(updated_at, id)
    )

    cursor.execute(update_order)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({"result": "order completed successfully!"})


@app.route('/view_client_orders', methods=['GET'])
def view_client_orders():
    conn = mysql.connector.connect(**db_config)
    id = request.args.get('id')
    cursor = conn.cursor()

    orders = (
     "SELECT * from orders where `client_id`=%s"
    )

    cursor.execute(orders, (id,))
    results = [{key: value for key, value in zip(cursor.column_names, row)} for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return jsonify(results)



@app.route('/view_supplier_orders', methods=['GET'])
def view_supplier_orders():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    supplier_orders = (
        "SELECT orders.*, clients.name as client_name "
        "FROM orders "
        "JOIN clients ON orders.client_id = clients.id "
        "WHERE orders.state='pending'"
    )

    cursor.execute(supplier_orders)
    results = [{key: value for key, value in zip(cursor.column_names, row)} for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return jsonify(results)


@app.route('/view_supplier_orders_to_serve', methods=['GET'])
def view_supplier_orders_to_serve():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    id = request.args.get('id')

    supplier_orders_query = (
        "SELECT orders.*, clients.name as client_name, clients.phone_number as client_phone "
        "FROM orders "
        "JOIN clients ON orders.client_id = clients.id "
        "WHERE orders.state='accepted' AND orders.supplier_id=%s"
    )

    cursor.execute(supplier_orders_query, (id,))
    results = [dict(zip(cursor.column_names, row)) for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return jsonify(results)


@app.route('/view_offers',methods=['POST','GET'])
def view_orders():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    offers=("SELECT * from offers where state='pending'")

    cursor.execute(offers)
    results = [{key: value for key, value in zip(cursor.column_names, row)} for row in cursor.fetchall()]
    cursor.close()
    cursor.close()
    return jsonify(results)

@app.route('/add_tank',methods=['POST','GET'])
def add_tank():
    created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)  # Use dictionary cursor to get rows as dictionaries
    input_data = request.get_json()
    
    add_tank = (
        "INSERT INTO `tanks`"
        "(`type`, `size`, `region`, `client_id`, `address`, `created_at`) "
        "VALUES (%s, %s, %s, %s, %s, %s)"
    )

    values = (
        input_data['type'], input_data['size'],
        input_data['region'], input_data['client_id'], input_data['address'], created
    )

    cursor.execute(add_tank, values)
    conn.commit()

    # Get the ID of the inserted tank
    tank_id = cursor.lastrowid

    cursor.execute("SELECT * FROM `tanks` WHERE `ID` = %s", (tank_id,))
    tank_info = cursor.fetchone()

    cursor.close()
    conn.close()

    if tank_info:
        return jsonify({"result": "Item added successfully!", "tank": tank_info})
    else:
        return jsonify({"result": "Failed to retrieve tank information."}), 500

from flask import request, jsonify

@app.route('/view_tank', methods=['GET'])
def view_tank():
    client_id = request.args.get('id')

    if not client_id:
        return jsonify("Missing 'id' parameter"), 400

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)  # Use dictionary=True to fetch results as dictionaries

        tank = "SELECT * FROM tanks WHERE id = %s"
        cursor.execute(tank, (client_id,))
        result = cursor.fetchall()

        cursor.close()
        conn.close()

        if result:
            return jsonify({"data": result})
        else:
            return jsonify("Tank not found"), 404

    except mysql.connector.Error as err:
        return jsonify({"result": "Error"}), 500


@app.route('/delete_tank',methods=['POST','GET'])
def delete_tank(id=4):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    being_used="SELECT * from orders where tank_id="+str(id)
    cursor.execute(being_used)
    check=cursor.fetchone()
    if check is None:
        delete="DELETE FROM `tanks` WHERE ID="+str(id)
        cursor.execute(delete)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify("Deleted Successfully!")
    else:
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify("This tank has active order")


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=4000)


