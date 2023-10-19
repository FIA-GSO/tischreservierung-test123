from flask import Flask
from flask import request   # wird benötigt, um die HTTP-Parameter abzufragen
from flask import jsonify   # übersetzt python-dicts in json
from marshmallow import Schema, fields
import marshmallow
class reserve_table_schema(Schema):
    datetime = fields.Str(required=True)
    duration = fields.Int(required=True)

app = Flask(__name__)
app.config["DEBUG"] = True  # Zeigt Fehlerinformationen im Browser, statt nur einer generischen Error-Message

@app.route('/ReserveTable', methods=['POST'])
def reserve_table():
    schema = reserve_table_schema()
    
    try:
        data = schema.load(request.json)
    except marshmallow.ValidationError as e:
        return jsonify(e.messages), 400

    return jsonify({"message": "Table reserved successfully!"}), 201

@app.route('/FreeTables', methods=['GET'])
def free_tables():
    return "<h1>Freie Plaetze</h1>"

@app.route('/CancelReservation', methods=['PUT'])
def cancel_reservation():
    return "<h1>Reservierung stornieren</h1>"

@app.route('/AllReservations', methods=['GET'])
def all_reservations():
    return "<h1>Reservierung stornieren</h1>"




app.run()