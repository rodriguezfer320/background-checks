from marshmallow import Schema, fields

class BackgroundArgsSchema(Schema):
    type = fields.String(required=False, missing=None)