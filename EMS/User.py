import mysql.connector
dataBase= mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="*******",
    database="employee_management"
)
cursorObject = dataBase.cursor()
# Creation of user table
userRecord=""" CREATE TABLE users (
   id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    password VARCHAR(255)
)"""
cursorObject.execute(userRecord);
dataBase.close()