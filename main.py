import os 
from flask import Flask
from application import config
from application.config import LocalDevelopmentConfig 
from application.database import db
from flask_bcrypt import Bcrypt

app = None

def createApp():
    app=Flask(__name__,template_folder="templates")
    app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()
    print(app)
    return app

app=createApp()

#app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///' + os.path.join(current_dir,'calibrationOfTools.sqlite3')

bcrypt=Bcrypt(app)

#from application.controllers import *
#from application.managerControllers import * 
from application.customerControllers import *

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5001')