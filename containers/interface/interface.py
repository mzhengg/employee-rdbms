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

            except:
                print("Please remove the dependents in the DEPENDENT table first!")

    except:
        return print("This employee doesn't exist!")

    connection.commit()
    cursor.close()

def add_dependent():
    cursor = connection.cursor()

    ssn = input("Enter employee SSN: ")

    # check if employee ssn exists
    cursor.execute("SELECT * FROM EMPLOYEE WHERE SSN='%s'", ssn)
    employee = cursor.fetchall()

    if len(employee) == 0:
        return print("This employee doesn't exist!")

    # get all dependents assosicated with the employee and lock the record
    cursor.execute("SELECT * FROM DEPENDENT WHERE ESSN='%s' FOR UPDATE" % (ssn))
    dependents = cursor.fetchall()
    
    if len(dependents) == 0:
        return print("This employee doesn't have any dependents!")

    else:
        print("Dependent information: ")

        for d in dependents:
            print("Name: " + d[1])
            print("Sex: " + d[2])
            print("Birthdate: " + str(d[3]))
            print("Relationship: " + d[4])
            print()

    # get new dependent information
    dependent_name = input("Enter the dependent's first name: ")
    sex = input("Enter the dependent's sex: ")
    bdate = input("Enter the dependent's birthdate: (YYYY-MM-DD) ")
    relationship = input("Enter the dependent's relationship to the employee: ")
    
    data = (ssn, dependent_name, sex, bdate, relationship)

    # check if the dependent already exists in DEPENDENT table
    cursor.execute("SELECT * FROM DEPENDENT WHERE ESSN='%s' AND DEPENDENT_NAME='%s' AND SEX='%s' AND BDATE='%s' AND RELATIONSHIP='%s'" % (data))

    if len(cursor.fetchall()) > 0:
        return print("This dependent already exists in the table!")

    else:
        # not in table, add the new dependent to DEPENDENT table
        cursor.execute("INSERT INTO DEPENDENT VALUES (%s, %s, %s, %s, %s)", data)
        print("Dependent successfully added!")

    connection.commit()
    cursor.close()

def remove_dependent():
    cursor = connection.cursor()

    ssn = input("Enter employee SSN: ")

    # get all dependents assosicated with the employee and lock the record
    cursor.execute("SELECT * FROM DEPENDENT WHERE ESSN='%s' FOR UPDATE" % (ssn))
    dependents = cursor.fetchall()

    if len(dependents) == 0:
        return print("This employee doesn't have any dependents!")

    else:
        print("Dependent information: ")
        
        for d in dependents:
            print("Name: " + d[1])
            print("Sex: " + d[2])
            print("Birthdate: " + str(d[3]))
            print("Relationship: " + d[4])
            print()

    dependent_fname = input("Enter the first name of the dependent to be removed: ")

    # check if dependent exists
    cursor.execute("SELECT * FROM DEPENDENT WHERE ESSN = '%s' AND DEPENDENT_NAME = '%s'" % (ssn, dependent_fname))
    
    if len(cursor.fetchall()) == 0:
        return print("This dependent doesn't exist in the table!")

    else:
        # delete the dependent from the DEPENDENT table
        cursor.execute("DELETE FROM DEPENDENT WHERE DEPENDENT_NAME = '%s'" % (dependent_fname))
        print("Dependent successfully removed!")

    connection.commit()
    cursor.close()

def add_department():
    cursor = connection.cursor()

    department_name = input("Enter the department name: ")
    department_number = input("Enter the department number: ")
    mgr_ssn = input("Enter the manager SSN: ")
    mgr_start_date = input("Enter the manager start date: (YYYY-MM-DD) ")
    
    try:
        data = (department_name, department_number, mgr_ssn, mgr_start_date)
        cursor.execute("INSERT INTO DEPARTMENT VALUES ('%s','%s','%s','%s')" % (data))
        
        print("Department successfully added!")

    except Error as err:
        print(f"Error: '{err}'")

    connection.commit()
    cursor.close()

