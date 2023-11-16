from marshmallow import Schema, fields, post_load

class ReserveRequest:
    def format_timestamp(self, timestamp) -> str:
        date, time = timestamp.split(" ")
        hh, mm, _ = time.split(":")
        if int(mm) > 30:
            hh = int(hh) + 1
            mm = "00"
        elif int(mm) != 0:
            mm = "30"

        return f"{date} {hh % 24:02d}:{mm}:00"
    
    def __init__(self, tablenumber, number_of_guests, datetime, duration):
        self.tablenumber = tablenumber
        self.number_of_guests = number_of_guests
        self.datetime = self.format_timestamp(datetime)
        self.duration = duration
    
    def __repr__(self):
        return f"{self.tablenumber}, {self.number_of_guests}, {self.datetime}, {self.duration}"

class ReserveSchema(Schema):
    tablenumber = fields.Int(required=True)
    number_of_guests = fields.Int(required=True)
    datetime = fields.Str(required=True)
    duration = fields.Float(required=True)

    @post_load
    def create_reserve_request(self, data, **kwargs):
        return ReserveRequest(**data)