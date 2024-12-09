from flask import Flask, request, jsonify, make_response, redirect, url_for, session
from flask_cors import CORS
import psycopg2
from psycopg2 import pool
from datetime import datetime
from DB_utils import search_inventory_info, search_factory, search_inventory_rate, search_supplier
from DB_utils import list_inventory, list_order, search_order, update_order_status, update_password
from DB_utils import db_register_employee
from DB_utils import modify_part, modify_supplier, modify_rate, modify_employee
from DB_utils import search_employee, list_employee, list_rate
from DB_utils import add_rate, place_order, add_supplier, add_inventory

app = Flask(__name__)
CORS(app, supports_credentials=True) # Enable CORS with credentials
app.secret_key = 'supersecretkey'  # Used for session encryption

# Create connection pool
try:
    connection_pool = psycopg2.pool.SimpleConnectionPool(1, 20,
                                                         user="postgres",
                                                         password="123456",
                                                         host="127.0.0.1",
                                                         port="5431",
                                                         database="boeing")
    if connection_pool:
        print("Connection pool created successfully")
except (Exception, psycopg2.DatabaseError) as error:
    print("Error while connecting to PostgreSQL", error)

@app.route('/login/<e_id>', methods=['GET'])
def login(e_id):
    try:
        conn = connection_pool.getconn()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM employee WHERE e_id = %s", (e_id,))
            row = cursor.fetchone()
            if row:
                result = {
                    'e_id': row[0],
                    'e_name': row[1],
                    'password': row[3],
                    'role': row[5]
                }
                response = make_response(jsonify(result))
                response.set_cookie('username', row[1], path='/')
                session['user_id'] = row[0]
                session['role'] = row[5]
                print(f"Set cookie: username={row[1]}")
                return response, 200
            else:
                result = {'error': 'Employee not found'}
            cursor.close()
            connection_pool.putconn(conn)
            return jsonify(result), 404
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while fetching data from PostgreSQL: {error}")
        return jsonify({'error': 'Database query error'}), 500


@app.route('/updatePassword', methods=['POST'])
def update_password_route():
    if 'user_id' not in session:
        return jsonify({'error': 'User not logged in'}), 401

    user_id = session['user_id']
    data = request.get_json()
    new_value = data.get('new_value')

    if not new_value:
        return jsonify({'error': 'New password must be provided'}), 400

    try:
        conn = connection_pool.getconn()
        if conn:
            cursor = conn.cursor()
            rows_affected = update_password(cursor, user_id, new_value)
            cursor.close()
            connection_pool.putconn(conn)
            if rows_affected > 0:
                return jsonify({'message': 'Password updated successfully'}), 200
            else:
                return jsonify({'error': 'User not found'}), 404
        else:
            return jsonify({'error': 'Database connection error'}), 500
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while updating password: {error}")
        return jsonify({'error': 'Database query error'}), 500

@app.route('/getMgrId/<e_id>', methods=['GET'])
def get_mgr_id(e_id):
    try:
        conn = connection_pool.getconn()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT mgr_id FROM employee WHERE e_id = %s", (e_id,))
            row = cursor.fetchone()
            if row:
                result = {'mgr_id': row[0]}
            else:
                result = {'error': 'Employee not found'}
            cursor.close()
            connection_pool.putconn(conn)
            return jsonify(result)
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while fetching data from PostgreSQL: {error}")
        return jsonify({'error': 'Database query error'}), 500

@app.route('/getSuperId/<f_id>', methods=['GET'])
def get_super_id(f_id):
    try:
        conn = connection_pool.getconn()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT super_id FROM factory WHERE f_id = %s", (f_id,))
            row = cursor.fetchone()
            if row:
                result = {'super_id': row[0]}
            else:
                result = {'error': 'Factory not found'}
            cursor.close()
            connection_pool.putconn(conn)
            return jsonify(result)
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while fetching data from PostgreSQL: {error}")
        return jsonify({'error': 'Database query error'}), 500


