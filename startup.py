import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="MasonBeale"
)
mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS mydatabase")
mycursor.execute('SHOW DATABASES')
for x in mycursor:
  print(x) 