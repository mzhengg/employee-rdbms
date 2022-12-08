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
        print("B - Add employee")
        print("C - View employee")
        print("D - Modify employee")
        print("E - Remove employee")
        print("F - Add dependent")
        print("G - Remove dependent")
        print("H - Add department")
        print("I - View department")
        print("J - Remove department")
        print("K - Add department location")
        print("L - Remove department location")
        print()

        user_input = input("Enter the operation letter: ")

        if user_input == "A":
            print("Closing menu")
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
            print("This is not a valid input")
            i = 0

        print()
        ans = input("Do you want to perform another operation? 'Yes' or 'No' ")

        if ans == "Yes":
            continue
        elif ans == "No":
            print("Closing menu")
            i = 0
        else:
            i = 0
            print("Not a valid input. Closing menu.")

def add_employee():
    cursor = connection.cursor()

    ssn = input("Enter employee SSN: ")
    fname, minit, lname = input("Enter employee full name: (first, middle, last) ").split()
    bdate = input("Enter employee birthdate: ")
    address = input("Enter employee address: ")
    sex = input("Enter employee sex: ")
    salary = input("Enter employee salary: ")
    super_ssn = input("Enter employee supervisor's SSN: (If none, then enter 'NULL') ")
    
    if super_ssn == 'NULL':
        super_ssn = None

    dno = input("Enter the employee's department number: ")

    try:
        data = (fname, minit, lname, ssn, bdate, address, sex, salary, super_ssn, dno)
        # insert new employee into table
        cursor.execute("INSERT INTO Employee VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", data)
        print("Employee successfully added!")
    except Error as err:
        print(f"Error: '{err}'")

    connection.commit()
    cursor.close()

def view_employee():
    cursor = connection.cursor()

    ssn = input("Enter employee SSN: ")

    # select all attributes of employee with that ssn
    cursor.execute("SELECT * FROM Employee WHERE Ssn = '%s'" % (ssn))
    emp_info = cursor.fetchall()

    if len(emp_info) == 0:
        return print("This employee does not exist!")

    # select supervisor's full name
    super_ssn = emp_info[0][8]
    cursor.execute("SELECT Fname, Minit, Lname FROM Employee WHERE Ssn = '%s'" % (super_ssn))
    super_name = cursor.fetchall()

    if len(super_name) == 0:
        super_name = "NULL"
        super_ssn = "NULL"
    else:
        super_name = " ".join(super_name[0])

    # select department name
    dno = emp_info[0][9]
    cursor.execute("SELECT Dname FROM Department WHERE Dnumber = '%s'" % (dno))
    dname = cursor.fetchall()

    # select dependent's name 
    cursor.execute("SELECT Dependent_name FROM Dependent WHERE Essn = '%s'" % (ssn))
    dep_names = cursor.fetchall()

    # display all the information
    if len(dep_names) > 1:
        dep_names = [entry[0] for entry in dep_names]
        dep_names = ", ".join(dep_names)
    elif len(dep_names) == 1:
        dep_names = dep_names[0][0]
    else: 
        dep_names = "NULL"

    print("Employee information: ")
    print("Name: " + emp_info[0][0] + " " + emp_info[0][1] + " " + emp_info[0][2])
    print("SSN: " + emp_info[0][3])
    print("Birthdate: " + str(emp_info[0][4]))
    print("Address: " + emp_info[0][5])
    print("Sex: " + emp_info[0][6])
    print("Salary: " + str(emp_info[0][7]))
    print("Supervisor's SSN: " + super_ssn)
    print("Department number: " + str(dno))
    print("Supervisor name: " + super_name)
    print("Department name: " + dname[0][0])
    print("Dependent names: ", dep_names)

    connection.commit()
    cursor.close()