@app.route('/searchInventory/<inv_id>', methods=['GET'])
def search_inventory(inv_id):
    print(f"Received request to search inventory with inv_id: {inv_id}")
    try:
        conn = connection_pool.getconn()
        if conn:
            cursor = conn.cursor()
            result = search_inventory_info(cursor, inv_id)
            print(f"Search result: {result}")
            cursor.close()
            connection_pool.putconn(conn)
            if result:
                return jsonify(result), 200
            else:
                return jsonify({'error': 'Inventory not found'}), 404
        else:
            print("Database connection error: No available connections")
            return jsonify({'error': 'Database connection error'}), 500
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while fetching data from PostgreSQL: {error}")
        return jsonify({'error': 'Database query error'}), 500


# Define the route and handler function for inventory rate
@app.route('/searchInventoryRate/<s_id>', methods=['GET'])
def get_inventory_rate(s_id):
    print("Search inventory rate")
    try:
        conn = connection_pool.getconn()
        if conn:
            cursor = conn.cursor()
            rates = search_inventory_rate(cursor, s_id)
            if rates:
                result = {'rates': rates}
            else:
                result = {'error': 'No rates found for the given supplier ID'}
                
            cursor.close()
            connection_pool.putconn(conn)
            print(f"Query result for s_id {s_id}: {rates}")
            return jsonify(result)
        else:
            return jsonify({'error': 'Database connection error'}), 500
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while fetching data from PostgreSQL: {error}")
        return jsonify({'error': 'Database query error'}), 500

@app.route('/searchFactory/<f_name>', methods=['GET'])
def get_factory_details(f_name):
    print("Search factory details")
    try:
        conn = connection_pool.getconn()
        if conn:
            cursor = conn.cursor()
            factory_details = search_factory(cursor, f_name)
            if factory_details:
                result = {'factory_details': factory_details}
            else:
                result = {'error': 'Factory not found'}
                
            cursor.close()
            connection_pool.putconn(conn)
            print(f"Query result for f_name {f_name}: {factory_details}")
            return jsonify(result)
        else:
            return jsonify({'error': 'Database connection error'}), 500
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while fetching data from PostgreSQL: {error}")
        return jsonify({'error': 'Database query error'}), 500
    
@app.route('/searchSupplier/<s_name>', methods=['GET'])
def get_supplier_details(s_name):
    print("Search supplier details")
    try:
        conn = connection_pool.getconn()
        if conn:
            cursor = conn.cursor()
            supplier_details = search_supplier(cursor, s_name)
            if supplier_details:
                result = {'supplier_details': supplier_details}
            else:
                result = {'error': 'Supplier not found'}
                
            cursor.close()
            connection_pool.putconn(conn)
            print(f"Query result for s_name {s_name}: {supplier_details}")
            return jsonify(result)
        else:
            return jsonify({'error': 'Database connection error'}), 500
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while fetching data from PostgreSQL: {error}")
        return jsonify({'error': 'Database query error'}), 500

@app.route('/listInventory/<inv_name>', methods=['GET'])
def get_inventory_list(inv_name):
    print("List inventory items")
    try:
        conn = connection_pool.getconn()
        if conn:
            cursor = conn.cursor()
            inventory_list = list_inventory(cursor, inv_name)
            if inventory_list:
                result = {'inventory_list': inventory_list}
            else:
                result = {'error': 'Inventory not found'}
                
            cursor.close()
            connection_pool.putconn(conn)
            print(f"Query result for inv_name {inv_name}: {inventory_list}")
            return jsonify(result)
        else:
            return jsonify({'error': 'Database connection error'}), 500
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while fetching data from PostgreSQL: {error}")
        return jsonify({'error': 'Database query error'}), 500

