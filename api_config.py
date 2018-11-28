# import semua module yang dibutuhkan
from flask import Flask, jsonify, request, send_file
from flask_restful import Api, Resource, reqparse, marshal, fields
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc, ForeignKey, text, func
from sqlalchemy.orm import relationship
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_jwt_extended import jwt_required, JWTManager, create_access_token, get_jwt_identity, get_jwt_claims, verify_jwt_in_request
from functools import wraps
from flask_cors import CORS
import sys
import datetime
# pengaturan app
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:sipsalphatech123@sips-db.cedjkayreeam.ap-southeast-1.rds.amazonaws.com/sips_database'
app.config['SQLALCHEMY_ECHO']=True
app.config['JWT_SECRET_KEY'] = 'SFsieaaBsLEpecP675r243faM8oSB2hV'
api = Api(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)

#==========================================JWT====================================
def guru_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['id_guru'] is None:
            return {'message':'FORBIDDEN'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper

def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['id_admin'] is None:
            return {'message':'FORBIDDEN'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper
