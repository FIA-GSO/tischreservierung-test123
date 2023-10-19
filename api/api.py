from flask import Flask
from flask import request   # wird benötigt, um die HTTP-Parameter abzufragen
from flask import jsonify   # übersetzt python-dicts in json
from marshmallow import Schema, fields
import marshmallow
import sqlite3




# SCHEMAS
class reserve_table_schema(Schema):
    tablenumber = fields.Int(required=True)
    number_of_guests = fields.Int(required=True)
    datetime = fields.Str(required=True)
    duration = fields.Int(required=True)

class cancel_reservation_schema(Schema):
    reservation_number = fields.Int(required=True)
    pin = fields.Str(required=True)

app = Flask(__name__)
app.config["DEBUG"] = True  # Zeigt Fehlerinformationen im Browser, statt nur einer generischen Error-Message



# ENDPOINTS

@app.route('/ReserveTable', methods=['POST'])
def reserve_table():
    schema = reserve_table_schema()
    
    try:
        data = schema.load(request.json)
        con = sqlite3.connect("../DB/buchungssystem.sqlite")

        cursor = con.cursor()

        query = "SELECT * FROM reservierungen"

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
        con = sqlite3.connect("../DB/buchungssystem.sqlite")

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