import random
import string

# 可被修改的欄位白名單：欄位名稱無法用參數化查詢，只能先比對白名單以防 SQL injection
MODIFIABLE_COLUMNS = {
    "part": {"p_name", "standard", "length", "width", "height"},
    "supplier": {"s_name", "s_country", "s_address", "s_phone", "super_name"},
    "rate": {"on_time", "quality", "after_sales_service", "final_score", "e_id"},
    "employee": {"e_name", "start_date", "leave_date", "password", "mgr_id", "role"},
}


def _check_column(table, item):
    if item not in MODIFIABLE_COLUMNS[table]:
        raise ValueError(f"Invalid column name for {table}: {item}")


def _strip_password(record):
    """查詢員工資料時不回傳密碼欄位。"""
    if isinstance(record, dict):
        record.pop("password", None)
    return record


# ============================= function for User =============================
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


def update_order_status(cursor, o_id, item, new_value):
    valid_columns = {"status", "feedback", "arrive_date"}
    if item not in valid_columns:
        raise ValueError("Invalid column name.")
    lock_query = f""" 
    SELECT o_id 
    FROM "Order" 
    WHERE o_id = %s 
    FOR UPDATE; 
    """ 
    cursor.execute(lock_query, (o_id,)) # Lock the row

    query = f"""
    UPDATE "Order"
    SET {item} = %s
    WHERE o_id = %s;
    """
    cursor.execute(query, (new_value, o_id))  # Use parameterized query to avoid SQL injection
    cursor.connection.commit()  # Commit the transaction
    return cursor.rowcount  # Return the number of rows affected

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

def find_history(cursor, inv_id):
    query = """
    SELECT *
    FROM "Order"
    WHERE inv_id = %s
    """
    cursor.execute(query, (inv_id,))  # Use parameterized query to avoid SQL injection
    results = cursor.fetchall()
    if results:
        column_names = [desc[0] for desc in cursor.description]
        return [dict(zip(column_names, result)) for result in results]  # Return a list of dictionaries
    else:
        return None

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

def list_order(cursor, order_date, due_date, arrive_date, status):
    conditions = []
    params = []
    if order_date != "None":
        conditions.append("order_date = %s")
        params.append(order_date)
    if due_date != "None":
        conditions.append("due_date = %s")
        params.append(due_date)
    if arrive_date != "None":
        conditions.append("arrive_date = %s")
        params.append(arrive_date)
    if status != "None":
        conditions.append("status LIKE %s")
        params.append(f"%{status}%")

    if not conditions:  # All arguments are "None" (No keyword for search)
        return " order_date, due_date, arrive_date, and status cannot be all empty."

    query = 'SELECT * FROM "Order" WHERE ' + " AND ".join(conditions) + ";"
    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()  # Fetch all matching rows
    if rows:
        column_names = [desc[0] for desc in cursor.description]
        return [dict(zip(column_names, row)) for row in rows]
    return None


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
    cursor.execute(query, (new_value, e_id))
    cursor.connection.commit()  # Commit the transaction
    return cursor.rowcount  # Return the number of rows affected


# ============================= function for Admin =============================

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


def modify_part(cursor, p_id, item, new_value):
    _check_column("part", item)
    query = f"""
    UPDATE part
    SET {item} = %s
    WHERE p_id = %s;
    """
    cursor.execute(query, (new_value, p_id))  # Use parameterized query to avoid SQL injection
    cursor.connection.commit()  # Commit the transaction
    return cursor.rowcount  # Return the number of rows affected

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


def modify_supplier(cursor, s_id, item, new_value):
    _check_column("supplier", item)
    query = f"""
    UPDATE supplier
    SET {item} = %s
    WHERE s_id = %s;
    """
    cursor.execute(query, (new_value, s_id))  # Use parameterized query to avoid SQL injection
    cursor.connection.commit()  # Commit the transaction
    return cursor.rowcount  # Return the number of rows affected

def add_rate(cursor, s_id, year, on_time, quality, after, final_score, e_id):
    query = """
    INSERT INTO rate (s_id, year, on_time, quality, after_sales_service, final_score, e_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (s_id, year, on_time, quality, after, final_score, e_id))
    cursor.connection.commit()

def modify_rate(cursor, year, s_id, item, new_value):
    _check_column("rate", item)
    query = f"""
    UPDATE rate
    SET {item} = %s
    WHERE year = %s AND s_id = %s;
    """
    cursor.execute(query, (new_value, year, s_id))  # Use parameterized query to avoid SQL injection
    cursor.connection.commit()  # Commit the transaction
    return cursor.rowcount  # Return the number of rows affected

def modify_employee(cursor, e_id, item, new_value):
    _check_column("employee", item)
    query = f"""
    UPDATE employee
    SET {item} = %s
    WHERE e_id = %s;
    """
    cursor.execute(query, (new_value, e_id))  # Use parameterized query to avoid SQL injection
    cursor.connection.commit()  # Commit the transaction
    return cursor.rowcount  # Return the number of rows affected

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
        return [_strip_password(dict(zip(column_names, row))) for row in rows]
    return None


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
        return _strip_password(dict(zip(column_names, result)))
    else:
        return f"No employee found with e_id: {e_id}"

def list_rate(cursor, s_id):
    query = """
    SELECT final_score, year, e_id
    FROM rate
    WHERE s_id = %s
    """
    cursor.execute(query, (s_id,))  # Use parameterized query to avoid SQL injection
    rows = cursor.fetchall()
    if rows:
        column_names = [desc[0] for desc in cursor.description]
        return [dict(zip(column_names, row)) for row in rows]
    return None

def search_item(cursor, p_inv, c_inv):
    query = """
    SELECT *, COUNT(*) OVER () AS total_count
    FROM item
    WHERE
    """
    conditions = []
    params = []

    if p_inv != "None":
        conditions.append("parent_inv = %s")
        params.append(p_inv)
    if c_inv != "None":
        conditions.append("child_inv = %s")
        params.append(c_inv)
    if not conditions:
        return "parent_inv and child_inv cannot be both empty."

    query += " AND ".join(conditions) + ";"
    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    if rows:
        column_names = [desc[0] for desc in cursor.description]
        return [dict(zip(column_names, row)) for row in rows]
    return None

def add_item(cursor, parent_inv, child_inv, quantity):
    query = """
    INSERT INTO item (parent_inv, child_inv, quantity)
    VALUES (%s, %s, %s)
    """
    cursor.execute(query, (parent_inv, child_inv, quantity))  # Use parameterized query to avoid SQL injection
    cursor.connection.commit()  # Commit the transaction