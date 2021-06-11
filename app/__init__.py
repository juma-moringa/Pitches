from flask import Flask
from flask_mail import Mail
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config_options

#initialize extensions

mail = Mail()
bootstrap = Bootstrap()
db = SQLAlchemy()
photos = UploadSet("photos", IMAGES)

def create_app(config_name):

    """
    This is a function that will initialize the Flask instance
    """
    
    #instantiate Flask

    app = Flask(__name__)

    #add the configurations

    app.config.from_object(config_options[config_name])

    #initialize the extensions
    
    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)

    #initialize the uploads

    configure_uploads(app,db)

    return app