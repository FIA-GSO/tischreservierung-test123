from marshmallow import Schema, fields, post_load

class ReserveRequest:
    def __init__(self, tischnummer, zeitpunkt):
        self.tischnummer = tischnummer
        self.zeitpunkt = zeitpunkt

    def __repr__(self):
        return f"{self.tischnummer}, {self.zeitpunkt}"

class ReserveSchema(Schema):
    tischnummer = fields.Int(required=True)
    zeitpunkt = fields.Str(required=True)

    @post_load
    def create_reserve_request(self, data, **kwargs):
        return ReserveRequest(**data)