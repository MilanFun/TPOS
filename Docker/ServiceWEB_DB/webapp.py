from flask import Flask, jsonify, make_response
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CONFIG = {
    'user': 'root',
    'password': "root",
    'host': 'db',
    'port': "3306"
}
SELECT = "SELECT * FROM users"
CONNECTION = None


def get_connection():
    return mysql.connector.connect(**CONFIG)


@app.route('/')
def select():
    if CONNECTION is not None and CONNECTION.is_connected():
        cursor = CONNECTION.cursor()
        cursor.execute("USE userdb")
        cursor.execute(SELECT)
        data = dict(cursor.fetchall())
        cursor.close()
        return make_response(jsonify(data), 200)
    else:
        return make_response(jsonify(dict()), 404)


@app.route('/health')
def check_health():
    if CONNECTION is not None and CONNECTION.is_connected():
        return make_response(jsonify({"status": "OK"}), 200)
    else:
        return make_response(jsonify(dict()), 404)


if __name__ == "__main__":
    while True:
        try:
            CONNECTION = get_connection()

            if CONNECTION.is_connected():
                app.run(host="0.0.0.0", port=8000)
        except Error as e:
            continue
