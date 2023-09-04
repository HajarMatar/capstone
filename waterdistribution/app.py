from flask import Flask, jsonify
from flask import Flask, flash, redirect, render_template, request, session,url_for, abort
import mysql.connector
import os
from datetime import datetime,timedelta
from flask_bcrypt import Bcrypt
import bcrypt
import jwt
from functools import wraps
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "*"])

bcrypt = Bcrypt(app)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'capstone',
    'auth_plugin': 'mysql_native_password'
}
app.config['SECRET_KEY'] = 'Qgtd12@tRv&kawrtYF'
# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
  
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        return f( *args, **kwargs)

    return decorated


def generate_token(userid):
    payload = {
        'userid': userid,
        'exp': datetime.utcnow() + timedelta(minutes = 120)  # Token expiration time
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token

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


@app.route('/version', methods=['POST','GET'])
def version():
        return jsonify([{"result":'Successful'}])

@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return "Hello Boss!"

@app.route('/supplier_login', methods=['POST','GET'])
def supplier_login(dataa=[{'phone_number':'717174','password':'321'}]):

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    input=dataa[0]
    # Execute a query to fetch users
    number=dataa[0]['phone_number']
    query = "SELECT phone_number,password,id FROM suppliers WHERE phone_number='"+number+"'"

    cursor.execute(query)
    data = cursor.fetchone()
    if data is None:
        return jsonify([{"result":'user Not Found'}])
    else:
        stored_pass=data[1]
        if bcrypt.check_password_hash(stored_pass, input['password']):
            # generates the JWT Token
            token = generate_token(data[2])
            print(token)
    
            return jsonify({'token' : token, "result":'Successful'})            
            
        else:
            return jsonify([{"result":'Wrong Password'}])


    # Close the database connection
    cursor.close()
    conn.close()

    return home()
@app.route('/add_supplier', methods= ['Post'])
@token_required
def add_supplier():
    #input=dataa[0]
    input = request.get_json()
    print(input)
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Execute a query to fetch users
    
    query = "SELECT phone_number FROM suppliers WHERE phone_number='"+input["phone_number"]+"'"
    cursor.execute(query)
    data = cursor.fetchone()
    if data is None:
        try:
            created=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            hashed_password = bcrypt.generate_password_hash(input['password']).decode('utf-8')
            add_user=  (
            "INSERT INTO `suppliers`"
            "(`name`, `phone_number`, `Region`, `created_at`, `email`, `password`) "
            "VALUES ('{}', '{}', '{}', '{}', '{}', '{}')"
            .format(
                input['name'], input['phone_number'], input['region'],
                created, input['email'], hashed_password
            )
            )
            cursor.execute(add_user)
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify([{"result":"user added successfully!"}])
        except mysql.connector.Error as err:
                cursor.close()
                conn.close()
                return jsonify([{"result":'Error'}])
    else:
        return jsonify([{"result":"user already exists"}])
@app.route('/edit_supplier',methods=['POST','GET'])
def edit_supplier():
    conn = mysql.connector.connect(**db_config)
    input = request.get_json()
    print(input)
    cursor = conn.cursor() 
    existing= "Select * FROM suppliers WHERE phone_number='"+input['new_phone']+"'"
    cursor.execute(existing)
    old=cursor.fetchone()
    if old is None:
        id=("select * from suppliers where phone_number ='"+ input['phone_number']+"'")
        cursor.execute(id)
        id=cursor.fetchall()
        first_row=id[0]
        supplier_id=first_row[0]
        updated=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        edit_info= (
            "update `suppliers` set"
            "`name`='{}', `phone_number`='{}', `Region`='{}', `email`='{}',`updated_at`='{}' where id={} "
            .format(
                input['name'], input['new_phone'], input['region'],
                input['email'], updated,supplier_id
            )
            )
        cursor.execute(edit_info)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify([{"result":"user updated successfully!"}])
    else: 
        return jsonify([{"result":"New username already exists!"}])





@app.route('/client_login', methods=['POST','GET'])
def client_login(dataa=[{'phone_number':'71504530','password':'mohammad'}]):

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Execute a query to fetch users
    number=dataa[0]['phone_number']
    query = "SELECT phone_number,password FROM clients WHERE phone_number='"+number+"'"
    input=dataa[0]
    cursor.execute(query)
    data = cursor.fetchall()
    if data is None:
        return jsonify([{"result":'user Not Found'}])
    else:
        if bcrypt.check_password_hash(data[0][1], input['password']):            
            return jsonify([{"result":'Successful'}])
        else:
            return jsonify([{"result":'Wrong Password'}])


    # Close the database connection
    cursor.close()
    conn.close()

    return home()

@app.route('/add_client', methods= ['Post','GET'])
def add_client(dataa=[{'name':'mahdi','phone_number':'71503540','email':'mahdi@hotmail.com','password':'1234'}]):
    input=dataa[0]
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Execute a query to fetch users
    
    query = "SELECT phone_number FROM clients WHERE phone_number='"+input["phone_number"]+"'"
    cursor.execute(query)
    data = cursor.fetchone()
    if data is None:
        try:
            created=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            hashed_password = bcrypt.generate_password_hash(input['password']).decode('utf-8')

            add_user=  (
            "INSERT INTO `clients`"
            "(`name`, `phone_number`, `created_at`, `email`, `password`) "
            "VALUES ('{}', '{}','{}', '{}', '{}')"
            .format(
                input['name'], input['phone_number'],
                created, input['email'], hashed_password
            )
            )
            cursor.execute(add_user)
            conn.commit()
            cursor.close()
            conn.close()
            return jsonify([{"result":"user added successfully!"}])
        except mysql.connector.Error as err:
                cursor.close()
                conn.close()
                return jsonify([{"result":'Error'}])
    else:
        return jsonify([{"result":"user already exists"}])
    
@app.route('/edit_client',methods=['POST','GET'])
def edit_client(dataa=[{'name':'mahdii','phone_number':'71503540','email':'Mahd@hotmail.com','new_phone':'71514530'}]):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor() 
    input=dataa[0]
    existing= "Select * FROM clients WHERE phone_number='"+input['new_phone']+"'"
    cursor.execute(existing)
    old=cursor.fetchone()
    if old is None:
        id=("select * from clients where phone_number ='"+ input['phone_number']+"'")
        cursor.execute(id)
        id=cursor.fetchall()
        first_row=id[0]
        client_id=first_row[0]     
        edit_info= (
            "update `clients` set"
            "`name`='{}', `phone_number`='{}', `email`='{}' where id={} "
            .format(
                input['name'], input['new_phone'],
                input['email'], client_id
            )
            )
        cursor.execute(edit_info)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify([{"result":"user updated successfully!"}])
    else: 
        return jsonify([{"result":"New user already exists!"}])

@app.route('/change_client_password', methods =['POST','GET'])
def change_client_password (dataa=[{'phone_number':'71504530','password':'1234','new_password':'Mohamad'}]):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor() 
    input=dataa[0]
    existing= "SELECT id,phone_number,password FROM clients WHERE phone_number='"+input["phone_number"]+"'"

    cursor.execute(existing)
    old_pass=cursor.fetchone()
    if bcrypt.check_password_hash(old_pass[2], input['password']):            
        id=old_pass[0]
        edit_pass= (
            "update `clients` set"
            "`password`='{}' where id={} "
            .format(
                bcrypt.generate_password_hash(input['new_password']).decode('utf-8'), old_pass[0]
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
def change_supplier_password (dataa=[{'phone_number':'717174','password':'1234','new_password':'321'}]):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor() 
    input=dataa[0]
    existing= "SELECT id,phone_number,password FROM suppliers WHERE phone_number='"+input["phone_number"]+"'"

    cursor.execute(existing)
    old_pass=cursor.fetchone()
    if bcrypt.check_password_hash(old_pass[2], input['password']):            
        ID_num=old_pass[0]
        edit_pass= (
            "update `suppliers` set "
            "`password`='{}'  where id={} "
            .format(
            bcrypt.generate_password_hash(input['new_password']).decode('utf-8'), ID_num
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
@token_required
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

@app.route('/view_single_supplier',methods=['POST','GET'])
def view_single_supplier(phone_number='717171'):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor() 
    single_supplier= "SELECT * FROM suppliers WHERE phone_number = "+phone_number
    cursor.execute(single_supplier)
    results = [{key: value for key, value in zip(cursor.column_names, row)} for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    
    return jsonify (results)
@app.route('/add_order',methods=['POST','GET'])
def add_order(dataa=[{'client_id':'1','tank_id':'2','payment_method':'cash'}]):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor() 
    input=dataa[0]
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
    cursor.close()
    conn.close()
    return jsonify([{"result":"order added successfully!"}])
    
@app.route('/delete_order',methods=['POST','GET'])
def delete_order(id=4):

    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor() 
    delete= (
            "UPDATE `orders`set"
            "`state`='{}' where id={} "
            .format(
                'deleted',id
            )
            )
    cursor.execute(delete)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify([{"result":"order deleted successfully!"}])

@app.route('/add_offer',methods=['POST','GET'])
def add_offer(dataa=[{'order_id':'4','supplier_id':'1','tank_id':'2','payment_method':'cash'}]):
    input=dataa[0]
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor()
    created=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    new_offer= ("INSERT INTO `offers`"
            "(`order_id`, `supplier_id`, `tank_id` ,`payment_method`,`state`,`created_at`) "
            "VALUES ('{}', '{}', '{}','{}','{}', '{}')"
            .format(
                input['order_id'], input['supplier_id'], input['tank_id'],
                input['payment_method'],'pending', created
            )
            )
    cursor.execute(new_offer)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify([{"result":"offer added successfully!"}])

@app.route('/delete_offer')
def delete_offer(id=2):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    check_offer="SELECT * from offers where id="+id
    cursor.execute(check_offer)
    checkk= ', '.join([f"'{item}'" for item in cursor.fetchall()])
    if checkk[0][5]=='pending':
     
        delete= (
            "UPDATE `offers`set"
            "`state`='{}' where id={} "
            .format(
                'deleted',id
            )
            )
        return jsonify([{"result":"offer deleted successfully!"}])
    elif checkk[0][5]=='deleted':
        return jsonify([{"result":"offer already deleted!"}])

        
    elif checkk[0][5]=='accepted':
        return jsonify([{"result":"offer already accepted!"}])

    cursor.execute(delete)
    conn.commit()
    cursor.close()
    conn.close()

@app.route('/accept_offer',methods=['POST','GET'])
def accept_offer(dataa=[{'offer_id':'3','order_id':'4'}]):
    input=dataa[0]
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor()
    get_offer=('SELECT * from offers where id='+input['offer_id'])
    cursor.execute(get_offer)
    accepted=cursor.fetchall()
    accepted_final = ', '.join([f"'{item}'" for item in accepted])
    updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    update_offer=("UPDATE `offers` set "
                  "`state`='{}',`updated_at`='{}' where `order_id`='{}'"
                  .format(
                    'declined',updated_at,input['order_id']

                  )
                  )
    cursor.execute(update_offer)


    update_order=(" UPDATE `orders` set"
            "`offer_id`={},`price`={},`state`='{}',`supplier_id`='{}',`updated_at`='{}' where `id`={}"
            .format(
                input['offer_id'], accepted[0][4],"accepted",accepted[0][2],updated_at, input['order_id']
            )
            ) 
    update_offer=("UPDATE `offers` set "
                  "`state`='{}',`updated_at`='{}' where `id`='{}'"
                  .format(
                    'accepted',updated_at,input['offer_id']

                  )
                  )
    cursor.execute(update_order)
    cursor.execute(update_offer)
    
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify([{"result":"offer accepted successfully!"}])    

@app.route("/complete_order", methods=['POST','GET'])
def complete_order(id=9):
    conn=mysql.connector.connect(**db_config)
    cursor=conn.cursor()
    updated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    update_order=("UPDATE `orders` set "
             "`state`='{}',`updated_at`='{}' where `id`='{}'"
            .format(
            'completed',updated_at,id

                  )
                  )
    cursor.execute(update_order)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify([{"result":"order completed successfully!"}]) 

@app.route("/view_client_orders", methods=['POST','GET'])
def all_orders(dataa=[{'client_id':'1','state':'all'}]):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor() 
    input=dataa[0]


    if input['state']=='all':
        clients_orders=("SELECT * from orders where `client_id`="+input['client_id'])
    else :
        clients_orders=("SELECT * from orders where `client_id`='{}' AND `state`='{}'"
            .format(
            input['client_id'], input['state']

                  )
                  )

    cursor.execute(clients_orders)
    results = [{key: value for key, value in zip(cursor.column_names, row)} for row in cursor.fetchall()]
    cursor.close()
    cursor.close()
    return jsonify(results)

@app.route('/view_supplier_orders',methods=['POST','GET'])
def view_supplier_orders(dataa=[{'supplier_id':'1','state':'pending'}]):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor() 
    input=dataa[0]


    if input['state']=='all':
        supplier_orders=("SELECT * from orders where `supplier_id`="+input['supplier_id'])
    else :
        supplier_orders=("SELECT * from orders where `supplier_id`='{}' AND `state`='{}'"
            .format(
            input['supplier_id'], input['state']

                  )
                  )

    cursor.execute(supplier_orders)
    results = [{key: value for key, value in zip(cursor.column_names, row)} for row in cursor.fetchall()]
    cursor.close()
    cursor.close()
    return jsonify(results)

@app.route('/view_offers',methods=['POST','GET'])
def view_orders(id=4):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor() 
    offers=("SELECT * from offers where order_id="+str(id))

    cursor.execute(offers)
    results = [{key: value for key, value in zip(cursor.column_names, row)} for row in cursor.fetchall()]
    cursor.close()
    cursor.close()
    return jsonify(results)

@app.route('/add_tank',methods=['POST','GET'])
def add_tank(dataa=[{'type':'tank','size':'10','region':'beirut','client_id':'1','address':'city-area-street-bldg-floor'}]):
    created=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    input=dataa[0]
    add_tank=  (
            "INSERT INTO `tanks`"
            "(`type`, `size`,`region`,`client_id`,`address` ,`created_at`) "
            "VALUES ('{}', '{}','{}', '{}', '{}','{}')"
            .format(
                input['type'], input['size'],
                input['region'], input['client_id'],input['address'],created
            )
            )
    cursor.execute(add_tank)
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify([{"result":"Item added successfully!"}])
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


