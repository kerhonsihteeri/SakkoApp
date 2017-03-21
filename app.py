from flask import Flask, render_template, json, request, redirect, session
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash


app = Flask(__name__)

app.secret_key = 'why would I tell you my secret key, you asshole?'



@app.route("/")
def main():
	if __name__ == "__main__":
		app.run()
	return render_template('index.html')
	


@app.route('/showSignUp')
def showSignUp():
	return render_template('signup.html')
	

@app.route('/showSignIn')
def showSignIn():
	return render_template ('signin.html')

