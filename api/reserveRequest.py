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
    
    def __init__(self, tischnummer, zeitpunkt):
        self.tischnummer = tischnummer
        self.zeitpunkt = self.format_timestamp(zeitpunkt)
    
    def __repr__(self):
        return f"{self.tischnummer},{self.zeitpunkt}"

class ReserveSchema(Schema):
    tischnummer = fields.Int(required=True)
    zeitpunkt = fields.Str(required=True)

    @post_load
    def create_reserve_request(self, data, **kwargs):
        return ReserveRequest(**data)