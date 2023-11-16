from marshmallow import Schema, fields, post_load

class ReserveSchema(Schema):
    tischnummer = fields.Int(required=True)
    zeitpunkt = fields.Str(required=True)

    @post_load
    def create_reserve_request(self, data, **kwargs):
        return ReserveRequest(**data)