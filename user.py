import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    password="Rasul@2003",
    user="root",
    database="user"
)

mycursor = db.cursor()

mycursor.execute("CREATE TABLE IF NOT EXISTS users (name VARCHAR(255) NOT NULL, countries VARCHAR(255) NOT NULL, school VARCHAR(255) NOT NULL, phone INT NOT NULL, grade INT NOT NULL)")

mycursor.execute("INSERT INTO users (name, countries, school, phone, grade) VALUES (%s,%s,%s,%s,%s)",("Drake","Canada","NIS",777, 19))
db.commit()
#mycursor.execute("DESCRIBE users")
mycursor.execute("SELECT * FROM users")
for x in mycursor:
    print(x)


