from flask import Flask, render_template, json, request, redirect, session

from werkzeug import generate_password_hash, check_password_hash


app = Flask(__name__)

app.secret_key = 'why would I tell you my secret key, you asshole?'

import os
import psycopg2
import urlparse

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)

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

