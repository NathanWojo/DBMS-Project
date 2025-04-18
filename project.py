import mysql.connector
from tabulate import tabulate
import sys 
import traceback
import logging

mysql_username = 'nawojtow'
mysql_passwork = 'Iox4quai'

def open_database(hostname, user_name, mysql_pw, database_name):
    global conn
    conn = mysql.connector.connect(host=hostname,
                                   user=user_name,
                                   password=mysql_pw,
                                   database=database_name
                                   )
    global cursor
    cursor = conn.cursor()

def printFormat(result):
    header = []
    for cd in cursor.description:  # get headers
        header.append(cd[0])
    print('')
    print('Query Result:')
    print('')
    return(tabulate(result, headers=header))  # print results in table format

def executeSelect(query):
    cursor.execute(query)
    res = printFormat(cursor.fetchall())
    return res

def executeUpdate(query):  # use this function for delete and update
    cursor.execute(query)
    conn.commit()

def close_db():  # use this function to close db
    cursor.close()
    conn.close()

#add driver
def addDriver(driverID, name, age):
    try:
        query = """
        insert into Driver (driverID, name, age)
        values (%s, %s, %s)
        """
        cursor.execute(query, (driverID, name, age))
        conn.commit()
        print(f"Driver {name.strip()} added")
    except mysql.connector.Error as err:
        print(f"Womp womp: failed to add")

#add pass, make sure 2 axles maps to 3.99 and 3 axles maps to 5.99
def addPass(passID, licensePlate, driverID, plazaNumber, passDate, passTime, cost):
    try:
        query1 = """
        select axles, driverID from Vehicle
        where licensePlate = %s
        """
        cursor.execute(query1, (licensePlate,))
        vehicle = cursor.fetchone()
        if not vehicle:
            print(f"Womp womp: vehicle with license plate {licensePlate} does not exist")
            return

        axleCount, vehicleID = vehicle

        if driverID != vehicleID:
            print(f"Womp womp: driver {driverID} is not assigned to vehicle {licensePlate}")
            return

        if axleCount == 2 and cost != 3.99:
            print("Womp womp: cost must be 3.99 for 2-axle vehicles")
            return
        elif axleCount == 3 and cost != 5.99:
            print("Womp womp: cost must be 5.99 for 3-axle vehicles")
            return

        query2 = """
        select 1 from Plaza
        where plazaNumber = %s
        """
        cursor.execute(query2, (plazaNumber,))
        if cursor.fetchone() is None:
            print(f"Womp womp: plaza {plazaNumber} does not exist")
            return

        query3 = """
            insert into Pass (passID, licensePlate, driverID, plazaNumber, passDate, passTime, cost)
            values (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query3, (passID, licensePlate, driverID, plazaNumber, passDate, passTime, cost))
        conn.commit()
        print(f"Pass {passID} added")

    except mysql.connector.Error as err:
        print(f"Womp womp: failed to add")

def listPasses(plazaNumber):
    try:
        query = """
        select Pass.passID, Driver.name as driverName, Pass.licensePlate, Pass.passDate, Pass.passTime, Pass.cost
        from Pass
        join Driver on Pass.driverID = Driver.driverID
        wehre Pass.plazaNumber = %s
        order by Driver.name asc
        """
        cursor.execute(query, (plazaNumber,))
        result = cursor.fetchall()
        if not result:
            print(f"Womp womp: no passes found at plaza {plazaNumber}")
            return
        print(printFormat(result))

    except mysql.connector.Error as err:
        print(f"Womp womp: failed to list")

def main():
    while True:
        break

if __name__ == "main":
    main()