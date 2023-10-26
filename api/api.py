import datetime
from flask import Flask
from flask import request   # wird benötigt, um die HTTP-Parameter abzufragen
from flask import jsonify   # übersetzt python-dicts in json
from flask import render_template
from marshmallow import Schema, fields
from marshmallow import Schema, fields, post_load
import marshmallow
import sqlite3
import random


class ReserveRequest:
    def __init__(self, tablenumber, number_of_guests, datetime, duration):
            self.tablenumber = tablenumber
            self.number_of_guests = number_of_guests
            self.datetime = datetime
            self.duration = duration
    
    def __repr__(self):
        return f"{self.tablenumber}, {self.number_of_guests}, {self.datetime}, {self.duration}"

# SCHEMAS
class ReserveSchema(Schema):
    tablenumber = fields.Int(required=True)
    number_of_guests = fields.Int(required=True)
    datetime = fields.Str(required=True)
    duration = fields.Int(required=True)


class comment_schema(Schema):
    username = fields.Str(required=True)
    comment = fields.Str(required=True)


    @post_load
    def create_reserve_request(self, data, **kwargs):
            return ReserveRequest(**data)

class cancel_reservation_schema(Schema):
    reservation_number = fields.Int(required=True)
    pin = fields.Str(required=True)


class free_table_schema(Schema):
    timestamp = fields.Str(required=True)

app = Flask(__name__)
# Zeigt Fehlerinformationen im Browser, statt nur einer generischen Error-Message
app.config["DEBUG"] = True


# ENDPOINTS

@app.route('/')
def home():
    con = sqlite3.connect("DB/buchungssystem.sqlite")

    cursor = con.cursor()

    query = "SELECT * FROM comments;"

    res = cursor.execute(query)

    rows = res.fetchall()
    res = [
        {
            'name': row[0],
            'text': row[1],
            'time': row[2]
        } for row in rows
    ]
    print(res)

    con.close()

    return render_template('index.html', comments=res)


@app.route('/PostComment', methods=['POST'])
def PostComment():
    schema = comment_schema()

    try:
        data = schema.load(request.json)
        username = data['username']
        comment = data['comment']
        con = sqlite3.connect("DB/buchungssystem.sqlite")

        cursor = con.cursor()

        dt = str(datetime.datetime.now())
        query = f"INSERT INTO comments VALUES('{username}','{comment}','{dt}');"
        print(query)

        res = cursor.execute(query)

        result = res.fetchall()
        con.commit()
        con.close()
        home()

    except marshmallow.ValidationError as e:
        return jsonify(e.messages), 400

    return result, 201


@app.route('/ReserveTable', methods=['POST'])
def reserve_table():
    schema = reserve_table_schema()

    pin = random.randint(1111, 9999)
    try:
        data = ReserveSchema().load(request.json)
        con = sqlite3.connect("DB/buchungssystem.sqlite")

        cursor = con.cursor()

        query = f"""INSERT INTO reservierungen(zeitpunkt, tischnummer, pin, storniert)
            VALUES ({data.datetime}, {data.tablenumber}, {pin}, 0)
        """
        print(query)
        res = cursor.execute(query)

        result = res.fetchall()
        con.commit()
        con.close()

    except marshmallow.ValidationError as e:
        return jsonify(e.messages), 400

    return result, 201


@app.route('/FreeTables', methods=['GET'])
def free_tables():
    schema = free_table_schema()
    try:
        data = schema.load(request.json)
        timestamp = data['timestamp']
        print(timestamp)
        date, time = timestamp.split(" ")
        hh, mm, _ = time.split(":")
        print(hh, mm)
        if int(mm) > 30:
            hh = int(hh) + 1
            mm = "00"
        elif 0 < int(mm) <= 30:
            mm = "30"
        timestamp = f"{date} {hh%24:02d}:{mm}:00"
        conn = sqlite3.connect('./DB/buchungssystem.sqlite')
        cur = conn.cursor()
        query = f"""SELECT * FROM reservierungen 
        WHERE zeitpunkt LIKE '{timestamp}'"""
        all_bookings = cur.execute(query).fetchall()
    except marshmallow.ValidationError as e:
        return jsonify(e.messages), 400
    return all_bookings



@app.route('/CancelReservation', methods=['PATCH'])
def cancel_reservation():
    schema = cancel_reservation_schema()

    try:
        data = schema.load(request.json)
        reservation_number = data['reservation_number']
        print(f"resrvation_number: {reservation_number}")
        pin = data['pin']
        print(f"PIN: {pin}")
        con = sqlite3.connect("DB/buchungssystem.sqlite")

        cursor = con.cursor()
        query = f"SELECT * FROM reservierungen WHERE reservierungsnummer = {reservation_number}"

        success = False
        for row in cursor.execute(query):
            print(row)
            if(str(row[3]) == pin):
                success = True

        con.close()

    except marshmallow.ValidationError as e:
        return jsonify(e.messages), 400
    if(success == False):
        return jsonify({"message": "Cancellation not successful! Reservation number or pin not correct."}), 400
    return jsonify({"message": "Cancellation successfully!"}), 201


@app.route('/AllReservations', methods=['GET'])
def all_reservations():
    return "<h1>Reservierung stornieren</h1>"


app.run()
