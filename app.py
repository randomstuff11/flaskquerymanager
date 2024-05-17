from flask import Flask, request, render_template, jsonify
import pyodbc
import pandas as pd

app = Flask(__name__)

# Configure your ODBC connection
connection_string = 'DRIVER={driver_name};SERVER=server_name;DATABASE=database_name;UID=user;PWD=password'
conn = pyodbc.connect(connection_string)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/query', methods=['POST'])
def query():
    sql_query = request.form['query']
    df = pd.read_sql(sql_query, conn)
    # Convert DataFrame to HTML table
    results = df.to_html()
    # Optionally, save the query here for history
    return render_template('results.html', results=results)

@app.route('/export', methods=['POST'])
def export():
    sql_query = request.form['query']  # Assume the same query is used for exporting
    df = pd.read_sql(sql_query, conn)
    # Save to CSV
    df.to_csv('output.csv')
    return jsonify({'message': 'Exported successfully to output.csv'})

if __name__ == '__main__':
    app.run(debug=True)
