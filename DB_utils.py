import sys
import numpy as np
import pandas as pd
#import duckdb
import psycopg2
#import matplotlib.pyplot as plt
from collections import Counter
from tabulate import tabulate
from threading import Lock
import random
import string

# ============================= Connection to database =============================

DB_NAME = "Final"
DB_USER = "postgres"
DB_HOST = "localhost"
DB_PORT = 5432

cur = None
db = None
create_event_lock = Lock()

#connect to database
def db_connect():
    exit_code = 0
    try:
        global db
        db = psycopg2.connect(database=DB_NAME, user=DB_USER, password='chiang20161231', 
                              host=DB_HOST, port=DB_PORT)
        print("Successfully connect to DBMS.")
        global cur
        cur = db.cursor()
        return db
        
    except psycopg2.Error as err:
        print("DB error: ", err)
        exit_code = 1
    except Exception as err:
        print("Internal Error: ", err)
        raise err
    
    sys.exit(exit_code)
    
#print the result
def print_table(cur):
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    return tabulate(rows, headers=columns, tablefmt="github")

# ============================= System function =============================

#find the user and ensure its authority (input employee_id)
def fetch_user(employee_id): 
    cmd = """
        SELECT * 
        FROM employee e
        WHERE e.User_id = %s;
    """
    cur.execute(cmd, [employee_id])
    rows = cur.fetchall()
    
    if not rows:
        return None, None, None, None, None, None

    return rows

#check whether that user exists    
def userid_exist(userid):
    cmd =   """
            select count(*) 
            from "USER"
            where User_id = %s;
            """
    cur.execute(cmd, [userid])
    count = cur.fetchone()[0]
    return count > 0

# ============================= function for User =============================
# V
def place_order(cursor, order_date, due_date, quantity, status, e_id, inv_id):
    query = """
    INSERT INTO "Order" (order_date, due_date, quantity, status, e_id, inv_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING o_id;
    """
    cursor.execute(query, (order_date, due_date, quantity, status, e_id, inv_id))  # Use parameterized query to avoid SQL injection
    o_id = cursor.fetchone()[0]
    cursor.connection.commit()  # Commit the transaction
    return o_id


# V
def update_order_status(cursor, o_id, item, new_value):
    valid_columns = {"status", "feedback", "arrive_date"}
    if item not in valid_columns:
        raise ValueError("Invalid column name.")
    
    query = f"""
    UPDATE "Order"
    SET {item} = %s
    WHERE o_id = %s;
    """
    cursor.execute(query, (new_value, o_id))  # Use parameterized query to avoid SQL injection
    cursor.connection.commit()  # Commit the transaction
    return cursor.rowcount  # Return the number of rows affected


# V
def search_inventory_info(cursor, inv_id):
    try:
        query = """
        SELECT *
        FROM inventory AS i
        JOIN part AS p ON i.p_id = p.p_id
        LEFT JOIN inventory_from_factory as iff on i.inv_id = iff.inv_id
        LEFT JOIN inventory_from_supplier as ifs on i.inv_id = ifs.inv_id
        WHERE i.inv_id = %s
        """
        cursor.execute(query, (inv_id,))
        row = cursor.fetchone()
        if row:
            column_names = [desc[0] for desc in cursor.description]
            return dict(zip(column_names, row))
        return None
    except Exception as e:
        print(f"Error executing query: {e}")
        return None



# V
def search_inventory_rate(cursor, inv_id):
    query = """
    SELECT r.score, r.year, r.e_id
    FROM inventory_from_supplier AS ifs
    JOIN rate AS r ON ifs.s_id = r.s_id
    WHERE ifs.inv_id = %s
    """
    cursor.execute(query, (inv_id,))  # Use parameterized query to avoid SQL injection
    rows = cursor.fetchall()  # Fetch all matching rows
    if rows:
        column_names = [desc[0] for desc in cursor.description]
        return [dict(zip(column_names, row)) for row in rows]
    return None

