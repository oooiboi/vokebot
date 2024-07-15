import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    password="Rasul@2003",
    user="root",
    database="user"
)


# SQL command to create the table
create_table_query = """
CREATE TABLE UserActivity (
    activity_id INT AUTO_INCREMENT PRIMARY KEY,
    chat_id INT,
    activity_date DATE,
    activity_description TEXT,
    activity_done BOOLEAN,
    CONSTRAINT fk_chat_id FOREIGN KEY (chat_id) REFERENCES Users_final(chat_id)
);
"""


mycursor = db.cursor()
        
        # Executing the create table command
mycursor.execute(create_table_query)
        
        # Committing the changes to the database




     
        # Commit the changes to the database
db.commit()




