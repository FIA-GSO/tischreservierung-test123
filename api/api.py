from flask import Flask
from flask import request   # wird benötigt, um die HTTP-Parameter abzufragen
from flask import jsonify   # übersetzt python-dicts in json
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

    @post_load
    def create_reserve_request(self, data, **kwargs):
            return ReserveRequest(**data)
    
class CancelRequest:
    def __init__(self, reservation_number, pin):
            self.reservation_number = reservation_number
            self.pin = pin
    
    def __repr__(self):
        return f"{self.reservation_number}, {self.pin}"

class CancelSchema(Schema):
    reservation_number = fields.Int(required=True)
    pin = fields.Str(required=True)

    @post_load
    def create_reserve_request(self, data, **kwargs):
            return CancelRequest(**data)

class FreeTables:
    def format_timestamp(self, timestamp) -> str:
        date, time = timestamp.split(" ")
        hh, mm, _ = time.split(":")
        if int(mm) > 30:
            hh = int(hh) + 1
            mm = "00"
        elif int(mm) != 0:
            mm = "30"

        return f"{date} {hh%24:02d}:{mm}:00"
    
    def __init__(self, timestamp):
        self.timestamp = self.format_timestamp(timestamp)
    
    
    def __repr__(self) -> str:
         return f'{self.timestamp}'
    
class FreeTablesSchema(Schema):
     timestamp = fields.Str(required=True)

     @post_load
     def create_freetables_schema(self, data, **kwargs):
        return FreeTables(**data)


app = Flask(__name__)
app.config["DEBUG"] = True  # Zeigt Fehlerinformationen im Browser, statt nur einer generischen Error-Message

# ENDPOINTS

@app.route('/ReserveTable', methods=['POST'])
def reserve_table():
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
    try:
        data = FreeTablesSchema().load(request.args.to_dict())
        print(data)
        timestamp = data.timestamp
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
    
    try:
        data = CancelSchema().load(request.json)
        reservation_number = data.reservaiton_number
        print(f"resrvation_number: {reservation_number}")
        pin = data['pin']
        print(f"PIN: {pin}")
        con = sqlite3.connect("DB/buchungssystem.sqlite")

        cursor = con.cursor()
        query = f"SELECT * FROM reservierungen WHERE reservierungsnummer = {reservation_number}"

        success = False
        for row in cursor.execute(query):
            print(row)
            if(str(row[3]) == pin) :
                success = True

        con.close()





    except marshmallow.ValidationError as e:
        return jsonify(e.messages), 400
    if(success == False): return jsonify({"message": "Cancellation not successful! Reservation number or pin not correct."}), 400
    return jsonify({"message": "Cancellation successfully!"}), 201




@app.route('/AllReservations', methods=['GET'])
def all_reservations():
    return "<h1>Reservierung stornieren</h1>"




app.run()
