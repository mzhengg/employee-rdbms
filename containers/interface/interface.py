import os

import mysql.connector
from mysql.connector import Error

# login information
host = 'warehouse' # find in docker-compose.yml, line 5
port = '3306' # find in docker-compose.yml, line 13
user = os.getenv('MYSQL_USER') # get environmental variable
password = os.environ.get('MYSQL_PASSWORD') # get environmental variable
database = os.environ.get('MYSQL_DATABASE') # get environmental variable

# establish connection to mysql database
connection = mysql.connector.connect(user=user, password=password, host=host, port=port, database=database, auth_plugin='mysql_native_password')

def interface():
    i = 1

    while i != 0:
        print("Please select an operation to perform.")
        print()
        print("A - Quit Menu")
        print("B - Add Employee")
        print("C - View Employee")
        print("D - Modify Employee")
        print("E - Remove Employee")
        print("F - Add Dependent")
        print("G - Remove Dependent")
        print("H - Add Department")
        print("I - View Department")
        print("J - Remove Department")
        print("K - Add Department Location")
        print("L - Remove Department Location")
        print()

        user_input = input("Enter the operation letter: ")

        if user_input == "A":
            print("Closing menu...")
            i = 0

        elif user_input == "B":
            add_employee()

        elif user_input == "C":
            view_employee()

        elif user_input == "D":
            modify_employee()

        elif user_input == "E":
            remove_employee()

        elif user_input == "F":
            add_dependent()

        elif user_input == "G":
            remove_dependent()

        elif user_input == "H":
            add_department()

        elif user_input == "I":
            view_department()

        elif user_input == "J":
            remove_department()

        elif user_input == "K":
            add_department_location()

        elif user_input == "L":
            remove_department_location()

        else:
            print("This is not a valid input letter.")

        print()
        answer = input("Do you want to perform another operation? ('Yes' or 'No'): ")

        if answer == "Yes":
            continue

        elif answer == "No":
            print("Closing menu...")
            i = 0

        else:
            print("Not a valid input - closing menu...")
            i = 0

def add_employee():
    cursor = connection.cursor()

    ssn = input("Enter the employee's SSN: ")
    fname = input("Enter the employee's first name: ")
    minit = input("Enter the employee's middle inital: ")
    lname = input("Enter the employee's last name: ")
    bdate = input("Enter the employee's birthdate: ")
    address = input("Enter the employee's address: ")
    sex = input("Enter the employee's sex: ")
    salary = input("Enter the employee's salary: ")
    dno = input("Enter the employee's department number: ")
    super_ssn = input("Enter the employee's supervisor's SSN: (If none, then enter 'NULL') ")

    if super_ssn == 'NULL':
        super_ssn = None

    try:
        data = (fname, minit, lname, ssn, bdate, address, sex, salary, super_ssn, dno)

        # add employee to 'Employee' table
        cursor.execute("INSERT INTO EMPLOYEE VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", data)

        print("Employee successfully added!")

    except Error as err:
        print(f"Error: '{err}'")

    connection.commit()
    cursor.close()

def view_employee():
    cursor = connection.cursor()

    ssn = input("Enter the employee's SSN: ")

    # select all attributes of employee with that ssn
    cursor.execute("SELECT * FROM EMPLOYEE WHERE SSN = '%s'" % (ssn))
    employee_info = cursor.fetchall()

    if len(employee_info) == 0:
        return print("This employee doesn't exist!")

    # get supervisor's full name
    super_ssn = employee_info[0][8]
    cursor.execute("SELECT FNAME, MINIT, LNAME FROM EMPLOYEE WHERE SSN = '%s'" % (super_ssn))
    super_name = cursor.fetchall()

    if len(super_name) == 0:
        super_name = "NULL"
        super_ssn = "NULL"
    else:
        super_name = " ".join(super_name[0])

    # get department name
    dno = employee_info[0][9]
    cursor.execute("SELECT DNAME FROM DEPARTMENT WHERE DNUMBER = '%s'" % (dno))
    dname = cursor.fetchall()

    # select dependents' names 
    cursor.execute("SELECT DEPENDENT_NAME FROM DEPENDENT WHERE ESSN = '%s'" % (ssn))
    dependent_names = cursor.fetchall()

    # display all the information
    if len(dependent_names) > 1:
        dependent_names = [entry[0] for entry in dependent_names]
        dependent_names = ", ".join(dependent_names)

    elif len(dependent_names) == 1:
        dependent_names = dependent_names[0][0]

    else: 
        dependent_names = "NULL"

    print("Employee information: ")
    print("Name: " + employee_info[0][0] + " " + employee_info[0][1] + " " + employee_info[0][2])
    print("SSN: " + employee_info[0][3])
    print("Birthdate: " + str(employee_info[0][4]))
    print("Address: " + employee_info[0][5])
    print("Sex: " + employee_info[0][6])
    print("Salary: " + str(employee_info[0][7]))
    print("Supervisor SSN: " + super_ssn)
    print("Department number: " + str(dno))
    print("Supervisor name: " + super_name)
    print("Department name: " + dname[0][0])
    print("Dependent names: " + dependent_names)

    connection.commit()
    cursor.close()

