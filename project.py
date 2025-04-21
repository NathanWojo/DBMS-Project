import mysql.connector
from tabulate import tabulate
from datetime import datetime
import sys 
import traceback
import logging
import argparse

mysql_username = 'nawojtow'
mysql_password = 'Iox4quai'

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
def addDriver(driverID, name, age, licensePlate, make, model, axles):
    try:
        query1 = """
        insert ignore into Driver (driverID, name, age)
        values (%s, %s, %s)
        """
        cursor.execute(query1, (driverID, name, age))
        conn.commit()
        print(f"\nDriver {name.strip()} added or already exists")

        query2 = """
        select 1 from Vehicle 
        where licensePlate = %s
        """
        cursor.execute(query2, (licensePlate,))
        vehicle = cursor.fetchone()

        if not vehicle:
            query3 = """
            insert into Vehicle (licensePlate, make, model, axles)
            values (%s, %s, %s, %s)
            """
            cursor.execute(query3, (licensePlate, make, model, axles))
            conn.commit()
            print(f"\nNew vehicle with plate {licensePlate} created")

        query4 = """
        insert ignore into VehicleOwner (licensePlate, driverID)
        values (%s, %s)
        """
        cursor.execute(query4, (licensePlate, driverID))
        conn.commit()

    except mysql.connector.Error as err:
        print(f"\nWomp womp: failed to add")

#add pass, make sure 2 axles maps to 3.99 and 3 axles maps to 5.99
def addPass(passID, licensePlate, driverID, plazaNumber, cost):
    try:
        date = datetime.now().strftime("%Y-%m-%d")
        time = datetime.now().strftime("%H:%M:%S")

        query1 = """
        select axles from Vehicle
        where licensePlate = %s
        """
        cursor.execute(query1, (licensePlate,))
        result = cursor.fetchone()
        if not result:
            print(f"\nWomp womp: vehicle with license plate {licensePlate} does not exist")
            return
        axleCount = result[0]

        query2 = """
        select 1 from VehicleOwner
        where licensePlate = %s and driverID = %s
        """
        cursor.execute(query2, (licensePlate, driverID))
        if cursor.fetchone() is None:
            print(f"\nWomp womp: driver {driverID} is not associated with given vehicle")
            return
        
        if axleCount == 2 and cost != 3.99:
            print("\nWomp womp: cost must be 3.99 for 2-axle vehicles")
            return
        elif axleCount == 3 and cost != 5.99:
            print("\nWomp womp: cost must be 5.99 for 3-axle vehicles")
            return

        query3 = """
        select 1 from Plaza
        where plazaNumber = %s
        """
        cursor.execute(query3, (plazaNumber,))
        if cursor.fetchone() is None:
            print(f"\nWomp womp: plaza {plazaNumber} does not exist")
            return

        query4 = """
        insert into Pass (passID, licensePlate, driverID, plazaNumber, passDate, passTime, cost)
        values (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query4, (passID, licensePlate, driverID, plazaNumber, date, time, cost))
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
        SELECT 
            V.licensePlate, V.make, V.model, V.axles, 
            GROUP_CONCAT(D.name SEPARATOR ', ') AS driverNames,
            P.passDate, P.passTime, P.cost, P.plazaNumber
        FROM Vehicle V
        LEFT JOIN VehicleOwner VO ON V.licensePlate = VO.licensePlate
        LEFT JOIN Driver D ON VO.driverID = D.driverID
        LEFT JOIN (
            SELECT p1.*
            FROM Pass p1
            INNER JOIN (
                SELECT licensePlate, MAX(CONCAT(passDate, ' ', passTime)) AS latestPass
                FROM Pass
                GROUP BY licensePlate
            ) latest ON p1.licensePlate = latest.licensePlate
            AND CONCAT(p1.passDate, ' ', p1.passTime) = latest.latestPass
        ) P ON V.licensePlate = P.licensePlate
        GROUP BY V.licensePlate, V.make, V.model, V.axles, P.passDate, P.passTime, P.cost, P.plazaNumber
        ORDER BY V.licensePlate ASC
        """
        cursor.execute(query)
        result = cursor.fetchall()
        print(printFormat(result))

    except mysql.connector.Error as err:
        print(f"\nWomp womp: failed to list")

