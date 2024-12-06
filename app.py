from flask import Flask, request, jsonify, make_response, redirect, url_for, session
from flask_cors import CORS
import psycopg2
from psycopg2 import pool
from DB_utils import search_inventory_info

app = Flask(__name__)
CORS(app, supports_credentials=True) # 啟用 CORS
app.secret_key = 'supersecretkey'  # 用於 session 加密

# 建立連接池
try:
    connection_pool = psycopg2.pool.SimpleConnectionPool(1, 20,
                                                         user="postgres",
                                                         password="chiang20161231",
                                                         host="127.0.0.1",
                                                         port="5432",
                                                         database="Final")
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

@app.route('/searchInventoryInfo/<inv_id>', methods=['GET'])
def search_inventory_info_route(inv_id):
    print("Search inventory info")
    try:
        row = search_inventory_info(inv_id)
        if row:
            # 確保返回的行數據格式化為 JSON 格式
            columns = ["inv_id", "p_id", "inv_name", "quantity"]  # 根據你的數據庫表的列名稱進行調整
            result = {'inventory_info': dict(zip(columns, row))}
        else:
            result = {'error': 'Inventory not found'}

        print(f"Query result for inv_id {inv_id}: {result}")
        return jsonify(result)
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while fetching data from PostgreSQL: {error}")
        return jsonify({'error': 'Database query error'}), 500

def authenticate_user(username, password): # 這裡是驗證使用者的邏輯，例如查詢資料庫 # 假設驗證成功返回 True，否則返回 False 
    return True

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)
