import os

from src.app import create_app
from dotenv import load_dotenv
from pathlib import Path  # python3 only

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


if __name__ == '__main__':
	# get the environment name
	env_name = os.getenv('FLASK_ENV', default='production')
	app = create_app(env_name)
	# run the app
	app.run()