#list all drivers that have 2 axled vehicles
def listDrivers(axles):
    try:
        query = """
        select distinct D.driverID, D.name, D.age
        from Driver D
        join VehicleOwner VO on D.driverID = VO.driverID
        join Vehicle V on VO.licensePlate = V.licensePlate
        where V.axles = %s
        order by D.name asc
        """
        cursor.execute(query, (axles,))
        result = cursor.fetchall()
        if not result:
            print(f"\nWomp womp: no drivers with {axles}-axled vehicles")
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
        
def bonus():
    try:
        query1 = """
        drop table if exists DriverStats
        """
        cursor.execute(query1)
        conn.commit()
        
        query2 = """
        create table DriverStats (
        driverID char(9) primary key,
        name char(25),
        numVehicles INT,
        numPasses INT
        )
        """
        cursor.execute(query2)
        conn.commit()

        query3 = """
        insert into DriverStats (driverID, name, numVehicles, numPasses)
        select
        D.driverID,
        D.name,
        count(distinct VO.licensePlate) as numVehicles,
        count(distinct P.passID) as numPasses
        from Driver D
        left join VehicleOwner VO on D.driverID = VO.driverID
        left join Pass P on D.driverID = P.driverID
        group by D.driverID, D.name
        """
        cursor.execute(query3)
        conn.commit()

        query4 = """
        select * from DriverStats
        order by numPasses desc
        """
        cursor.execute(query4)
        result = cursor.fetchall()
        print(printFormat(result))

    except mysql.connector.Error as err:
        print(f"\nWomp womp: failed to create table")

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='cmd')

    # add driver/vehicle sub command
    p = sub.add_parser('add_driver')
    p.add_argument('driver_id')
    p.add_argument('name')
    p.add_argument('age', type=int)
    p.add_argument('license_plate')
    p.add_argument('make')
    p.add_argument('model')
    p.add_argument('axles', type=int)

    # add pass sub command
    p2 = sub.add_parser('add_pass')
    p2.add_argument('pass_id')
    p2.add_argument('license_plate')
    p2.add_argument('driver_id')
    p2.add_argument('plaza_number')
    p2.add_argument('cost', type=float)

    p3 = sub.add_parser('view_passes')
    p3.add_argument('plaza_number')

    p4 = sub.add_parser('view_vehicles')

    p5 = sub.add_parser('view_drivers')
    p5.add_argument('axles', type=int, choices=[2, 3])

    p6 = sub.add_parser('view_plazas')
    p6.add_argument('name')

    p7 = sub.add_parser('plaza_report')
    p7.add_argument('plaza_number')
    
    p8 = sub.add_parser('bonus')

    args = parser.parse_args()

    open_database('localhost', mysql_username, mysql_password, mysql_username)

    try:
        # commands
        if args.cmd == 'add_driver':
            addDriver(args.driver_id, args.name, args.age, args.license_plate, args.make, args.model, args.axles)
 
        elif args.cmd == 'add_pass':
            addPass(args.pass_id, args.license_plate, args.driver_id, args.plaza_number, args.cost)
        
        elif args.cmd == 'view_passes':
            listPasses(args.plaza_number)
        
        elif args.cmd == 'view_vehicles':
            listVehicles()

        elif args.cmd == 'view_drivers':
            listDrivers(args.axles)

        elif args.cmd == 'view_plazas':
            listPlazas(args.name)

        elif args.cmd == 'plaza_report':
            plazaReport(args.plaza_number)
            
        elif args.cmd == 'bonus':
            bonus()

        else:
            print("No command specified. Use -h for help.")
    finally:
        close_db()

if __name__ == "__main__":
    main()
