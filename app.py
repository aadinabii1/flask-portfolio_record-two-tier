import os
from flask import Flask, render_template, request, redirect, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configure MySQL connection from environment variables
db_config = {
    'host': os.environ.get('DB_HOST', 'db'),
    'user': os.environ.get('DB_USER', 'appuser'),
    'password': os.environ.get('DB_PASSWORD', 'app123'),
    'database': os.environ.get('DB_NAME', 'app_db'),
    'port': int(os.environ.get('DB_PORT', 3306))
}

def get_db_connection():
    """Create and return a database connection with error handling."""
    try:
        return mysql.connector.connect(**db_config)
    except Error as e:
        print(f"Database connection error: {e}")
        raise

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name', '').strip()
    role = request.form.get('role', '').strip()
    skills = request.form.get('skills', '').strip()
    email = request.form.get('email', '').strip()
    
    # Basic validation
    if not all([name, role, skills, email]):
        flash('All fields are required!', 'error')
        return redirect('/')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO portfolio (name, role, skills, email) VALUES (%s, %s, %s, %s)",
            (name, role, skills, email)
        )
        conn.commit()
        flash('Portfolio entry added successfully!', 'success')
    except Error as e:
        print(f"Database error: {e}")
        flash('An error occurred while saving data.', 'error')
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
    return redirect('/portfolio')

@app.route('/portfolio')
def portfolio():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)  # Returns dict instead of tuple
        cursor.execute("SELECT name, role, skills, email FROM portfolio")
        rows = cursor.fetchall()
    except Error as e:
        print(f"Database error: {e}")
        flash('Unable to retrieve portfolio data.', 'error')
        rows = []
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    
    return render_template('table.html', rows=rows)

@app.route('/health', methods=['GET'])
def health():
    try:
        return {"status": "ok"}, 200
    except Exception as e:
        return {"status": "error", "message": str(e)}, 500

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=os.environ.get('DEBUG', 'False').lower() == 'true'
    )