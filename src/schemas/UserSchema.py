from marshmallow import fields

from src.schemas import BlogSpotSchema
from src.schemas.BaseSchema import BaseSchema


class UserSchema(BaseSchema):
	""" User Schema"""

	name = fields.Str(required=True)
	email = fields.Str(required=True)
	password = fields.Str(required=True)
	blogspot = fields.Nested(BlogSpotSchema, many=True)