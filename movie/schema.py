from marshmallow import Schema, fields, validate, validates_schema, ValidationError


class MovieSchema(Schema):
    name = fields.Str(required=True)
    popularity = fields.Str(required=True)
    imdb_score = fields.Str(required=True)
    director = fields.Str(required=True)
    genre = fields.List(fields.Str, validate=validate.Length(min=1), required=True)


class MovieDeleteSchema(Schema):
    name = fields.Str(required=True)


class MovieUpdateSchema(Schema):
    name = fields.Str(required=True)
    new_name = fields.Str()
    popularity = fields.Str()
    imdb_score = fields.Str()
    director = fields.Str()
    genre = fields.List(fields.Str, validate=validate.Length(min=1))


class MovieSearchSchema(Schema):
    name = fields.Str()
    director = fields.Str()
    genre = fields.List(fields.Str, validate=validate.Length(min=1))


class MovieDetailsSchema(Schema):
    name = fields.Str(required=True)
