from . import db
import datetime


class BaseModel(db.Model):
	'''
	Base Model consist of common attributes
	'''
	__abstract__ = True

	id = db.Column(db.Integer, primary_key=True)
	deleted = db.Column(db.Boolean, default=False)
	created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
	updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)