from marshmallow import Schema, fields, post_load



class FreeTablesSchema(Schema):
    timestamp = fields.Str(required=True)    
    tableNr = fields.Int(required=False)