@app.route('/listOrder', methods=['GET'])
def get_order_list():
    print("List orders")
    order_date = request.args.get('order_date', 'None')
    due_date = request.args.get('due_date', 'None')
    arrive_date = request.args.get('arrive_date', 'None')
    status = request.args.get('status', 'None')
    try:
        conn = connection_pool.getconn()
        if conn:
            cursor = conn.cursor()
            order_list = list_order(cursor, order_date, due_date, arrive_date, status)
            if order_list and isinstance(order_list, list):
                result = {'order_list': order_list}
            else:
                result = {'error': order_list or 'Orders not found'}
                
            cursor.close()
            connection_pool.putconn(conn)
            print(f"Query result: {order_list}")
            return jsonify(result)
        else:
            return jsonify({'error': 'Database connection error'}), 500
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while fetching data from PostgreSQL: {error}")
        return jsonify({'error': 'Database query error'}), 500

@app.route('/searchOrder/<o_id>', methods=['GET'])
def get_order_details(o_id):
    print("Search order details")
    try:
        conn = connection_pool.getconn()
        if conn:
            cursor = conn.cursor()
            order_details = search_order(cursor, o_id)
            if order_details:
                result = {'order_details': order_details}
            else:
                result = {'error': 'Order not found'}
                
            cursor.close()
            connection_pool.putconn(conn)
            print(f"Query result for o_id {o_id}: {order_details}")
            return jsonify(result)
        else:
            return jsonify({'error': 'Database connection error'}), 500
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while fetching data from PostgreSQL: {error}")
        return jsonify({'error': 'Database query error'}), 500

@app.route('/modifyPart', methods=['POST'])
def modify_part_route():
    data = request.get_json()
    p_id = data.get('p_id')
    item = data.get('item')
    new_value = data.get('new_value')
    try:
        conn = connection_pool.getconn()
        if conn:
            cursor = conn.cursor()
            row_count = modify_part(cursor, p_id, item, new_value)
            cursor.close()
            connection_pool.putconn(conn)
            print(f"Part modified. Rows affected: {row_count}")
            if row_count > 0:
                return jsonify({'success': f'{row_count} row(s) updated.'}), 200
            else:
                return jsonify({'error': 'No rows updated.'}), 404
        else:
            return jsonify({'error': 'Database connection error'}), 500
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while modifying part: {error}")
        return jsonify({'error': 'Database query error'}), 500

@app.route('/modifySupplier', methods=['POST'])
def modify_supplier_route():
    data = request.get_json()
    s_id = data.get('s_id')
    item = data.get('item')
    new_value = data.get('new_value')
    try:
        conn = connection_pool.getconn()
        if conn:
            cursor = conn.cursor()
            row_count = modify_supplier(cursor, s_id, item, new_value)
            cursor.close()
            connection_pool.putconn(conn)
            print(f"Supplier modified. Rows affected: {row_count}")
            if row_count > 0:
                return jsonify({'success': f'{row_count} row(s) updated.'}), 200
            else:
                return jsonify({'error': 'No rows updated.'}), 404
        else:
            return jsonify({'error': 'Database connection error'}), 500
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while modifying supplier: {error}")
        return jsonify({'error': 'Database query error'}), 500

@app.route('/modifyRate', methods=['POST'])
def modify_rate_route():
    data = request.get_json()
    year = data.get('year')
    s_id = data.get('s_id')
    item = data.get('item')
    new_value = data.get('new_value')
    try:
        conn = connection_pool.getconn()
        if conn:
            cursor = conn.cursor()
            row_count = modify_rate(cursor, year, s_id, item, new_value)
            cursor.close()
            connection_pool.putconn(conn)
            print(f"Rate modified. Rows affected: {row_count}")
            if row_count > 0:
                return jsonify({'success': f'{row_count} row(s) updated.'}), 200
            else:
                return jsonify({'error': 'No rows updated.'}), 404
        else:
            return jsonify({'error': 'Database connection error'}), 500
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while modifying rate: {error}")
        return jsonify({'error': 'Database query error'}), 500

