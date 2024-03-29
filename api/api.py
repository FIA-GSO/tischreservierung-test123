import random
import sqlite3
from marshmallow import ValidationError
from datetime import datetime, timedelta
from flask import Flask, jsonify, render_template, request
from cancelRequest import CancelSchema, CancelRequest
from reserveRequest import ReserveSchema


def make_key():
    """A function which is called to derive the key for a computed value.
       The key in this case is the concat value of all the json request
       parameters. Other strategy could to use any hashing function.
    :returns: unique string for which the value should be cached.
    """
    user_data = request.get_json()
    return ",".join([f"{key}={value}" for key, value in user_data.items()])


def init_app(app):

    @app.route('/api/docs')
    def get_docs():
        print('sending docs')
        return render_template('swaggerui.html')

    @app.route("/")
    def home():
        app.send_static_file("index.html")

    # ENDPOINTS
    @app.route("/Reservation", methods=["POST"])
    def reserve_table():
        response_json = None
        data = None
        # now = datetime.now()
        pin = random.randint(1111, 9999)

        try:
            data = ReserveSchema().load(request.json)
        except ValidationError as e:
            return jsonify(e.messages), 400

        try:
            con = sqlite3.connect("DB/buchungssystem.sqlite")
            con.row_factory = dict_factory

            if not is_valid_reservation_datetime(con, data.zeitpunkt):
                return jsonify("Kann nicht in die vergangenheit buchen"), 400

            if not has_free_table(con, data.zeitpunkt, data.tischnummer):
                return jsonify("Kein Tisch verfügbar"), 400

            cursor = con.cursor()
            query = "INSERT INTO reservierungen(zeitpunkt, tischnummer, pin, storniert) VALUES (?, ?, ?, ?)"
            parameters = (data.zeitpunkt, data.tischnummer, pin, "False")
            cursor.execute(query, parameters)

            response_json = get_reservation_response(
                con, data.zeitpunkt, data.tischnummer, pin
            )

            con.commit()
            con.close()
        except sqlite3.Error as e:
            return jsonify(e), 400

        print(response_json)
        return response_json, 200

    @app.route("/FreeTables", methods=["GET"])
    def free_tables():
        try:
            con = sqlite3.connect("./DB/buchungssystem.sqlite")
            con.row_factory = dict_factory
            timestamp = request.json["timestamp"]
            dt = format_timestamp(timestamp)
            print(dt)
            cur = con.cursor()
            query = "SELECT * FROM reservierungen WHERE zeitpunkt = ?"

            all_bookings = cur.execute(query, (dt,)).fetchall()
            con.close()
        except ValidationError as e:
            return jsonify(e.messages), 400
        return jsonify(bookings=all_bookings), 200

    @app.route("/Reservation", methods=["DELETE"])
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
                if str(row[3]) == pin:
                    success = True

            con.close()
        except ValidationError as e:
            return jsonify(e.messages), 400
        if not success:
            return (
                jsonify(
                    {
                        "message": "Cancellation not successful! Reservation number or pin not correct."
                    }
                ),
                400,
            )
        return jsonify({"message": "Cancellation successfully!"}), 201

    @app.route("/AllReservations", methods=["GET"])
    def all_reservations():
        try:
            con = sqlite3.connect("DB/buchungssystem.sqlite")

            cursor = con.cursor()
            query = "SELECT * FROM reservierungen WHERE zeitpunkt > ? AND zeitpunkt < ? AND storniert=FALSE"

            parameter = get_start_end_today()
            result = cursor.execute(query, parameter).fetchall()

            con.close()
        except ValidationError as e:
            return jsonify(e.messages), 400

        return result, 200


def has_free_table(connection, zeitpunkt, tischnummer):
    cursor = connection.cursor()
    parameters = (zeitpunkt, tischnummer)
    query = "SELECT * FROM reservierungen WHERE zeitpunkt = ? AND tischnummer = ?"
    response = cursor.execute(query, parameters)
    print(response)
    rows = response.fetchall()
    if len(rows) > 0:
        return False

    return True


def is_valid_reservation_datetime(connection, date_time):
    now = datetime.now()
    try:
        time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return False
    if time.minute != 0 and time.minute != 30:
        return False
    if time < now:
        return False
    return True


def get_reservation_response(connection, zeitpunkt, tischnummer, pin):
    cursor = connection.cursor()
    select = (
        "SELECT * FROM reservierungen WHERE zeitpunkt=? AND tischnummer=? AND pin=?"
    )
    selectParams = (zeitpunkt, tischnummer, pin)
    cur_result = cursor.execute(select, selectParams)
    result = cur_result.fetchone()

    return jsonify(result)


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_start_end_today():
    today = datetime.utcnow().date()
    start = datetime(today.year, today.month, today.day)
    end = start + timedelta(1)

    return start, end


def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True

    init_app(app)

    return app


def format_timestamp(timestamp) -> datetime:
    try:
        time = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

        if time.minute > 30:
            time = time.replace(hour=time.hour + 1, minute=0)
        elif time.minute != 0:
            time = time.replace(minute=30)

    except ValueError:
        raise ("TIMESTAMP!!!!!!!!!")

    return time


if __name__ == "__main__":
    app = create_app()
<< << << < HEAD
app.run(use_reloader=True, debug=False)
== == == =
app.run()
>>>>>> > 8f3e494(sql execute placeholder)
