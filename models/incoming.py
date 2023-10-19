from marshmallow import Schema, fields

class reserve_table(Schema):
    datetime = fields.Str(required=True)
    duration = fields.Int(required=True)