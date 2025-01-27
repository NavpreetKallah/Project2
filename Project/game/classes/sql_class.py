import sqlite3, os

data = os.getcwd() + "/data/data.db"

class Sql:
    def __init__(self):
        pass


    def connect(self):
        with sqlite3.connect(f"{data}") as connection:
            cursor = connection.cursor()
            #cursor.execute("CREATE TABLE Username (UserID INT PRIMARY KEY NOT NULL,username VARCHAR(10));")
            #cursor.execute("CREATE TABLE Password (PasswordID INT PRIMARY KEY NOT NULL,password VARCHAR(10));")
            cursor.execute("CREATE TABLE Link (PasswordID INT NOT NULL, UserID INT NOT NULL, FOREIGN KEY (UserID) REFERENCES Username(UserID), FOREIGN KEY (PasswordID) REFERENCES Password(PasswordID));")
            connection.commit()

    def reset(self):
        with sqlite3.connect(f"{data}") as connection:
            cursor = connection.cursor()
            #cursor.execute("DROP Username, Password, Link")
            connection.commit()


