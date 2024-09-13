import mysql.connector

dataBase =mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="******"
)
cursorObject = dataBase.cursor()
# employee_management database creation
cursorObject.execute("CREATE DATABASE employee_management")
dataBase.close()
dataBase= mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="*****",
    database="employee_management"
)
cursorObject = dataBase.cursor()
# creating a employee table
employeeRecord=""" CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    age INT,
    department VARCHAR(255),
    salary DECIMAL(10, 2)
)"""
cursorObject.execute(employeeRecord);
dataBase.close()

