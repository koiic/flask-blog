from src.models.BaseModel import BaseModel
from . import db
import datetime
from slugid import slugid

class BlogPostModel(BaseModel):
	"""BlogPost Model"""

	__tablename__ = 'blogs'

	title = db.Column(db.String(128), nullable=False)
	contents = db.Column(db.Text, nullable=False)
	slug = db.Column(db.String(128), nullable=False, unique=True)
	owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

	def __init__(self, data):
		self.title = data.get('title')
		self.contents = data.get('contents')
		self.slug = slugid.nice()
		self.owner_id = data.get('owner_id')


	def save(self):
		db.session.add(self)
		db.session.commit()


	def update(self, data):
		for key, value in data.items():
			setattr(self, key, value)
		self.updated_at(datetime.datetime.utcnow())
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()


	@staticmethod
	def get_all_blogpost():
		return BlogPostModel.query.all()

	def get_single_blogpost(id_):
		return BlogPostModel.query.get(id_)

	def get_single_blogpost_by_slug(slug):
		return BlogPostModel.query.get(slug)


	def __repr__(self):
		return '<id {}>'.format(self.id)