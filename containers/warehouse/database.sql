/* create airflow user */
CREATE USER 'airflow'@'%';
GRANT ALL PRIVILEGES ON *.* TO 'airflow'@'%' WITH GRANT OPTION;

/* create tables */
CREATE TABLE WAREHOUSE.EMPLOYEE (
  /* variables */
  FNAME VARCHAR(15) NOT NULL,
  MINIT CHAR, 
  LNAME VARCHAR(15) NOT NULL,
  SSN CHAR(9) NOT NULL,
  BDATE DATE,
  ADDRESS VARCHAR(30),
  SEX CHAR,
  SALARY DECIMAL(10, 2),
  SUPER_SSN CHAR(9), 
  DNO INT NOT NULL,

  /* constraints */
  PRIMARY KEY (SSN)
  );

-- foreign keys can't be added until table we are referencing has been created
ALTER TABLE WAREHOUSE.EMPLOYEE ADD FOREIGN KEY (SUPER_SSN) REFERENCES WAREHOUSE.EMPLOYEE(SSN);

CREATE TABLE WAREHOUSE.DEPARTMENT (
  /* variables */
  DNAME VARCHAR(15) NOT NULL,
  DNUMBER INT NOT NULL,
  MGR_SSN CHAR(9) NOT NULL,
  MGR_START_DATE DATE,

  /* constraints */
  PRIMARY KEY (DNUMBER),
  UNIQUE (DNAME),
  FOREIGN KEY (MGR_SSN) REFERENCES EMPLOYEE(SSN)
  );

-- foreign keys can't be added until table we are referencing has been created
ALTER TABLE WAREHOUSE.EMPLOYEE ADD FOREIGN KEY (DNO) REFERENCES WAREHOUSE.DEPARTMENT(DNUMBER);

CREATE TABLE WAREHOUSE.DEPT_LOCATIONS (
  /* variables */
  DNUMBER INT NOT NULL,
  DLOCATION VARCHAR(15) NOT NULL,

  /* constraints */
  PRIMARY KEY (DNUMBER, DLOCATION),
  FOREIGN KEY (DNUMBER) REFERENCES DEPARTMENT(DNUMBER)
  );

CREATE TABLE WAREHOUSE.PROJECT (
  /* variables */
  PNAME VARCHAR(15) NOT NULL,
  PNUMBER INT NOT NULL,
  PLOCATION VARCHAR(15),
  DNUM INT NOT NULL,

  /* constraints */
  PRIMARY KEY (PNUMBER),
  UNIQUE (PNAME),
  FOREIGN KEY (DNUM) REFERENCES DEPARTMENT(DNUMBER) 
  );

CREATE TABLE WAREHOUSE.WORKS_ON (
  /* variables */
  ESSN CHAR(9) NOT NULL,
  PNO INT NOT NULL,
  HOURS DECIMAL(3, 1) NOT NULL,

  /* constraints */
  PRIMARY KEY (ESSN, PNO),
  FOREIGN KEY (ESSN) REFERENCES EMPLOYEE(SSN),
  FOREIGN KEY (PNO) REFERENCES PROJECT(PNUMBER) 
  ); 

CREATE TABLE WAREHOUSE.DEPENDENT (
  /* variables */
  ESSN CHAR(9) NOT NULL,
  DEPENDENT_NAME VARCHAR(15) NOT NULL,
  SEX CHAR,
  BDATE DATE,
  RELATIONSHIP VARCHAR(8),

  /* constraints */
  PRIMARY KEY (ESSN, DEPENDENT_NAME),
  FOREIGN KEY (ESSN) REFERENCES EMPLOYEE(SSN) 
  );

/* CONFUSION: don't know why foreign keys need to be dropped for insertion to work */
ALTER TABLE WAREHOUSE.EMPLOYEE DROP FOREIGN KEY employee_ibfk_1;
ALTER TABLE WAREHOUSE.EMPLOYEE DROP FOREIGN KEY employee_ibfk_2;

