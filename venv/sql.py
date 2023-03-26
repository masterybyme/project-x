import mysql.connector

#CREATE MYSQL
#------------------------------------------------------------------------------
mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='ProjectX2023',
    port = '3306',
    database = 'projectxdb')
mycursor = mydb.cursor()

#delete_table = 'DROP TABLE User'
#create_db = 'CREATE DATABASE projectxdb'
#create_table = 'CREATE TABLE xyz'
delete_table_entries = 'TRUNCATE TABLE Opening_Hours'

mycursor.execute(delete_table_entries)


#for db in mycursor:
    #print(db)

#-------------------------------------------------------------------------------
