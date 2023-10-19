import flask
from flask import request   # wird benötigt, um die HTTP-Parameter abzufragen
from flask import jsonify   # übersetzt python-dicts in json

app = flask.Flask(__name__)
app.config["DEBUG"] = True  # Zeigt Fehlerinformationen im Browser, statt nur einer generischen Error-Message

@app.route('/ReserveTable', methods=['POST'])
def reserve_table():
    return "<h1>Tischreservierung</h1>"

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