from operator import and_
from flask import Flask, url_for, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api

####################################################################################
# Configuration                                                                    #
####################################################################################

#initialize app
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

#initialize API
api = Api(app)

CORS(app)

#initialize sqlalchemy
db = SQLAlchemy(app)

#initialize marshmallow
ma = Marshmallow(app)

#Initialize Blueprint
from project.company import company
from project.item import item
from project.invoice import invoice
from project.summary import summary
# from project.summary import summary
# from project.summary2 import summary2
# from project.activity import activity

app.register_blueprint(company,url_prefix='/company')
app.register_blueprint(item,url_prefix='/item')
app.register_blueprint(invoice,url_prefix='/invoice')
app.register_blueprint(summary,url_prefix='/summary')

# app.register_blueprint(summary,url_prefix='/summary')
# app.register_blueprint(summary2,url_prefix='/summary2')

# app.register_blueprint(activity,url_prefix='/activity')

def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)



##to create table in db

# flask shell
# from project import db
# db.create_all()
