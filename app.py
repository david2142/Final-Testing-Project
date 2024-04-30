from flask import Flask,render_template,request,redirect,url_for # type: ignore
import sqlite3
app = Flask(__name__)
import os.path

app = Flask(__name__)
# Define the path to your SQLite database

def get_db_connection():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_dir = (BASE_DIR + '\\TestDB.db')
    conn = sqlite3.connect(db_dir)
    conn.row_factory = sqlite3.Row  # This enables column access by name: row['column_name']     
    return conn

@app.route('/register', methods=['GET'])
def register_form():
    return render_template('Register.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']  # In a real app, hash the password before storing it
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Check if the username already exists
    cur.execute('SELECT * FROM users WHERE username = ?', (username,))
    if cur.fetchone():
        conn.close()
        return "Username already exists. Please choose a different username."
    
    # Insert new user
    cur.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
    conn.commit()
    conn.close()
    
    return redirect(url_for('success'))

@app.route('/success')
def success():
    return render_template('Success.html')

if __name__ == "__main__":
    app.run(debug=True)