def modify_employee():
    cursor = connection.cursor()

    ssn = input("Enter employee SSN: ")

    # select employee information and lock the record
    cursor.execute("SELECT * FROM Employee WHERE Ssn = '%s' FOR UPDATE" % (ssn))
    emp = cursor.fetchall()

    print("Employee information: ")
    print("Name: " + emp[0][0] + " " + emp[0][1] + " " + emp[0][2])
    print("SSN: " + emp[0][3])
    print("Birthdate: " + str(emp[0][4]))
    print("Address: " + emp[0][5])
    print("Sex: " + emp[0][6])
    print("Salary: " + str(emp[0][7]))
    print("Supervisor's SSN: " + str(emp[0][8]))
    print("Department number: " + str(emp[0][9]))

    i = 1

    while i != 0:
        print("Options: ")
        print("A - Quit")
        print("B - Address")
        print("C - Sex")
        print("D - Salary")
        print("E - Supervisor's SSN")
        print("F - Department number")

        ans = input("Which attribute do you want to update? Input the appropriate letter: ")

        if ans == "A":
            return
        elif ans == "B":
            address = input("Enter the new address: ")
            # update employee's address to the new address
            cursor.execute("UPDATE Employee SET address = '%s' WHERE ssn = '%s'" % (address, ssn))
            print("Address successfully updated!")
        elif ans == "C":
            sex = input("Enter the new sex: ")
            # update employee's sex to the new sex 
            cursor.execute("UPDATE Employee SET sex = '%s' WHERE ssn = '%s'" % (sex, ssn))
            print("Sex successfully updated!")
        elif ans == "D":
            salary = input("Enter the new salary: ")
            # update employee's salary to the new salary 
            cursor.execute("UPDATE Employee SET salary = '%s' WHERE ssn = '%s'" % (salary, ssn))
            print("Salary successfully updated!")
        elif ans == "E":
            super_ssn = input("Enter the new supervisor SSN: ")
            try:
                # update employee's super_ssn to the new super_ssn
                cursor.execute("UPDATE Employee SET Super_ssn = '%s' WHERE ssn = '%s'" % (super_ssn, ssn))
                print("Supervisor SSN successfully updated!")
            except Error as err:
                print(f"Error: '{err}'")
        elif ans == "F":
            dno = input("Enter the new department number: ")
            try:
                # update employee dno to the new dno 
                cursor.execute("UPDATE Employee SET dno = '%s' WHERE ssn = '%s'" % (dno, ssn))
                print("Department number successfully updated!")
            except Error as err:
                print(f"Error: '{err}'")
        else:
            return print("Error: Please input a valid option!")
        
        connection.commit()
        inp = input("Are there any other attributes you want to update? Type 'Yes' or 'No' ")
        
        if inp == "Yes":
            continue
        elif inp == "No":
            i = 0

    cursor.close()

def remove_employee():
    cursor = connection.cursor()

    ssn = input("Enter employee SSN: ")

    # retrieve employee information with that ssn and lock the row
    cursor.execute("SELECT * FROM Employee WHERE Ssn='%s' FOR UPDATE" % (ssn))
    emp_info = cursor.fetchall()

    try:
        print("Employee information: ")
        print("Name: " + emp_info[0][0] + " " + emp_info[0][1] + " " + emp_info[0][2])
        print("SSN: " + emp_info[0][3])
        print("Birthdate: " + str(emp_info[0][4]))
        print("Address: " + emp_info[0][5])
        print("Sex: " + emp_info[0][6])
        print("Salary: " + str(emp_info[0][7]))

        conf = input("Are you sure you want to delete this employee? Type 'Yes' or 'No'")
        if conf == "No":
            pass
        else:
            try:
                # delete employee with the given ssn from employee table
                cursor.execute("DELETE FROM Employee WHERE Ssn='%s'" % (ssn))
                print("Employee successfully removed!")
            except Error as err:
                print(f"Error: '{err}'")
                print("Please remove the necessary dependencies first!")
    except:
        return print("This employee does not exist!")

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
        emp_info = cursor.fetchall()
        print("Department information: ")
        print("Department name: " + emp_info[0][0])
        print("Department number: " + str(emp_info[0][1]))
        print("Manager SSN: " + emp_info[0][2])
        print("Manager start date (YYYY-MM-DD): " + str(emp_info[0][3]))

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