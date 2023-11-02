from marshmallow import Schema, fields, post_load

class CancelRequest:
    def __init__(self, reservation_number, pin):
        self.reservation_number = reservation_number
        self.pin = pin

    def __repr__(self):
        return f"{self.reservation_number}, {self.pin}"


class CancelSchema(Schema):
    reservation_number = fields.Int(required=True)
    pin = fields.Str(required=True)

    @post_load
    def create_reserve_request(self, data, **kwargs):
        return CancelRequest(**data)