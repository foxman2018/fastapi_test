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

def sql_get_query(query):
    try:
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(query)
        data = cursor.fetchall()
        cursor.close()
        cnx.close()
        return data
    except:
        return {"Error": "Error retrieving data from server"}

def sql_post_query(query):
    try:
        cursor = cnx.cursor()
        cursor.execute(query)
        id = cursor.lastrowid
        cnx.commit()
        cursor.close()
        cnx.close()
        return id
    except:
        return {"Error": "Error posting data to server"}

app = FastAPI()

class Employee(BaseModel):
    name: str
    position: Optional[str] = None
    age: Optional[float] = None

class Department(BaseModel):
    name: str
    location: Optional[str] = None

@app.get('/')
def index():
    return {"data": ""}
    
@app.get('/employees')
async def employees():
    data = sql_get_query("SELECT * FROM employees")
    return data

@app.get('/employee/{id}')
async def employee(id: int = Path(..., title="The ID of the item to get")):
    data = sql_get_query("SELECT * FROM employees WHERE id = %s" % id)
    return data

@app.post("/employee")
async def create_employee(employee: Employee):
    data = sql_post_query("INSERT INTO employees (name, position, age) VALUES (%s, %s, %s)" % (employee.name, employee.position, employee.age))
    return data

@app.get('/departments')
async def departments():
    data = sql_get_query("SELECT * FROM departments")
    return data

@app.get('/department/{id}')
async def department(id: int = Path(..., title="The ID of the item to get")):
    data = sql_get_query("SELECT * FROM departments WHERE id = %s" % id)
    return data

@app.post("/department")
async def create_employee(department: Department):
    data = sql_post_query("INSERT INTO departments (name, location) VALUES (%s, %s)" % (department.name, department.location))
    return data