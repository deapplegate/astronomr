from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.creole import Creole
from flask.ext.login import LoginManager

#############
### Set up app
app = Flask('astronomr', instance_relative_config=True) #look for things in the instance direcotry
app.config.from_object('astronomr.default_config')
app.config.from_pyfile('astronomr.cfg', silent = True) #overrides

db = SQLAlchemy(app)
creole = Creole(app)

login_manager = LoginManager()
login_manager.init_app(app)




#last but not least

from astronomr import views, model, forms





