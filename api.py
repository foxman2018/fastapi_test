from fastapi import FastAPI, Path
import mysql.connector
from pydantic import BaseModel
from typing import Optional

cnx = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  port=8889,
  database="fastapi_test"
)

def sql_query(query):
    try:
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(query)
        data = cursor.fetchall()
        return data
    except:
        return {"Error": "Error retrieving data from server"}

app = FastAPI()

class Employee(BaseModel):
    name: str
    position: Optional[str] = None
    age: Optional[float] = None

@app.get('/')
def index():
    return {"data": ""}
    
@app.get('/employees')
async def employees():
    data = sql_query("SELECT * FROM employees")
    return data

@app.get('/employee/{id}')
async def employee(id: int = Path(..., title="The ID of the item to get")):
    data = sql_query("SELECT * FROM employees WHERE id = %s" % id)
    return data

@app.get('/departments')
async def departments():
    data = sql_query("SELECT * FROM departments")
    return data

@app.post("/employees/")
async def create_employee(employee: Employee):
    data = sql_query(f"INSERT INTO employees (name, position, age) VALUES (%s, %s, %s)" % (employee.name, employee.position, employee.age))
    return data
