import sqlite3
import os
import random
from typing import Optional, Union

data = os.getcwd() + "/data/data.db"


def hash(user_input: str) -> str:
    hash_val = 1
    for index, letter in enumerate(user_input):
        hash_val *= ord(letter) ** len(user_input) * len(str(hash_val)) + (index + 1) * index ** 2
        if len(hex(int(hash_val))) > 32 or int(hash_val) > 1 * 10 * 48:
            hash_val //= 16 ** (len(hex(int(hash_val))) - 34)
        if len(hex(int(hash_val))) < 24:
            hash_val = hash_val ** 10
    return "".join([x for x in hex(int(hash_val)) if x != "0"])


class Sql:
    def __init__(self) -> None:
        pass

    def create(self) -> None:
        with open(f"{data}", "w"):
            pass
        with sqlite3.connect(f"{data}") as connection:
            cursor = connection.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS Users (UserID INTEGER PRIMARY KEY AUTOINCREMENT,Username TEXT NOT NULL);")
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS Passwords (PasswordID INTEGER PRIMARY KEY AUTOINCREMENT,Password TEXT NOT NULL);")
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS Link (UserID INTEGER,PasswordID INTEGER,FOREIGN KEY (UserID) REFERENCES Users(UserID),FOREIGN KEY (PasswordID) REFERENCES Passwords(PasswordID));")
            connection.commit()

    def validate(self, username: str, password: str) -> Optional[bool]:
        with sqlite3.connect(f"{data}") as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT Passwords.Password\
                                FROM Users JOIN Link ON Users.UserID == Link.UserID\
                                JOIN Passwords ON Link.PasswordID == Passwords.PasswordID\
                                WHERE Users.Username = (?)", (username,))
            password_found = cursor.fetchone()
            if password_found:
                return password_found[0] == hash(password)
            return None

    def createUser(self, username: str, password: str) -> Union[str, bool]:
        with sqlite3.connect(f"{data}") as connection:
            cursor = connection.cursor()

            if not username or not password:
                return "empty"

            cursor.execute("SELECT Username FROM Users")
            existing_users = [info[0] for info in cursor.fetchall()]
            if username in existing_users:
                return "username"

            cursor.execute("SELECT UserID FROM Users")
            existing_user_ids = [info[0] for info in cursor.fetchall()]
            cursor.execute("SELECT PasswordID FROM Passwords")
            existing_password_ids = [info[0] for info in cursor.fetchall()]

            user_id = random.randint(1, 999999)
            password_id = random.randint(1, 999999)
            while user_id in existing_user_ids and password_id in existing_password_ids:
                user_id = random.randint(1, 999999)
                password_id = random.randint(1, 999999)

            cursor.execute("INSERT INTO Users (UserID, Username) VALUES (?, ?)", (user_id, username,))
            cursor.execute("INSERT INTO Passwords (PasswordID, Password) VALUES (?, ?)", (password_id, hash(password),))
            cursor.execute("INSERT INTO Link (UserID, PasswordID) VALUES (?, ?)", (user_id, password_id))
            connection.commit()
            return True

    def reset(self) -> None:
        with sqlite3.connect(f"{data}") as connection:
            cursor = connection.cursor()
            # cursor.execute("DROP Username, Password, Link")
            connection.commit()
