from marshmallow import Schema, fields, post_load

class FreeTablesRequest:
    def format_timestamp(self, timestamp) -> str:
        date, time = timestamp.split(" ")
        hh, mm, _ = time.split(":")
        if int(mm) > 30:
            hh = int(hh) + 1
            mm = "00"
        elif int(mm) != 0:
            mm = "30"

        return f"{date} {hh % 24:02d}:{mm}:00"

    def __init__(self, timestamp):
        self.timestamp = self.format_timestamp(timestamp)

    def __repr__(self) -> str:
        return f'{self.timestamp}'


class FreeTablesSchema(Schema):
    timestamp = fields.Str(required=True)
    tableNr = fields.Int(required=False)

    @post_load
    def create_freetables_schema(self, data, **kwargs):
        return FreeTablesRequest(**data)