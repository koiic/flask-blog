from flask import Flask
from .config import config_obj
from .models import bcrypt, db

# from .models import BaseModel
# from .models import UserModel
# from .models import BlogPostModel

# import user_api blueprint
from .views.UserView import user_api as user_blueprint

def create_app(environment):
	""" Create an instance of flask
	:arg
		environment(String): environment to run on flask app
	"""
	# initialize app
	app = Flask(__name__)

	# configure the environment
	app.config.from_object(config_obj[environment])

	#initialize bcrypt
	bcrypt.init_app(app)

	db.init_app(app)

	# baseUrl = '/ap1/v1/users'
	app.register_blueprint(user_blueprint, url_prefix='/api/v1/users')

	@app.route('/', methods=['GET'])
	def index():
		"""
		example endpoint
		"""
		return 'Congratulations! Your first endpoint is workin'

	return app

