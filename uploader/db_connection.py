import mysql.connector
from mysql.connector import errorcode
import os

from dotenv import load_dotenv


load_dotenv()
config = {
  'user': os.getenv('DB_USERNAME'),
  'password': os.getenv('DB_PASSWORD'),
  'host': os.getenv('DB_HOST'),
  'database': os.getenv('DB'),
  'raise_on_warnings': True
}

try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = """SELECT * FROM bp_users_tbl"""
    cursor.execute(query)
    records = cursor.fetchall()
    for row in records:
        print("Id: ",row[0])
        print("Name: ",row[1])
    print("Connection Successful")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
