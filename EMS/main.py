import mysql.connector
import bcrypt

# making a function to connect database
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="*****",
        database="employee_management"
    )

# hashing
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# for verifying  password
def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

# Check user is exist in database or not
def user_exists(username):
    conn = connect_to_db()
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone() 
    cursor.close()
    conn.close()
    return result is not None

# Function to register a new employee user
def register_employee_user():
    username = input("Enter a new username: ")
    if user_exists(username):
        print("Username already exists. Try logging in.")
        return False
    password = input("Enter a new password: ")
    hashed_password = hash_password(password)
    conn = connect_to_db()
    cursor = conn.cursor()

    # Insert the new user into the users table
    query = "INSERT INTO users (username, password) VALUES (%s, %s)"
    cursor.execute(query, (username, hashed_password.decode('utf-8')))
    conn.commit()
    print("User registered successfully!")
    # Once it registered, then we will add Employee details
    name = input("Enter employee name: ")
    age = int(input("Enter employee age: "))
    department = input("Enter employee department: ")
    salary = float(input("Enter employee salary: "))

    query = "INSERT INTO employees (name, age, department, salary) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, age, department, salary))
    conn.commit()
    print("Employee registered successfully!")
    cursor.close()
    conn.close()
    return True


# Function to log in the user
def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    conn = connect_to_db()
    cursor = conn.cursor()

    query = "SELECT password FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    # Here we are fetching the password
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result:
        stored_password = result[0]
        if verify_password(stored_password, password):
            print("Login successful!")
            return True
        else:
            print("Incorrect password. Try again.")
            return False
    else:
        print("Username not found. Would you like to register as a new employee?")
        register_choice = input("Enter 'yes' to register or 'no' to cancel: ").lower()
        if register_choice == 'yes':
            return register_employee_user()
        else:
            return False


# Function to add a new employee (for general purposes, not the login/registration part)
def add_employee():
    name = input("Enter employee name: ")
    age = int(input("Enter employee age: "))
    department = input("Enter employee department: ")
    salary = float(input("Enter employee salary: "))

    conn = connect_to_db()
    cursor = conn.cursor()

    query = "INSERT INTO employees (name, age, department, salary) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, age, department, salary))

    conn.commit()
    print("Employee added successfully!")
    cursor.close()
    conn.close()


# Function to view all employees
def view_employees():
    conn = connect_to_db()
    cursor = conn.cursor()

    query = "SELECT * FROM employees"
    cursor.execute(query)
    result = cursor.fetchall()

    if result:
        print("\nEmployee List:")
        for row in result:
            print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Department: {row[3]}, Salary: {row[4]}")
    else:
        print("No employees found.")

    cursor.close()
    conn.close()


# Function to update employee details
def update_employee():
    emp_id = int(input("Enter employee ID to update: "))

    print("What do you want to update?")
    print("1. Name")
    print("2. Age")
    print("3. Department")
    print("4. Salary")

    choice = int(input("Enter choice: "))

    conn = connect_to_db()
    cursor = conn.cursor()

    if choice == 1:
        new_name = input("Enter new name: ")
        query = "UPDATE employees SET name = %s WHERE id = %s"
        cursor.execute(query, (new_name, emp_id))
    elif choice == 2:
        new_age = int(input("Enter new age: "))
        query = "UPDATE employees SET age = %s WHERE id = %s"
        cursor.execute(query, (new_age, emp_id))
    elif choice == 3:
        new_department = input("Enter new department: ")
        query = "UPDATE employees SET department = %s WHERE id = %s"
        cursor.execute(query, (new_department, emp_id))
    elif choice == 4:
        new_salary = float(input("Enter new salary: "))
        query = "UPDATE employees SET salary = %s WHERE id = %s"
        cursor.execute(query, (new_salary, emp_id))
    else:
        print("Invalid choice.")
        return

    conn.commit()
    print("Employee updated successfully!")
    cursor.close()
    conn.close()


# Function to delete an employee
def delete_employee():
    emp_id = int(input("Enter employee ID to delete: "))

    conn = connect_to_db()
    cursor = conn.cursor()

    query = "DELETE FROM employees WHERE id = %s"
    cursor.execute(query, (emp_id,))

    conn.commit()
    print("Employee deleted successfully!")
    cursor.close()
    conn.close()


# Function to search for an employee by ID or name
def search_employee():
    print("Search by:")
    print("1. ID")
    print("2. Name")

    choice = int(input("Enter choice: "))

    conn = connect_to_db()
    cursor = conn.cursor()

    if choice == 1:
        emp_id = int(input("Enter employee ID: "))
        query = "SELECT * FROM employees WHERE id = %s"
        cursor.execute(query, (emp_id,))
    elif choice == 2:
        emp_name = input("Enter employee name: ")
        query = "SELECT * FROM employees WHERE name LIKE %s"
        cursor.execute(query, (f"%{emp_name}%",))
    else:
        print("Invalid choice.")
        return

    result = cursor.fetchall()

    if result:
        for row in result:
            print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}, Department: {row[3]}, Salary: {row[4]}")
    else:
        print("Employee not found.")

    cursor.close()
    conn.close()


# Menu
def main_menu():
    while True:
        print("\nEmployee Management System")
        print("1. Add New Employee")
        print("2. View Employees")
        print("3. Update Employee")
        print("4. Delete Employee")
        print("5. Search Employee")
        print("6. Exit")

        choice = int(input("Enter your choice: "))

        if choice == 1:
            add_employee()
        elif choice == 2:
            view_employees()
        elif choice == 3:
            update_employee()
        elif choice == 4:
            delete_employee()
        elif choice == 5:
            search_employee()
        elif choice == 6:
            print("Exiting program....")
            break
        else:
            print("Invalid choice so please choose again.")


# Code for start the program

print("Welcome to the Employee Management System")
while True:
        print("1. Login")
        print("2. Register New User")
        print("3. Exit")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            if login():
                main_menu()
        elif choice == 2:
            register_employee_user()
        elif choice == 3:
            print("Exiting the program.")
            break
        else:
            print("Invalid choice! Please try again.")
