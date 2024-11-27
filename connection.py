import mysql.connector

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = 'earntodie1',
    port = 3306,
    database = 'python_db'
)

my_cursor = mydb.cursor()