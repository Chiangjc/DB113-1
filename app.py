from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2 import pool

app = Flask(__name__)
CORS(app)  # 啟用 CORS

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
            print(f"Query result for e_id {e_id}: {row}")
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

@app.route('/getRole/<e_id>', methods=['GET'])
def get_role(e_id):
    try:
        conn = connection_pool.getconn()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT role FROM employee WHERE e_id = %s", (e_id,))
            row = cursor.fetchone()
            if row:
                result = {'role': row[0]}
            else:
                result = {'error': 'Employee not found'}
            cursor.close()
            connection_pool.putconn(conn)
            return jsonify(result)
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error while fetching data from PostgreSQL: {error}")
        return jsonify({'error': 'Database query error'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)