# V
def search_factory(cursor, f_name):
    query = """
    SELECT *
    FROM factory
    WHERE f_name = %s
    """
    cursor.execute(query, (f_name,))  # Use parameterized query to avoid SQL injection
    row = cursor.fetchone()  # Fetch the matching row
    if row:
        column_names = [desc[0] for desc in cursor.description]
        return dict(zip(column_names, row))
    return None

#V
def search_supplier(cursor, s_name):
    query = """
    SELECT *
    FROM supplier
    WHERE s_name = %s
    """
    cursor.execute(query, (s_name,))  # Use parameterized query to avoid SQL injection
    row = cursor.fetchone()  # Fetch the matching row
    if row:
        column_names = [desc[0] for desc in cursor.description]
        return dict(zip(column_names, row))
    return None

#V
def list_inventory(cursor, inv_name):
    query = """
    SELECT *
    FROM inventory
    WHERE inv_name = %s
    """
    cursor.execute(query, (inv_name,))  # Use parameterized query to avoid SQL injection
    rows = cursor.fetchall()  # Fetch all matching rows
    if rows:
        column_names = [desc[0] for desc in cursor.description]
        return [dict(zip(column_names, row)) for row in rows]
    return None

# V
def list_order(cursor, order_date, due_date, arrive_date, status):
    query = """
    SELECT *
    FROM "Order"
    WHERE
    """
    count = 0
    if order_date != "None":
        count += 1
        query += f" order_date = '{order_date}'"
    if due_date != "None":
        if count > 0:
            query += ' AND '
        count += 1
        query += f" due_date = '{due_date}'"
    if arrive_date != "None":
        if count > 0:
            query += ' AND '
        count += 1
        query += f" arrive_date = '{arrive_date}'"
    if status != "None":
        if count > 0:
            query += ' AND '
        count += 1
        query += f" status LIKE '%{status}%'"
    query += ';'
    
    if count == 0:  # All arguments are "None" (No keyword for search)
        return " order_date, due_date, arrive_date, and status cannot be all empty."

    cursor.execute(query)
    rows = cursor.fetchall()  # Fetch all matching rows
    if rows:
        column_names = [desc[0] for desc in cursor.description]
        return [dict(zip(column_names, row)) for row in rows]
    return None


# V    
def search_order(cursor, o_id):
    query = """
    SELECT *
    FROM "Order"
    WHERE o_id = %s
    """
    cursor.execute(query, (o_id,))  # Use parameterized query to avoid SQL injection
    row = cursor.fetchone()  # Fetch the matching row
    if row:
        column_names = [desc[0] for desc in cursor.description]
        return dict(zip(column_names, row))
    return None

def update_password(cursor, e_id, new_value):
    query = """
    UPDATE "employee"
    SET password = %s
    WHERE e_id = %s;
    """
    cursor.execute(query, (new_value, e_id))  # Use parameterized query to avoid SQL injection
    cursor.connection.commit()  # Commit the transaction
    return cursor.rowcount  # Return the number of rows affected



# ============================= function for Admin =============================

# X
def generate_employee_id():
    letters = ''.join(random.choices(string.ascii_uppercase, k=2))  # Generate two random uppercase letters
    number = random.randint(1, 9999999999)  # Generate a random number between 1 and 9999999999
    e_id = f"{letters}{number:010d}"  # Format the number to be 10 digits with leading zeros
    return e_id

def db_register_employee(cursor, e_name, start_date, password, mgr_id, role):
    e_id = generate_employee_id()
    cmd = """
    INSERT INTO employee (e_id, e_name, start_date, password, mgr_id, role)
    VALUES (%s, %s, %s,%s, %s, %s)
    """
    cursor.execute(cmd, (e_id, e_name, start_date, password, mgr_id, role))  # Use parameterized query to avoid SQL injection
    cursor.connection.commit()  # Commit the transaction
    return e_id

# V  
def add_inventory(cursor, inv_name, status, p_id):
    query = """
    INSERT INTO inventory (inv_name, status, p_id)
    VALUES (%s, %s, %s)
    RETURNING inv_id
    """
    cursor.execute(query, (inv_name, status, p_id))  # Use parameterized query to avoid SQL injection
    inv_id = cursor.fetchone()[0]
    cursor.connection.commit()  # Commit the transaction
    return inv_id


