from app import db
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime


#creating userdb model
class User(db.Model):
	__tablename__ = "tbl_user"
	user_id = db.Column(db.Integer, primary_key=True)
	user_name = db.Column(db.Varchar(45))
	user_username = db.Column(db.Varchar(45), unique=True)
	user_email = db.Column(db.Varchar(120), unique=True)
	user_password = db.Column(db.Varchar(256))
	
#cearing sakkodb model	
class Sakko (db.Model):
	__tablename__ = "tbl_sakko"
	sakko_id = db.Column(db.Integer, primary_key=True)
	sakko_title = db.Column(db.Varchar(45))
	sakko_description = db.Column(db.Varchar(5000))
	sakko_user_id = db.Column(db.Integer)
	sakko_date = db.Column(db.datetime)