def view_department():
    cursor = connection.cursor()

    department_number = input("Enter department number: ")

    # get department information from the department number
    cursor.execute("SELECT DNAME, MGR_SSN FROM DEPARTMENT WHERE DNUMBER = '%s'" % (department_number))
    dept_info = cursor.fetchall()
    
    if len(dept_info) == 0:
        return print("This is an invalid department number!")
    
    # get the department supervisor's name 
    mgr_ssn = dept_info[0][1]
    cursor.execute("SELECT FNAME, MINIT, LNAME FROM EMPLOYEE WHERE SSN = '%s'" % (mgr_ssn))
    mgr_info = cursor.fetchall()

    # get the location(s) of the department
    cursor.execute("SELECT DLOCATION FROM DEPT_LOCATIONS WHERE DNUMBER = '%s'" % (department_number))
    dept_loc = cursor.fetchall()

    print("Department information: ")
    print("Department: " + dept_info[0][0])
    print("Department manager: " + " ".join(mgr_info[0]))
    print("Department location(s): " + ", ".join(dept_loc[0]))

    connection.commit()
    cursor.close()

def remove_department():
    cursor = connection.cursor()

    department_number = input("Enter department number: ")

    try:
        # get department information from the department number and lock the record
        cursor.execute("SELECT * FROM DEPARTMENT WHERE DNUMBER='%s' FOR UPDATE" % (department_number))
        dept_info = cursor.fetchall()

        print("Department information: ")
        print("Department name: " + dept_info[0][0])
        print("Department number: " + str(dept_info[0][1]))
        print("Manager SSN: " + dept_info[0][2])
        print("Manager start date: " + str(dept_info[0][3]))

        answer = input("Are you sure you want to delete this department? ")

        if answer == "No":
            pass

        else:
            try:
                # delete the department with the department number
                cursor.execute("DELETE FROM DEPARTMENT WHERE DNUMBER='%s'" % (department_number))
                print("Department successfully removed!")

            except:
                print("Please remove the projects in the PROJECT table and the department locations in the DEPT_LOCATIONS table first!")

    except:
        return print("This department number doesn't exist!")

    connection.commit()
    cursor.close()

def add_department_location():
    cursor = connection.cursor()
    
    dnum = input("Enter department number: ")

    # get department locations for the department number and lock the record
    cursor.execute("SELECT DLOCATION FROM DEPT_LOCATIONS WHERE DNUMBER='%s' FOR UPDATE" % (dnum))
    dept_locations = cursor.fetchall()

    if len(dept_locations) == 0:
        return print("This department number doesn't exist!")

    else:
        dept_locations_list = [loc[0] for loc in dept_locations]
        print("Department is currently located in these locations: " + ", ".join(dept_locations_list))

    new_dept_location = input("Enter new department location: ")

    try:
        # add new department location for the department number into DEPT_LOCATIONS table
        cursor.execute("INSERT INTO DEPT_LOCATIONS VALUES ('%s', '%s')" % (dnum, new_dept_location))
        print("Department location successfully added!")

    except:
        print("This department location already exists!")
    
    connection.commit()
    cursor.close()

def remove_department_location():
    cursor = connection.cursor()

    dept_number = input("Enter the department number: ")

    # get department locations for the department number and lock the record
    cursor.execute("SELECT DLOCATION FROM DEPT_LOCATIONS WHERE DNUMBER='%s' FOR UPDATE" % (dept_number))
    dept_locations = cursor.fetchall()

    if len(dept_locations) == 0:
        return print("This department number doesn't exist!")

    else:
        dept_locations_list = [loc[0] for loc in dept_locations]
        print("Department is currently located in these locations: " +  ", ".join(dept_locations_list))
        
        dept_location_to_remove = input("Enter department location to remove: ")

        if dept_location_to_remove in dept_locations_list:
            # delete the department location from the DEPT_LOCATIONS table
            cursor.execute("DELETE FROM DEPT_LOCATIONS WHERE DLOCATION ='%s' and DNUMBER = '%s'" % (dept_location_to_remove, dept_number))
            print("Department location successfully removed!")

        else:
            print("This department location is not a valid entry!")

    connection.commit()
    cursor.close()

if __name__ == '__main__':
    interface()
    connection.close()