# V
def modify_part(cursor, p_id, item, new_value):
    query = f"""
    UPDATE part
    SET {item} = %s
    WHERE p_id = %s;
    """
    cursor.execute(query, (new_value, p_id))  # Use parameterized query to avoid SQL injection
    cursor.connection.commit()  # Commit the transaction
    return cursor.rowcount  # Return the number of rows affected

# V 
def add_supplier(cursor, s_name, s_country, s_address, s_phone, super_name):
    query = """
    INSERT INTO supplier (s_name, s_country, s_address, s_phone, super_name)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING s_id
    """
    cursor.execute(query, (s_name, s_country, s_address, s_phone, super_name))  # Use parameterized query to avoid SQL injection
    s_id = cursor.fetchone()[0]
    cursor.connection.commit()  # Commit the transaction
    return s_id


# V
def modify_supplier(cursor, s_id, item, new_value):
    query = f"""
    UPDATE supplier
    SET {item} = %s
    WHERE s_id = %s;
    """
    cursor.execute(query, (new_value, s_id))  # Use parameterized query to avoid SQL injection
    cursor.connection.commit()  # Commit the transaction
    return cursor.rowcount  # Return the number of rows affected

# V
def add_rate(cursor, score, year, s_id, e_id):
    query = """
    INSERT INTO rate (s_id ,year, on_time, quality, after_sales_service, final_score, e_id)
    VALUES (%s, %s,60,60,60, %s, %s)
    """
    print(score)
    cursor.execute(query, (s_id, year, score , e_id))  # Use parameterized query to avoid SQL injection
    cursor.connection.commit()  # Commit the transaction

# V
def modify_rate(cursor, year, s_id, item, new_value):
    query = f"""
    UPDATE rate
    SET {item} = %s
    WHERE year = %s AND s_id = %s;
    """
    cursor.execute(query, (new_value, year, s_id))  # Use parameterized query to avoid SQL injection
    cursor.connection.commit()  # Commit the transaction
    return cursor.rowcount  # Return the number of rows affected

# V
def modify_employee(cursor, e_id, item, new_value):
    query = f"""
    UPDATE employee
    SET {item} = %s
    WHERE e_id = %s;
    """
    cursor.execute(query, (new_value, e_id))  # Use parameterized query to avoid SQL injection
    cursor.connection.commit()  # Commit the transaction
    return cursor.rowcount  # Return the number of rows affected

# V
def list_employee(cursor, start_date, mgr_id):
    query = """
    SELECT *
    FROM employee
    WHERE
    """
    conditions = []
    params = []

    if start_date != "None":
        conditions.append("start_date >= %s")
        params.append(start_date)
    if mgr_id != "None":
        conditions.append("mgr_id = %s")
        params.append(mgr_id)

    if not conditions:
        return "start_date and mgr_id cannot be both empty."

    query += " AND ".join(conditions) + ";"

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    if rows:
        column_names = [desc[0] for desc in cursor.description]
        return [dict(zip(column_names, row)) for row in rows]
    return None


# V
def search_employee(cursor, e_id):
    query = """
    SELECT *
    FROM employee
    WHERE e_id = %s
    """
    cursor.execute(query, (e_id,))  # Use parameterized query to avoid SQL injection
    result = cursor.fetchone()
    if result:
        column_names = [desc[0] for desc in cursor.description]
        return dict(zip(column_names, result))  # Return as a dictionary
    else:
        return f"No employee found with e_id: {e_id}"

# V
def list_rate(cursor, s_id):
    query = """
    SELECT score, year, e_id
    FROM rate
    WHERE s_id = %s
    """
    cursor.execute(query, (s_id,))  # Use parameterized query to avoid SQL injection
    rows = cursor.fetchall()
    if rows:
        column_names = [desc[0] for desc in cursor.description]
        return [dict(zip(column_names, row)) for row in rows]
    return None

