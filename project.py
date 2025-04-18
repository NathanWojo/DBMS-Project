import mysql.connector
from tabulate import tabulate
import sys 
import traceback
import logging
import argparse

mysql_username = 'stephenn'
mysql_password = 'Lohmoa4a'

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
    print('\nQuery Result:')
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
        print(f"\nDriver {name.strip()} added")
    except mysql.connector.Error as err:
        print(f"\nWomp womp: failed to add")

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
            print(f"\nWomp womp: vehicle with license plate {licensePlate} does not exist")
            return

        axleCount, vehicleID = vehicle

        if driverID != vehicleID:
            print(f"\nWomp womp: driver {driverID} is not assigned to vehicle {licensePlate}")
            return

        if axleCount == 2 and cost != 3.99:
            print("\nWomp womp: cost must be 3.99 for 2-axle vehicles")
            return
        elif axleCount == 3 and cost != 5.99:
            print("\nWomp womp: cost must be 5.99 for 3-axle vehicles")
            return

        query2 = """
            select 1 from Plaza
            where plazaNumber = %s
        """
        cursor.execute(query2, (plazaNumber,))
        if cursor.fetchone() is None:
            print(f"\nWomp womp: plaza {plazaNumber} does not exist")
            return

        query3 = """
            insert into Pass (passID, licensePlate, driverID, plazaNumber, passDate, passTime, cost)
            values (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query3, (passID, licensePlate, driverID, plazaNumber, passDate, passTime, cost))
        conn.commit()
        print(f"\nPass {passID} added")

    except mysql.connector.Error as err:
        print(f"\nWomp womp: failed to add")

#list all passes ordered by driver name
def listPasses(plazaNumber):
    try:
        query = """
            select Pass.passID, Driver.name as driverName, Pass.licensePlate, Pass.passDate, Pass.passTime, Pass.cost
            from Pass
            join Driver on Pass.driverID = Driver.driverID
            where Pass.plazaNumber = %s
            order by Driver.name asc
        """
        cursor.execute(query, (plazaNumber,))
        result = cursor.fetchall()
        if not result:
            print(f"\nWomp womp: no passes found at plaza {plazaNumber}")
            return
        print(printFormat(result))

    except mysql.connector.Error as err:
        print(f"\nWomp womp: failed to list")

#list all vehicles ordered by license plate, and display most recent pass the vehicle has made
def listVehicles():
    try:
        query = """
            select 
            V.licensePlate, V.make, V.model, V.axles, 
            D.name as driverName, P.passDate, P.passTime, P.cost, P.plazaNumber
            from Vehicle V
            join Driver D on V.driverID = D.DriverID
            left join (
            select p1.*
            from Pass p1
            inner join (
            select licensePlate, max(concat(passDate, ' ', passTime)) as latestPass
            from Pass
            group by licensePlate
            ) latest on p1.licensePlate = latest.licensePlate
            and concat(p1.passDate, ' ', p1.passTime) = latest.latestPass
            ) P on V.licensePlate = P.licensePlate
            order by V.licensePlate asc
        """
        cursor.execute(query)
        result = cursor.fetchall()
        print(printFormat(result))

    except mysql.connector.Error as err:
        print(f"\nWomp womp: failed to list")

#list all drivers that have 2 axled vehicles
def listDrivers():
    try:
        query = """
            select distinct D.driverID, D.name, D.age
            from Driver D
            join Vehicle V ON D.driverID = V.driverID
            where V.axles = 2
            order by D.name asc
        """
        cursor.execute(query)
        result = cursor.fetchall()
        if not result:
            print("\nWomp womp: no drivers with 2-axled vehicles")
            return
        print(printFormat(result))

    except mysql.connector.Error as err:
        print(f"\nWomp womp: failed to list")
        
#list all plazas visited by given driver, sorted by state
def listPlazas(name):
    try:
        query = """
            select distinct Plaza.plazaNumber, Plaza.state
            from Driver
            join Pass on Driver.driverID = Pass.driverID
            join Plaza on Pass.plazaNumber = Plaza.plazaNumber
            where Driver.name = %s
            order by Plaza.state asc
        """
        cursor.execute(query, (name,))
        result = cursor.fetchall()
        if not result:
            print("Womp womp: {name} has not been to any plazas")
            return
        print(printFormat(result))
        
    except mysql.connector.Error as err:
        print(f"\nWomp womp: failed to list")

#report showing num unique vehicles, num passes, num drivers, and total money collected
def plazaReport(plazaNumber):
    try:
        query1 = """
            select
            P.plazaNumber, P.state,
            count(distinct Pass.licensePlate) as uniqueVehicles,
            count(Pass.passID) as totalPasses,
            count(distinct Pass.driverID) as uniqueDrivers,
            sum(Pass.cost) as totalRevenue
            from Plaza P
            left join Pass on P.plazaNumber = Pass.plazaNumber
            where P.plazaNumber = %s
            group by P.plazaNumber, P.state
        """
        cursor.execute(query1, (plazaNumber,))
        result = cursor.fetchall()
        if not result:
            print(f"\nWomp womp: no data for plaza {plazaNumber}")
            return
        
        print(f"\n--- Pass Summary for Plaza {plazaNumber} ---")
        print(printFormat(result))

        query2 = """
            select
            count(distinct Pass.licensePlate) as uniqueVehicles,
            count(Pass.passID) as totalPasses,
            count(distinct Pass.driverID) as uniqueDrivers,
            sum(Pass.cost) as totalRevenue
            from Pass
            where plazaNumber = %s
        """
        cursor.execute(query2, (plazaNumber,))
        result = cursor.fetchone()

        print("\n--- Summary for Plaza ---")
        print(tabulate([result], headers=["totalUniqueVehicles", "totalPasses", "totalUniqueDrivers", "totalRevenue"]))

    except mysql.connector.Error as err:
        print(f"\nWomp womp: failed to list")

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='cmd')

    # add driver sub command
    p = sub.add_parser('add_driver')
    p.add_argument('driver_id')
    p.add_argument('name')
    p.add_argument('age', type=int)

    # add pass sub command
    p2 = sub.add_parser('add_pass')
    p2.add_argument('pass_id')
    p2.add_argument('license_plate')
    p2.add_argument('driver_id')
    p2.add_argument('plaza_number')
    p2.add_argument('pass_date')
    p2.add_argument('pass_time')
    p2.add_argument('cost', type=float)

    p3 = sub.add_parser('view_passes')
    p3.add_argument('plaza_number')

    p4 = sub.add_parser('view_vehicles')

    p5 = sub.add_parser('view_drivers')

    p6 = sub.add_parser('view_plazas')
    p6.add_argument('name')

    p7 = sub.add_parser('plaza_report')
    p7.add_argument('plaza_number')

    args = parser.parse_args()

    open_database('localhost', mysql_username, mysql_password, mysql_username)

    try:
        # commands
        if args.cmd == 'add_driver':
            addDriver(args.driver_id, args.name, args.age)
 
        elif args.cmd == 'add_pass':
            addPass(args.pass_id, args.license_plate, args.driver_id, args.plaza_number, args.pass_date, args.pass_time, args.cost)
        
        elif args.cmd == 'view_passes':
            listPasses(args.plaza_number)
        
        elif args.cmd == 'view_vehicles':
            listVehicles()

        elif args.cmd == 'view_drivers':
            listDrivers()

        elif args.cmd == 'view_plazas':
            listPlazas(args.name)

        elif args.cmd == 'plaza_report':
            plazaReport(args.plaza_number)

        else:
            print("No command specified. Use -h for help.")
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()