@app.route('/modifyEmployee', methods=['POST'])
def modify_employee_route():
    data = request.get_json()
    e_id = data.get('e_id')
    item = data.get('item')
    new_value = data.get('new_value')
    try:
        conn = connection_pool.getconn()
        if conn:
            cursor = conn.cursor()
            row_count = modify_employee(cursor, e_id, item, new_value)
            cursor.close()
            connection_pool.putconn(conn)
            print(f"Employee modified. Rows affected: {row_count}")
            if row_count > 0:
                return jsonify({'success': f'{row_count} row(s) updated.'}), 200
            else:
                return jsonify({'error': 'No rows updated.'}), 404
        else:
            return jsonify({'error': 'Database connection error'}), 500
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while modifying employee: {error}")
        return jsonify({'error': 'Database query error'}), 500

@app.route('/searchEmployee/<e_id>', methods=['GET'])
def get_employee_details(e_id):
    print("Search employee details")
    try:
        conn = connection_pool.getconn()
        if conn:
            cursor = conn.cursor()
            employee_details = search_employee(cursor, e_id)
            cursor.close()
            connection_pool.putconn(conn)
            if isinstance(employee_details, dict):
                print(f"Query result for e_id {e_id}: {employee_details}")
                return jsonify({'employee_details': employee_details}), 200
            else:
                print(employee_details)
                return jsonify({'error': employee_details}), 404
        else:
            return jsonify({'error': 'Database connection error'}), 500
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while fetching data from PostgreSQL: {error}")
        return jsonify({'error': 'Database query error'}), 500
    
@app.route('/listEmployee', methods=['GET'])
def get_employee_list():
    start_date_str = request.args.get('start_date', 'None')
    mgr_id = request.args.get('mgr_id', 'None')
    
    # Convert the start_date_str to date if it is not "None"
    if start_date_str != 'None':
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    else:
        start_date = None

    try:
        conn = connection_pool.getconn()
        if conn:
            cursor = conn.cursor()
            employee_list = list_employee(cursor, start_date, mgr_id)
            cursor.close()
            connection_pool.putconn(conn)
            if employee_list and isinstance(employee_list, list):
                return jsonify({'employee_list': employee_list}), 200
            else:
                return jsonify({'error': employee_list or 'No employees found'}), 404
        else:
            return jsonify({'error': 'Database connection error'}), 500
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while fetching data from PostgreSQL: {error}")
        return jsonify({'error': 'Database query error'}), 500

    
@app.route('/listRate/<s_id>', methods=['GET'])
def get_rate_list(s_id):
    try:
        conn = connection_pool.getconn()
        if conn:
            cursor = conn.cursor()
            rate_list = list_rate(cursor, s_id)
            cursor.close()
            connection_pool.putconn(conn)
            if rate_list and isinstance(rate_list, list):
                return jsonify({'rate_list': rate_list}), 200
            else:
                return jsonify({'error': rate_list or 'No rates found'}), 404
        else:
            return jsonify({'error': 'Database connection error'}), 500
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while fetching data from PostgreSQL: {error}")
        return jsonify({'error': 'Database query error'}), 500

@app.route('/addRate', methods=['POST'])
def add_rate_route():
    if 'user_id' not in session:
        return jsonify({'error': 'User not logged in'}), 401
    data = request.get_json()
    score = data.get('score')
    year = data.get('year')
    s_id = data.get('s_id')
    # e_id = data.get('e_id')
    e_id = session['user_id']
    try:
        conn = connection_pool.getconn()
        if conn:
            cursor = conn.cursor()
            add_rate(cursor, score, year, s_id, e_id)
            cursor.close()
            connection_pool.putconn(conn)
            print(f"Rate added for s_id {s_id}")
            return jsonify({'success': 'Rate added successfully'}), 201
        else:
            return jsonify({'error': 'Database connection error'}), 500
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while adding rate: {error}")
        return jsonify({'error': 'Database query error'}), 500
    