def modify_employee():
    cursor = connection.cursor()

    ssn = input("Enter employee's SSN: ")

    # get employee information and lock the record
    cursor.execute("SELECT * FROM EMPLOYEE WHERE SSN = '%s' FOR UPDATE" % (ssn))
    employee_information = cursor.fetchall()

    print("Employee information: ")
    print("Name: " + employee_information[0][0] + " " + employee_information[0][1] + " " + employee_information[0][2])
    print("SSN: " + employee_information[0][3])
    print("Birthdate: " + str(employee_information[0][4]))
    print("Address: " + employee_information[0][5])
    print("Sex: " + employee_information[0][6])
    print("Salary: " + str(employee_information[0][7]))
    print("Supervisor SSN: " + str(employee_information[0][8]))
    print("Department number: " + str(employee_information[0][9]))

    i = 1

    while i != 0:
        print("Options: ")
        print("A - Quit")
        print("B - Address")
        print("C - Sex")
        print("D - Salary")
        print("E - Supervisor SSN")
        print("F - Department number")

        answer = input("Which attribute do you want to modify? Enter the appropriate letter: ")

        if answer == "A":
            return

        elif answer == "B":
            address = input("Enter the new address: ")

            # update employee's address to the new address
            cursor.execute("UPDATE EMPLOYEE SET ADDRESS = '%s' WHERE SSN = '%s'" % (address, ssn))
            print("Address successfully updated!")

        elif answer == "C":
            sex = input("Enter the new sex: ")

            # update employee's sex to the new sex 
            cursor.execute("UPDATE EMPLOYEE SET SEX = '%s' WHERE SSN = '%s'" % (sex, ssn))
            print("Sex successfully updated!")

        elif answer == "D":
            salary = input("Enter the new salary: ")

            # update employee's salary to the new salary 
            cursor.execute("UPDATE EMPLOYEE SET SALARY = '%s' WHERE SSN = '%s'" % (salary, ssn))
            print("Salary successfully updated!")

        elif answer == "E":
            super_ssn = input("Enter the new supervisor SSN: ")

            try:
                # update employee's supervisor ssn to the new supervisor ssn
                cursor.execute("UPDATE EMPLOYEE SET SUPER_SSN = '%s' WHERE SSN = '%s'" % (super_ssn, ssn))
                print("Supervisor SSN successfully updated!")

            except Error as err:
                print(f"Error: '{err}'")

        elif answer == "F":
            dno = input("Enter the new department number: ")

            try:
                # update employee department number to the new department number
                cursor.execute("UPDATE EMPLOYEE SET DNO = '%s' WHERE SSN = '%s'" % (dno, ssn))
                print("Department number successfully updated!")

            except Error as err:
                print(f"Error: '{err}'")

        else:
            print("This is not a valid input letter.")
        
        connection.commit()
        answer = input("Do you want to perform another operation? ('Yes' or 'No'): ")
        
        if answer == "Yes":
            continue

        elif answer == "No":
            i = 0

    cursor.close()

