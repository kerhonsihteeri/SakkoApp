import os

from flask import Flask, render_template, json, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)




app.secret_key = 'why would I tell you my secret key, you asshole?'



from models import User

@app.route("/")
def main():
	if __name__ == "__main__":
		app.run()
	return render_template('index.html')
	


@app.route('/showSignUp')
def showSignUp():
	return render_template('signup.html')
	
@app.route('/signUp' ,methods=['POST'])
def signUp():
	if request.method =='POST':
		user_name = request.form['inputName']
		user_email = request.form['inputEmail']
		user_password = request.form['inputPassword']
		user_username = None
		if not db.session.query(User).filter(User.user_email == user_email).count():
			reg = User(user_email)
			db.session.add(reg)
			db.session.commit()
		return render_template('success.html')
	return render_template ('index.html')
		
@app.route('/showSignIn')
def showSignIn():
	return render_template ('signin.html')