@app.route('/updateOrderStatus', methods=['POST'])
def update_order_status_route():
    data = request.get_json()
    o_id = data.get('o_id')
    item = data.get('item')
    new_value = data.get('new_value')
    try:
        conn = connection_pool.getconn()
        if conn:
            cursor = conn.cursor()
            row_count = update_order_status(cursor, o_id, item, new_value)
            cursor.close()
            connection_pool.putconn(conn)
            print(f"Order status updated. Rows affected: {row_count}")
            if row_count > 0:
                return jsonify({'success': f'{row_count} row(s) updated.'}), 200
            else:
                return jsonify({'error': 'No rows updated.'}), 404
        else:
            return jsonify({'error': 'Database connection error'}), 500
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while updating order status: {error}")
        return jsonify({'error': 'Database query error'}), 500

@app.route('/placeOrder', methods=['POST'])
def place_order_route():
    if 'user_id' not in session:
        return jsonify({'error': 'User not logged in'}), 401
    data = request.get_json()
    order_date = data.get('order_date')
    due_date = data.get('due_date')
    quantity = data.get('quantity')
    status = data.get('status')
    e_id = session['user_id']
    inv_id = data.get('inv_id')
    try:
        conn = connection_pool.getconn()
        if conn:
            cursor = conn.cursor()
            o_id = place_order(cursor, order_date, due_date, quantity, status, e_id, inv_id)
            cursor.close()
            connection_pool.putconn(conn)
            print(f"Order placed with o_id {o_id}")
            return jsonify({'o_id': o_id}), 201
        else:
            return jsonify({'error': 'Database connection error'}), 500
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while placing order: {error}")
        return jsonify({'error': 'Database query error'}), 500
    
@app.route('/addSupplier', methods=['POST'])
def add_supplier_route():
    data = request.get_json()
    s_name = data.get('s_name')
    s_country = data.get('s_country')
    s_address = data.get('s_address')
    s_phone = data.get('s_phone')
    super_name = data.get('super_name')
    try:
        conn = connection_pool.getconn()
        if conn:
            cursor = conn.cursor()
            s_id = add_supplier(cursor, s_name, s_country, s_address, s_phone, super_name)
            cursor.close()
            connection_pool.putconn(conn)
            print(f"Supplier added with s_id {s_id}")
            return jsonify({'s_id': s_id}), 201
        else:
            return jsonify({'error': 'Database connection error'}), 500
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while adding supplier: {error}")
        return jsonify({'error': 'Database query error'}), 500

@app.route('/addInventory', methods=['POST'])
def add_inventory_route():
    data = request.get_json()
    inv_name = data.get('inv_name')
    status = data.get('status')
    p_id = data.get('p_id')
    try:
        conn = connection_pool.getconn()
        if conn:
            cursor = conn.cursor()
            inv_id = add_inventory(cursor, inv_name, status, p_id)
            cursor.close()
            connection_pool.putconn(conn)
            print(f"Inventory added with inv_id {inv_id}")
            return jsonify({'inv_id': inv_id}), 201
        else:
            return jsonify({'error': 'Database connection error'}), 500
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while adding inventory: {error}")
        return jsonify({'error': 'Database query error'}), 500

@app.route('/registerEmployee', methods=['POST'])
def register_employee():
    if 'user_id' not in session:
        return jsonify({'error': 'User not logged in'}), 401

    user_id = session['user_id']
    data = request.get_json()
    e_name = data.get('e_name')
    start_date = data.get('start_date')
    password = data.get('password')
    mgr_id = user_id
    role = data.get('role')
    try:
        conn = connection_pool.getconn()
        if conn:
            cursor = conn.cursor()
            e_id = db_register_employee(cursor, e_name, start_date, password, mgr_id, role)
            cursor.close()
            connection_pool.putconn(conn)
            print(f"Employee registered with e_id {e_id}")
            return jsonify({'e_id': e_id}), 201
        else:
            return jsonify({'error': 'Database connection error'}), 500
                
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while registering employee: {error}")
        return jsonify({'error': 'Database query error'}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