def remove_employee():
    cursor = connection.cursor()

    ssn = input("Enter employee SSN: ")

    # get employee information and lock the record
    cursor.execute("SELECT * FROM EMPLOYEE WHERE SSN='%s' FOR UPDATE" % (ssn))
    employee_information = cursor.fetchall()

    try:
        print("Employee information: ")
        print("Name: " + employee_information[0][0] + " " + employee_information[0][1] + " " + employee_information[0][2])
        print("SSN: " + employee_information[0][3])
        print("Birthdate: " + str(employee_information[0][4]))
        print("Address: " + employee_information[0][5])
        print("Sex: " + employee_information[0][6])
        print("Salary: " + str(employee_information[0][7]))

        answer = input("Are you sure you want to delete this employee? Type 'Yes' or 'No': ")

        if answer == "No":
            pass

        else:
            try:
                # delete employee from EMPLOYEE table
                cursor.execute("DELETE FROM EMPLOYEE WHERE SSN='%s'" % (ssn))
                print("Employee successfully removed!")

            except Error as err:
                print(f"Error: '{err}'")
                print("Please remove the dependents in the DEPENDENT table first!")

    except:
        return print("This employee doesn't exist!")

    connection.commit()
    cursor.close()

def add_dependent():
    cursor = connection.cursor()

    ssn = input("Enter Employee SSN: ")

    # check if employee ssn exists
    cursor.execute("SELECT * FROM Employee WHERE Ssn='%s'", ssn)
    emp = cursor.fetchall()
    if len(emp) == 0:
        return print("This employee does not exist!")

    # selects all dependents assosicated with that ssn and lock the row
    cursor.execute("SELECT * FROM Dependent WHERE Essn='%s' FOR UPDATE" % (ssn))
    dep = cursor.fetchall()
    
    if len(dep) == 0:
        return print("This employee does not have any dependents!")
    else:
        print("Dependent information: ")
        for t in dep:
            print("Name: " + t[1])
            print("Sex: " + t[2])
            print("Birthdate: " + str(t[3]))
            print("Relationship: " + t[4])
            print()

    # adds new dependent information to dependent table
    dep_name = input("Enter the dependent's first name: ")
    sex = input("Enter the dependent's sex: ")
    bdate = input("Enter the dependent's birthdate: (YYYY-MM-DD) ")
    relationship = input("Enter the dependent's relationship to the employee: ")
    
    data = (ssn, dep_name, sex, bdate, relationship)
    # check if the dependent already exists in the table
    cursor.execute("SELECT * FROM Dependent WHERE Essn='%s' AND Dependent_name='%s' AND Sex='%s' AND Bdate='%s' AND Relationship='%s'" % (data))

    if len(cursor.fetchall()) > 0:
        return print("This dependent already exists in the table!")
    else:
        # since they are not in the table, add the dependent to the table
        cursor.execute("INSERT INTO Dependent VALUES (%s, %s, %s, %s, %s)", data)
        print("Dependent successfully added!")

    connection.commit()
    cursor.close()

def remove_dependent():
    cursor = connection.cursor()

    ssn = input("Enter employee SSN: ")

    # selects all dependents assosicated with that ssn
    cursor.execute("SELECT * FROM Dependent WHERE Essn='%s' FOR UPDATE" % (ssn))
    dep = cursor.fetchall()

    if len(dep) == 0:
        return print("This employee does not have any dependents!")
    else:
        print("Dependent information: ")
        for t in dep:
            print("Name: " + t[1])
            print("Sex: " + t[2])
            print("Birthdate: " + str(t[3]))
            print("Relationship: " + t[4])
            print()

    dep_name = input("Enter the first name of the dependent to be removed: ")

    # check if dependent exists
    cursor.execute("SELECT * FROM Dependent WHERE Essn = '%s' AND Dependent_name = '%s'" % (ssn, dep_name))
    if len(cursor.fetchall()) == 0:
        return print("This dependent does not exist in the table!")
    else:
        # delete the dependent from the dependent table
        cursor.execute("DELETE FROM Dependent WHERE Dependent_name = '%s'" % (dep_name))
        print("Dependent successfully removed!")

    connection.commit()
    cursor.close()

def add_department():
    cursor = connection.cursor()

    dname = input("Enter the department name: ")
    dnumber = input("Enter the department number: ")
    mgr_ssn = input("Enter the manager SSN: ")
    mgr_start_date = input("Enter the manager start date: (YYYY-MM-DD) ")
    
    try:
        data = (dname, dnumber, mgr_ssn, mgr_start_date)
        cursor.execute("INSERT INTO Department VALUES ('%s','%s','%s','%s')" % (data))
        print("Department successfully added!")
    except Error as err:
        print(f"Error: '{err}'")

    connection.commit()
    cursor.close()

