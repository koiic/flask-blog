import datetime

from src.models.BaseModel import BaseModel
from . import db, bcrypt

class UserModel(BaseModel):
	"""Model For User"""

	# table name
	__tablename__ = 'users'

	name = db.Column(db.String, nullable=False)
	email = db.Column(db.String(128), nullable=False, unique=True)
	password = db.Column(db.String(128), nullable=False)
	blogposts = db.relationship('BlogPostModel', backref='users', lazy=True)

	# Class constructor
	def __init__(self, data):
		self.name = data.get('name')
		self.email = data.get('email')
		self.password = self.__generate_hash(data.get('password'))
		self.updated_at = data.get('updated_at')
		self.created_at = data.get('created_at')


	"""
	Method IMPLEMENTATION
	"""

	# save a model instance
	def save(self):
		db.session.add(self)
		db.session.commit()

	# delete a user object
	def delete(self):
		db.session.delete(self)
		db.session.commit()

	# update a single user
	def update(self, data):
		for key, item in data.items():
			if key == 'password':
				self.__generate_hash(item)
			setattr(self, key, item)
			self.updated_at = datetime.datetime.utcnow()

	# soft delete a user
	@staticmethod
	def deleteUser(user_id):
		user = UserModel.query.get(user_id)
		if user:
			user.deleted = True
		db.session.commit()

	# get all users
	@staticmethod
	def get_all_users():
		return UserModel.query.all()

	# get single user by id
	@staticmethod
	def get_single_user(_id):
		return UserModel.query.get(_id)

	# get single user by id
	@staticmethod
	def get_single_user_by_email(_email):
		return UserModel.query.filter_by(email=_email).first()

	# method to generate hash
	def __generate_hash(self, password):
		return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")


	# method to check hash
	def check_hash(self, password):
		return bcrypt.check_password_hash(self.password, password)


	def __repr__(self):
		return '<User {} >'.format(self)