/* populate the database with dummy data */

/* insert records into `EMPLOYEE` table */
INSERT INTO `WAREHOUSE`.`EMPLOYEE` VALUES  
('John', 'B', 'Smith', '123456789', '1965-01-09', '731 Fondren, Houston, TX', 'M', '30000', '333445555', '5'),
('Franklin', 'T', 'Wong', '333445555', '1955-12-08', '638 Voss, Houston, TX', 'M', '40000', '888665555', '5'),
('Alicia', 'J', 'Zelaya', '999887777', '1968-01-19', '3321 Castle, Spring, TX', 'F', '25000', '987654321', '4'),
('Ramesh', 'K', 'Narayan', '666884444', '1962-09-15', '975 Fire Oak, Humble, TX', 'M', '38000', '333445555', '5'),
('Joyce', 'A', 'English', '453453453', '1972-07-31', '5631 Rice, Houston, TX', 'F', '25000', '333445555', '5'),
('Ahmad', 'V', 'Jabbar', '987987987', '1969-03-29', '980 Dallas, Houston, TX', 'M', '25000', '987654321', '4'),
('James', 'E', 'Borg', '888665555', '1937-11-10', '450 Stone, Houston, TX', 'M', '55000', NULL, '1'),
('Jennifer', 'S', 'Wallace', '987654321', '1941-06-20', '291 Berry, Bellaire, TX', 'F', '43000', '888665555', '4');

/* insert records into `DEPARTMENT` table */
INSERT INTO `WAREHOUSE`.`DEPARTMENT` VALUES 
('Research', '5', '333445555', '1988-05-22'), 
('Administration', '4', '987654321', '1995-01-01'), 
('Headquarters', '1', '888665555', '1981-06-19');

/* insert records into `DEPT_LOCATIONS` table */
INSERT INTO `WAREHOUSE`.`DEPT_LOCATIONS` VALUES
('5', 'Houston'),
('1', 'Houston'),
('4', 'Stafford'),
('5', 'Bellaire'),
('5', 'Sugarla');

/* insert records into `PROJECT` table */
INSERT INTO `WAREHOUSE`.`PROJECT` VALUES
('ProductX', '1', 'Bellaire', '5'),
('ProductY', '2', 'Sugarland', '5'),
('ProductZ', '3', 'Houston', '5'),
('Computerization', '10', 'Stafford', '4'),
('Reorganization', '20', 'Houston', '1'),
('Newbenefits', '30', 'Stafford', '4');
 
/* insert records into `DEPENDENT` table */
INSERT INTO `WAREHOUSE`.`DEPENDENT` VALUES
('333445555', 'Alice', 'F', '1986-04-05', 'Daughter'),
('333445555', 'Theodore', 'M', '1983-10-25', 'Son'),
('333445555', 'Joy', 'F', '1958-05-03', 'Spouse'),
('987654321', 'Abner', 'M', '1942-02-28', 'Spouse'),
('123456789', 'Michael', 'M', '1988-01-04', 'Son'),
('123456789', 'Alice', 'F', '1988-12-30', 'Daughter'),
('123456789', 'Elizabeth', 'F', '1967-05-05', 'Spouse');

/* insert records into `WORKS_ON` table */
INSERT INTO `WAREHOUSE`.`WORKS_ON` VALUES
('123456789', '1', '32.5'),
('123456789', '2', '7.5'),
('666884444', '3', '40.0'),
('453453453', '1', '20.0'),
('453453453', '2', '20.0'),
('333445555', '2', '10.0'),
('333445555', '3', '10.0'),
('333445555', '10', '10.0'),
('333445555', '20', '10.0'),
('999887777', '30', '30.0'),
('999887777', '10', '10.0'),
('987987987', '10', '35.0'),
('987987987', '30', '5.0'),
('987654321', '30', '20.0'),
('987654321', '20', '15.0'),
('888665555', '20', '25.0');