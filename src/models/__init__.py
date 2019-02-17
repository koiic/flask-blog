from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


# initialize our db
db = SQLAlchemy()

bcrypt = Bcrypt()


from . import BaseModel, UserModel, BlogPostModel
