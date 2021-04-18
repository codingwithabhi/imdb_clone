from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class NewUser(Schema):
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Int(required=True)
    user_type = fields.Str(required=True, validate=validate.OneOf(["Admin", "User"]))



