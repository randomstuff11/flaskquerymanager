from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
import sqlite3
import json
import pandas as pd
import pyodbc
import tempfile

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    connections = conn.execute('SELECT * FROM connections').fetchall()
    conn.close()
    return render_template('index.html', connections=connections)

@app.route('/execute_query', methods=['POST'])
def execute_query():
    query = request.form['query']
    connection_id = request.form['connection_id']
    conn = get_db_connection()
    conn_info = conn.execute('SELECT connection_string FROM connections WHERE id = ?', (connection_id,)).fetchone()
    conn.close()
    
    # Execute the query using the selected database connection
    db_conn = pyodbc.connect(conn_info['connection_string'])
    df = pd.read_sql(query, db_conn)
    temp = tempfile.NamedTemporaryFile(delete=False, suffix='.csv')
    df.to_csv(temp.name, index=False)
    temp.close()
    
    return send_file(temp.name, as_attachment=True, attachment_filename='query_results.csv')

# Additional routes for managing connections, sequences, and viewing results as needed

if __name__ == '__main__':
    app.run(debug=True)
