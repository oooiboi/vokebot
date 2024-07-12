import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    password="Rasul@2003",
    user="root",
    database="user"
)

mycursor = db.cursor()

mycursor.execute("CREATE TABLE IF NOT EXISTS Users_final (name VARCHAR(255) NOT NULL, countries VARCHAR(255) NOT NULL, school VARCHAR(255) NOT NULL, phone VARCHAR(255) NOT NULL, grade INT NOT NULL)")





