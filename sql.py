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

#docker run --name mysql -e MYSQL_ROOT_PASSWORD=ProjectX2023 -d mysql:latest
#docker ps
#nvm ls
#node -v
#nvm install 19 (version)
#node -v
#docker run --name mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=ProjectX2023 -d mysql:latest
#yarn start:dev

#for db in mycursor:
    #print(db)

#-------------------------------------------------------------------------------
