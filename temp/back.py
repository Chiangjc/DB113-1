from flask import Flask, request, render_template, redirect, url_for, flash
import psycopg2

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for using flash messages

# Set up the database connection
conn = psycopg2.connect(
    dbname="Final",
    user="postgres",
    password="chiang20161231",
    host="localhost",
    port="5432"
)

@app.route('/')
def index():
    return render_template('front.html')

@app.route('/search_employee', methods=['POST'])
def search_employee():
    employee_id = request.form['employee_id']
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM employee WHERE e_id = %s", (employee_id,))
    employee = cursor.fetchone()
    cursor.close()

    # Check if the employee was found
    if employee:
        flash(f'Employee found: {employee[1]}', 'success')  # Show success message with employee name
    else:
        flash('No employee found with that ID.', 'danger')  # Show error message

    return redirect(url_for('front'))  # Redirect back to the home page (index.html)

if __name__ == '__main__':
    app.run(debug=True)
