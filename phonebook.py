import psycopg2
from connect import connect
from config import load_config
import csv

sqlIN = 'INSERT INTO numbers(name, Phone_number) values(%s,%s) returning *'
sqlDEL = 'DELETE FROM numbers WHERE name = %s'
sqlUPDATEnum = 'UPDATE numbers SET Phone_number = %s WHERE name = %s'
sqlUPDATEname = 'UPDATE numbers SET name = %s WHERE Phone_number = %s'
sqlCHECK = 'SELECT * FROM numbers WHERE name = %s'
sqlCHECKN = 'SELECT * FROM numbers WHERE Phone_number = %s'
choice = 0


def readcsv(filename):
    data = []
    with open(filename, 'r') as f:
        datar = csv.reader(f, quotechar='"')
        for row in datar:
            data.append(row)
    print(data)
    return data


conn = connect(load_config())
cur = conn.cursor()

print('to Insert manually type 1 \n to insert from csv type 2')
print('to delete recort type 3')
print('to find the number type 4')
choice = int(input())
if choice == 1:
    name = input()
    number = input()
    if len(number) == 11:
        cur.execute(sqlCHECK, (name,))
        result = cur.fetchone()
        cur.execute(sqlCHECK, (number,))
        Nresult = cur.fetchone()
        if result:
            cur.execute(sqlUPDATEnum, (number, name))
            conn.commit()
        elif Nresult:
            cur.execute(sqlUPDATEname, (name, number))
            conn.commit()
        else:
            cur.execute(sqlIN, (name, number))
            conn.commit()
    else:
        print('Invalid number')
elif choice == 2:
    cur.executemany(sqlIN, readcsv('LegendsPhoneBook.csv'))
    conn.commit()
elif choice == 3:
    print('Type name')
    name = input()
    cur.execute(sqlCHECK, (name,))
    result = cur.fetchone()
    if result:
        cur.execute(sqlDEL, (name,))
        conn.commit()
        print('Deleted')
    else:
        print('no such record')
elif choice == 4:
    name = input()
    cur.execute(sqlCHECK, (name,))
    result = cur.fetchone()
    if result:
        print(result)
    else:
        print('No record found')
cur.close()
conn.close()
