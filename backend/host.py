from flask import Flask, jsonify
import mysql.connector
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    con = mysql.connector.connect(
        user="root",
        password="12345678",
        host="localhost",
        database="restaurant",
        port=3305
    )
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT rest_name, rest_image, rest_href FROM rest")
    restaurants = cursor.fetchall()
    cursor.close()
    con.close()
    return jsonify(restaurants)

if __name__ == '__main__':
    app.run(port=5000)
