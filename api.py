from fastapi import FastAPI
import mysql.connector

cnx = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  port=8889,
  database="fastapi_test"
)

def sql_query(query):
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(query)
    data = cursor.fetchall()
    return data

app = FastAPI()

@app.get('/')
def index():
    return {"data": "index"}
    
@app.get('/employees')
def about():
    data = sql_query("SELECT * FROM employees")
    return data

@app.get('/departments')
def about():
    data = sql_query("SELECT * FROM departments")
    return data
