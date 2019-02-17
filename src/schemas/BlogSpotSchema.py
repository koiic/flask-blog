from marshmallow import fields
from src.schemas.BaseSchema import BaseSchema


class BlogSpotSchema(BaseSchema):
	"""BlogSpot Schema"""

	title = fields.Str(required=True)
	contents = fields.Str(required=True)
	slug = fields.Str(dump_only=True)
	owner_id = fields.Int(required=True)