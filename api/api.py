import random
import sqlite3
import marshmallow

from datetime import datetime, timedelta

from flask import Flask, jsonify, request

#custom modules
from reserveRequest import ReserveSchema, ReserveRequest
from cancelRequest import CancelSchema, CancelRequest
from freeTablesRequest import FreeTablesSchema, FreeTablesRequest

app = Flask(__name__)

def init_app():
    app.config["DEBUG"] = True

@app.route('/')
def home():
    app.send_static_file("/index.html")

# ENDPOINTS
@app.route('/ReserveTable', methods=['POST'])
def reserve_table():
    result = None
    pin = random.randint(1111, 9999)
    try:
        schema = ReserveSchema()
        data = schema.load(request.json)
        con = sqlite3.connect("DB/buchungssystem.sqlite")

        print(data.zeitpunkt)
        print(data.tischnummer)


        cursor = con.cursor()
        prequery = f"SELECT * FROM reservierungen WHERE zeitpunkt = '{data.zeitpunkt}' AND tischnummer = '{data.tischnummer}'"
        response = cursor.execute(prequery)
        print(response)
        rows = response.fetchall()
        if(len(rows) > 0): return jsonify("Tisch schon vergeben"), 400



        print("NO RESERVIERUNG FOUND")

        cursor = con.cursor()
        query = "INSERT INTO reservierungen(zeitpunkt, tischnummer, pin, storniert) VALUES (?, ?, ?, ?)"
        
        parameters = (data.zeitpunkt, data.tischnummer, pin, "False")
        cursor.execute(query, parameters)
        
        cursor = con.cursor()
        select = "SELECT * FROM reservierungen WHERE zeitpunkt=? AND tischnummer=? AND pin=?"
        selectParams = (data.zeitpunkt, data.tischnummer, pin)
        cur_result = cursor.execute(select, selectParams)
        result = cur_result.fetchone()
        
        print(response)
        con.commit()
        con.close()

    except marshmallow.ValidationError as e:
        return jsonify(e.messages), 400

    print(result)
    return jsonify(result), 200


@app.route('/FreeTables', methods=['GET'])
def free_tables():
    try:
        freetables_loaded_data = FreeTablesSchema().load(request.data)

        freetables_request = FreeTablesRequest(**freetables_loaded_data)

        con = sqlite3.connect('./DB/buchungssystem.sqlite')

        cur = con.cursor()
        query = "SELECT * FROM reservierungen WHERE zeitpunkt LIKE '?'"

        all_bookings = cur.execute(query, freetables_request.timestamp).fetchall()
        con.close()
    except marshmallow.ValidationError as e:
        return jsonify(e.messages), 400
    return all_bookings


@app.route('/CancelReservation', methods=['PATCH'])
def cancel_reservation():
    try:
        cancel_loaded_data = CancelSchema().load(request.data)
        cancel_request = CancelRequest(**cancel_loaded_data)

        reservation_number = cancel_request.reservation_number
        print(f"resrvation_number: {reservation_number}")
        pin = cancel_request.pin
        print(f"PIN: {pin}")
        con = sqlite3.connect("DB/buchungssystem.sqlite")

        cursor = con.cursor()
        query = "SELECT * FROM reservierungen WHERE reservierungsnummer = ?"

        success = False
        for row in cursor.execute(query, cancel_request.reservation_number):
            print(row)
            if (str(row[3]) == pin):
                success = True

        con.close()
    except marshmallow.ValidationError as e:
        return jsonify(e.messages), 400
    if(success == False):
        return jsonify({"message": "Cancellation not successful! Reservation number or pin not correct."}), 400
    return jsonify({"message": "Cancellation successfully!"}), 201


@app.route('/AllReservations', methods=['GET'])
def all_reservations():
    try:
        con = sqlite3.connect("DB/buchungssystem.sqlite")
        
        cursor = con.cursor()
        query = "SELECT * FROM reservierungen WHERE zeitpunkt > ? AND zeitpunkt < ? AND storniert=FALSE"

        parameter = get_start_end_today()
        result = cursor.execute(query, parameter).fetchall()

        con.close()
    except marshmallow.ValidationError as e:
        return jsonify(e.messages), 400
    
    return result, 200


@app.route('/CheckIt', methods=['GET'])
def get_checkit_options():
    options = {
        "real": 
            {
                "text": lorem.text(),
                "img": {
                    "url": "https://img.zeit.de/politik/ausland/2023-06/usa-trump-anklage-geheimdokumente-tonbahnaufnahme-bild-2/square__960x960",
                    "alt": lorem.paragraph()
                }
            },
        "fake": 
            {
                "text": lorem.text(),
                "img": {
                    "url": "https://i.imgflip.com/7i9qy9.jpg",
                    "alt": lorem.paragraph()
                },
                "fakeHints": [    
                    {
                        "start": 1,
                        "length": 3,
                        "source": "https://www.google.com"
                    },
                ]
            },
    }

    return options



def get_start_end_today():
    today = datetime.utcnow().date()
    start = datetime(today.year, today.month, today.day)
    end = start + timedelta(1)
    
    return start, end

init_app()
app.run()
