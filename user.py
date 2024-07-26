import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    password="Rasul@2003",
    user="root",
    database="user"
)




mycursor = db.cursor()
        
db.commit()




