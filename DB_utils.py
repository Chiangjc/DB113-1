import sys
import numpy as np
import pandas as pd
import duckdb
import psycopg2
import matplotlib.pyplot as plt
from collections import Counter
from tabulate import tabulate
from threading import Lock

# ============================= Connection to database =============================

DB_NAME = "back"
DB_USER = "postgres"
DB_HOST = "local host"
DB_PORT = 5432

cur = None
db = None
create_event_lock = Lock()

#connect to database
def db_connect():
    exit_code = 0
    try:
        global db
        db = psycopg2.connect(database=DB_NAME, user=DB_USER, password='1234', 
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

def place_order(order_date, due_date, quantity, status, e_id, inv_id):
    query = """
    INSERT INTO "order" (order_date, due_date, quantity, status, e_id, inv_id)
    VALUES (%s, %s, %s, %s, %s, %s)
    RETURNING o_id;
    """
    cur.execute(query, [order_date, due_date, quantity, status, e_id, inv_id])
    o_id = cur.fetchone()[0]
    db.commit()
    return o_id

def update_order_status(o_id, item, new_value):
    
    valid_columns = {"status", "feedback", "arrive_date"}
    if item not in valid_columns:
        raise ValueError("Invalid column name.")
    
    query = f"""
    UPDATE "order"
    SET {item} = %s
    WHERE o_id = %s;
    """
    cur.execute(query, [new_value, o_id])
    db.commit()
    
def search_inventory_info(inv_id):
    query = """
    SELECT *
    FROM inventory AS i
    JOIN part AS p ON i.p_id = p.p_id
    WHERE i.inv_id = %s
    """
    cur.execute(query, (inv_id, ))  # 修正變數名稱
    return cur.fetchone()

def search_inventory_rate(s_id):
    query = """
    SELECT score, year, e_id
    FROM inventory_from_supplier AS ifs
    JOIN rate AS r ON ifs.s_id = r.s_id
    WHERE ifs.s_id = %s
    """
    cur.execute(query, [s_id])  # 使用參數化避免 SQL 注入
    return print_table(cur) #要使用的話，需確保 print_table() 函式可用
    
def search_factory(f_name):
    query = """
    SELECT *
    FROM factory
    WHERE f_name = %s
    """
    cur.execute(query, [f_name])
    return print_table(cur)  # 使用 print_table 格式化輸出

def search_supplier(s_name):
    query = """
    SELECT *
    FROM supplier
    WHERE s_name = %s
    """
    cur.execute(query, [s_name])
    return print_table(cur)  # 使用 print_table 格式化輸出

def list_inventory(inv_name):
    query = """
    select*
    from inventory
    where inv_name = %s
    """
    cur.execute(query, [inv_name])
    return print_table(cur)

def list_order(order_date, due_date, arrive_date, status):
    query = f"""
    select*
    from order
    where
    """
    count = 0
    if order_date != "None":
        count += 1
        query += f" order_date Like '%{ order_date }%'"
    if due_date != "None":
        if count > 0:
            query += ' And '
            count += 1
            query += f" due_date Like '%{due_date }%'"
    if arrive_date != "None":
        if count > 0:
            query += ' And '
            count += 1
            query += f" arrive_date Like '%{ arrive_date }%'"
    if status != "None":
        if count > 0:
            query += ' And '
            count += 1
            query += f" status Like '%{ status }%'"
            query += ';'
    if count == 0: # All argument is "None" (No keyword for search)
        return " order_date, due_date, arrive_date and status cannot be all empty."

    # print(cur.mogrify(query))
    cur.execute(query)
    return print_table(cur)
    
def search_order(o_id):
    query = """
    SELECT *
    FROM "order"
    WHERE o_id = %s
    """
    cur.execute(query, [o_id])
    return cur.fetchone()  # 返回單筆查詢結果

# ============================= function for Admin =============================

# add user or admin themselves
def db_register_employee(e_name, start_date, password, mgr_id, role):
    cmd =   """
            INSERT INTO employee (e_name, start_date, password, mgr_id, role) 
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING e_id;
            """
    cur.execute(cmd, [e_name, start_date, password, mgr_id, role])
    e_id = cur.fetchone()[0]
    db.commit()

    return e_id
    
def add_inventory(inv_name, status, p_id):
    query = """
    INSERT INTO inventory (inv_name, status, p_id)
    VALUES (%s, %s, %s)
    RETURNING i_id
    """
    cur.execute(query, [inv_name, status, p_id])
    i_id = cur.fetchone()[0]
    db.commit()
    return i_id  # 可以選擇返回 i_id

def add_inventory(inv_name, status, p_id):
    query = """
    INSERT INTO inventory (inv_name, status, p_id)
    VALUES (%s, %s, %s)
    RETURNING i_id
    """
    cur.execute(query, [inv_name, status, p_id])
    i_id = cur.fetchone()[0]
    db.commit()
    return i_id  # 可以選擇返回 i_id

def modify_part(p_id, item, new_value):
    query = """
    UPDATE part
    SET {0} = %s
    WHERE p_id = %s;
    """
    cur.execute(query, [new_value, p_id])
    db.commit()
    
def add_supplier(s_name, s_country, s_address, s_phone, super_name):
    query = """
    INSERT INTO supplier (s_name, s_country, s_address, s_phone, super_name)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING s_id
    """
    cur.execute(query, [s_name, s_country, s_address, s_phone, super_name])
    s_id = cur.fetchone()[0]
    db.commit()
    return s_id  # 可以選擇返回 s_id

def modify_supplier(s_id, item, new_value):
    query = f"""
    UPDATE supplier
    SET {item} = %s
    WHERE s_id = %s;
    """
    cur.execute(query, [new_value, s_id])
    db.commit()

def add_rate(score, year, s_id, e_id):
    query = """
    INSERT INTO rate (score, year, s_id, e_id)
    VALUES (%s, %s, %s, %s)
    RETURNING rate_id
    """
    cur.execute(query, [score, year, s_id, e_id])
    rate_id = cur.fetchone()[0]
    db.commit()
    return rate_id  # 返回 rate_id

def modify_rate(year, s_id, item, new_value):
    query = f"""
    UPDATE rate
    SET {item} = %s
    WHERE year = %s AND s_id = %s;
    """
    cur.execute(query, [new_value, year, s_id])
    db.commit()

def modify_employee(e_id, item, new_value):
    query = f"""
    UPDATE employee
    SET {item} = %s
    WHERE e_id = %s;
    """
    cur.execute(query, [new_value, e_id])
    db.commit()

def list_employee(start_date, mgr_id):
    query = """
    SELECT *
    FROM employee
    WHERE
    """
    count = 0
    if start_date != "None":
        count += 1
        query += f" start_date LIKE '%{start_date}%'"
    if mgr_id != "None":
        if count > 0:
            query += ' AND '
        count += 1
        query += f" mgr_id LIKE '%{mgr_id}%'"
    query += ';'
    
    if count == 0:  # All arguments are "None" (No keyword for search)
        return "start_date and mgr_id cannot be both empty."

    cur.execute(query)
    return print_table(cur)

def search_employee(e_id):
    query = """
    SELECT *
    FROM employee
    WHERE e_id = %s
    """
    cur.execute(query, [e_id])
    result = cur.fetchone()
    if result:
        return result  # 或者返回 print_table(result) 如果需要格式化輸出
    else:
        return f"No employee found with e_id: {e_id}"

def list_rate(s_id):
    query = """
    SELECT score, year, e_id
    FROM rate
    WHERE s_id = %s
    """
    cur.execute(query, [s_id])
    return print_table(cur)
