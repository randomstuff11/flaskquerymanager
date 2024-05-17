from flask import Flask, request, render_template, jsonify, redirect, url_for
import pyodbc
import pandas as pd
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('queries.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    queries = conn.execute('SELECT * FROM all_queries ORDER BY timestamp DESC LIMIT 10').fetchall()
    connections = conn.execute('SELECT * FROM connections').fetchall()
    conn.close()
    return render_template('index.html', queries=queries, connections=connections)

@app.route('/manage_connections', methods=['GET', 'POST'])
def manage_connections():
    if request.method == 'POST':
        name = request.form['name']
        connection_string = request.form['connection_string']
        conn = get_db_connection()
        conn.execute('INSERT INTO connections (name, connection_string) VALUES (?, ?)', (name, connection_string))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('manage_connections.html')

@app.route('/query', methods=['POST'])
def query():
    sql_query = request.form['query']
    connection_id = int(request.form['connection'])
    conn = get_db_connection()
    connection = conn.execute('SELECT connection_string FROM connections WHERE id = ?', (connection_id,)).fetchone()
    conn_odbc = pyodbc.connect(connection['connection_string'])

    df = pd.read_sql(sql_query, conn_odbc)
    results = df.to_html()

    conn.execute('INSERT INTO all_queries (query, connection_id) VALUES (?, ?)', (sql_query, connection_id))
    conn.commit()
    conn.close()

    return render_template('results.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)
