import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

# Give access to the project in ANY OS we find ourselves in 
# Allows outside files/folders to be added to the project from the base directory

load_dotenv(os.path.join(basedir, '.env'))

class Config():
    """
    Set configuration variables for the flask app.
    Using environment variables where available.
    Otherwise create the config variable if not done already.
    """
    
    FLASK_APP = os.environ.get('FLASK_APP')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    SECRET_KEY = os.environ.get('SECRET_KEY') or "nana nana boo boo you'll never guess"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Turns off messages from SQLAlchemy regarding updates to our DB