def view_department():
    cursor = connection.cursor()

    dnumber = input("Enter department number: ")

    # select department information with the given department number
    cursor.execute("SELECT Dname, Mgr_ssn FROM Department WHERE Dnumber = '%s'" % (dnumber))
    dept_info = cursor.fetchall()
    
    if len(dept_info) == 0:
        return print("This is an invalid department number!")
    
    # select the department supervisor's name 
    mgr_ssn = dept_info[0][1]
    cursor.execute("SELECT Fname, Minit, Lname FROM Employee WHERE Ssn = '%s'" % (mgr_ssn))
    mgr_info = cursor.fetchall()

    # statement the location(s) of that department
    cursor.execute("SELECT Dlocation FROM Dept_locations WHERE Dnumber = '%s'" % (dnumber))
    dept_loc = cursor.fetchall()

    # make it look nicer
    print()
    print("Department information: ")
    print("Department: " + dept_info[0][0])
    print("Department manager: " + " ".join(mgr_info[0]))
    print("Department location(s): " + " ".join(dept_loc[0]))

    connection.commit()
    cursor.close()

def remove_department():
    cursor = connection.cursor()

    dnumber = input("Enter department number: ")

    try:
        # retrieve information about the department with that department number and lock the row
        cursor.execute("SELECT * FROM Department WHERE Dnumber='%s' FOR UPDATE" % (dnumber))
        employee_info = cursor.fetchall()
        print("Department information: ")
        print("Department name: " + employee_info[0][0])
        print("Department number: " + str(employee_info[0][1]))
        print("Manager SSN: " + employee_info[0][2])
        print("Manager start date (YYYY-MM-DD): " + str(employee_info[0][3]))

        conf = input("Are you sure you want to delete this department? ")

        if conf == "No":
            pass
        else:
            try:
                # delete the department with that department number
                cursor.execute("DELETE FROM Department WHERE Dnumber='%s'" % (dnumber))
                print("Department successfully removed!")
            except Error as err:
                print(f"Error: '{err}'")
                print("Please remove the necessary dependencies first!")
    except:
        return print("This department number does not exist!")

    connection.commit()
    cursor.close()

def add_department_location():
    cursor = connection.cursor()
    
    dnum = input("Enter department number? ")

    # select all department locations for that department number and lock the row
    cursor.execute("SELECT Dlocation FROM Dept_locations WHERE Dnumber='%s' FOR UPDATE" % (dnum))
    loc_info = cursor.fetchall()

    if len(loc_info) == 0:
        return print("This department number does not exist!")
    else:
        loc_list = [loc[0] for loc in loc_info]
        print("Department locations: " + ", ".join(loc_list))

    new_loc = input("Enter new department location: ")

    try:
        # insert new location for that department number into table
        cursor.execute("INSERT INTO Dept_locations VALUES ('%s', '%s')" % (dnum, new_loc))
        connection.commit()
        cursor.close()
        return print("Department location successfully added!")
    except Error as err:
        print(f"Error: '{err}'")
        print("This department location already exists!")
    
    connection.commit()
    cursor.close()

def remove_department_location():
    cursor = connection.cursor()

    dno = input("Enter the department number: ")

    # select all department locations for that department number and lock the row(s)
    cursor.execute("SELECT Dlocation FROM Dept_locations WHERE Dnumber='%s' FOR UPDATE" % (dno))
    dept_loc = cursor.fetchall()

    if len(dept_loc) == 0:
        return print("This department number does not exist!")
    else:
        dept_loc_list = [loc[0] for loc in dept_loc]
        print("Department locations: " +  ", ".join(dept_loc_list))
        
        rem_location = input("Which location do you want to remove? ")

        if rem_location in dept_loc_list:
            # delete the specified department location from that department
            cursor.execute("DELETE FROM Dept_locations WHERE Dlocation ='%s' and Dnumber = '%s'" % (rem_location, dno))
            print("Department location successfully removed!")
        else:
            print("This location is not a valid entry!")

    connection.commit()
    cursor.close()

if __name__ == '__main__':
    database = interface()
    connection.close()