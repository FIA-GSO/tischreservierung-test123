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

class cancel_reservation_schema(Schema):
    reservation_number = fields.Int(required=True)
    pin = fields.Str(required=True)

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
    return "<h1>Freie Plaetze</h1>"










@app.route('/CancelReservation', methods=['PATCH'])
def cancel_reservation():
    schema = cancel_reservation_schema()
    
    try:
        data = schema.load(request.json)
        
        con = sqlite3.connect("DB/buchungssystem.sqlite")

        cursor = con.cursor()
        query = "SELECT * FROM reservierungen"
        for row in cursor.execute(query):
            print(row)

      

        cursor.execute(query)
        result = cursor.fetchall()

        print(result)

        con.close()





    except marshmallow.ValidationError as e:
        return jsonify(e.messages), 400

    return jsonify({"message": "Cancellation successfully!"}), 201







@app.route('/AllReservations', methods=['GET'])
def all_reservations():
    return "<h1>Reservierung stornieren</h1>"




app.run()