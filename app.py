from flask import Flask, request, render_template, jsonify, redirect, url_for
import pyodbc
import pandas as pd
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('queries.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/', methods=['GET', 'POST'])
def index():
    conn = get_db_connection()
    queries = conn.execute('SELECT * FROM all_queries ORDER BY timestamp DESC LIMIT 10').fetchall()
    conn.close()
    return render_template('index.html', queries=queries)

@app.route('/query', methods=['POST'])
def query():
    sql_query = request.form['query']
    connection_string = request.form['connection']
    conn_odbc = pyodbc.connect(connection_string)

    df = pd.read_sql(sql_query, conn_odbc)
    results = df.to_html()

    # Save query to database
    conn = get_db_connection()
    conn.execute('INSERT INTO all_queries (query, connection) VALUES (?, ?)', (sql_query, connection_string))
    conn.commit()
    conn.close()

    return render_template('results.html', results=results, query=sql_query, connection=connection_string)

@app.route('/save_query', methods=['POST'])
def save_query():
    sql_query = request.form['query']
    connection_string = request.form['connection']
    conn = get_db_connection()
    conn.execute('INSERT INTO saved_queries (query, connection) VALUES (?, ?)', (sql_query, connection_string))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
