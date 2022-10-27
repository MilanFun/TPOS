import pandas as pd
import mysql.connector
from mysql.connector import Error
import os

CONFIG = {
    'user': 'root',
    'password': "root",
    'host': 'db',
    'port': "3306"
}
INSERT = "INSERT INTO users (name, age) VALUES (%s, %s)"
SELECT = "SELECT * FROM users"
DATAPATH = os.path.abspath("./") + os.sep + "data.csv"
DATA = pd.read_csv(DATAPATH)
SIZE = DATA.shape[0]


def get_connection():
    return mysql.connector.connect(**CONFIG)


def select(conn):
    cursor = conn.cursor()
    cursor.execute(SELECT)
    result = cursor.fetchall()
    for elem in result:
        print(elem)


def close(conn, curs):
    conn.close()
    curs.close()


def insert(conn):
    cursor = conn.cursor()
    for i in range(SIZE):
        cursor.execute(INSERT, (DATA['name'][i], str(DATA['age'][i])))
    conn.commit()


if __name__ == "__main__":
    while True:
        try:
            connection = get_connection()

            if connection.is_connected():
                cursor = connection.cursor()
                cursor.execute("USE userdb")

                insert(connection)
                select(connection)
                close(connection, cursor)
                break

        except Error as e:
            continue
