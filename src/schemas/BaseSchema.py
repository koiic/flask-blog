from marshmallow import fields, Schema

class BaseSchema(Schema):
	"""BASE SCHEMA"""

	id = fields.Int(dump_only=True)
	deleted = fields.Boolean(dump_only=True)
	created_at = fields.DateTime(dump_only=True)
	updated_at = fields.DateTime(dump_only=True)

	def load_object_into_schema(self, data, partial=False):
		"""Helper function to load python objects into schema"""
		data, error = self.load(data, partial=partial)

		if error:
			raise AttributeError(dict(errors=error, message='An error occurred'), 400)

		return data