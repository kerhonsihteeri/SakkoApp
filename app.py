from flask import Flask, render_template, json, request, redirect, session
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash


app = Flask(__name__)
mysql = MySQL()
app.secret_key = 'why would I tell you my secret key, you asshole?'


# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'imsyhm5uqwvmcb1a'
app.config['MYSQL_DATABASE_PASSWORD'] = 'z3vnrusg30ry8ivz'
app.config['MYSQL_DATABASE_DB'] = 'cygpdp7hgoack6lg'
app.config['MYSQL_DATABASE_HOST'] = 'o3iyl77734b9n3tg.cbetxkdyhwsb.us-east-1.rds.amazonaws.com'
mysql.init_app(app)

#Default setting
pageLimit = 50

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser


# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
# tab of
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.
DEVELOPER_KEY = "AIzaSyCGBwf_FniRboagzyQ9dYhJ78ytyEm3tm8"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

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
	
@app.route('/userHome')
def userHome():
	if session.get('user'):
		return render_template('userHome.html')
	else:	
		return render_template('error.html', error='Unauthorized Access')
		
@app.route('/showAddSakko')
def showAddSakko():
    return render_template('addSakko.html')
	
@app.route('/settings')
def settings():
	return render_template('settings.html')

@app.route('/logout')
def logout():
	session.pop('user',None)
	return redirect('/')

@app.route('/feed')
def feed():
	if session.get('user'):
		return render_template ('feedSakko.html')
	else:
		return render_template('error.html', error='Unauthorized Access')

@app.route('/video')
def video():
	return render_template('apisivu.html')
	
@app.route('/signUp',methods=['POST','GET'])
def signUp():
	try:
		_name = request.form['inputName']
		_username = request.form['inputUsername']
		_email = request.form['inputEmail']
		_password = request.form['inputPassword']
		
		
		# validate the received values
		if _name and _username and _email and _password:
			
			conn = mysql.connect()
			cursor = conn.cursor()
			_hashed_password = generate_password_hash(_password)			
			cursor.callproc('sp_createUser',(_name,_username,_email,_hashed_password))			
			data = cursor.fetchall()			

			if len(data) is 0:
				conn.commit()
				return json.dumps({'message':'User created successfully !'})
			else:
				return json.dumps({'error':str(data[0])})		
			
		else:
			return json.dumps({'html':'<span>Enter the required fields</span>'})
	except Exception as e:
		return json.dumps({'excepterror':str(e)})
	finally:
		cursor.close()
		conn.close()


	
@app.route('/validateLogin',methods=['POST'])
def validateLogin():
	try:
		_username = request.form['inputUsername']
		_password = request.form['inputPassword']
		
					
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.callproc('sp_validateLogin',(_username,))
		data = cursor.fetchall()
			
		if len(data) > 0:
			if check_password_hash(str(data[0][4]),_password):
				session['user'] = data [0][0]
				return redirect('/feed')
			else:
				return render_template('error.html',error = 'Wrong Username or Password.')
		else:
			return render_template('error.html',error = 'Wrong Email address or Password.')
	
		
	except Exception as e:
		return render_template('error.html',error = str(e))
	finally:
		cursor.close()
		conn.close()


	
@app.route('/addWish',methods=['POST'])
def addWish():
    try:
        if session.get('user'):
            _title = request.form['inputTitle']
            _maara= request.form['inputMaara']
            _description = request.form['inputDescription']
            _user = session.get('user')
 
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_addSakko',(_title,_maara,_description,_user))
            data = cursor.fetchall()
 
            if len(data) is 0:
                conn.commit()
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'An error occurred!')
 
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()
		
@app.route('/getWish',methods=['POST'])
def getWish():
	try:
		if session.get('user'):
			_user = session.get('user')
			_limit = pageLimit
			_offset = request.form ['offset']
			#print _offset
			_total_records = 0

			con = mysql.connect()
			cursor = con.cursor()
			cursor.callproc('sp_GetSakkoByUser',(_user,_limit,_offset,_total_records))
			wishes = cursor.fetchall()
			
			cursor.close()
			
			cursor = con.cursor()
			cursor.execute('SELECT @_sp_GetSakkoByUser_3');
			
			outParam = cursor.fetchall()

			response = []
			wishes_dict = []
			for wish in wishes:
				wish_dict = {
					'Id': wish[0],
					'Title': wish[1],
					'Description': wish[3],
					'Maara': wish[2],
					'Date': wish[5]}
				wishes_dict.append(wish_dict)
				
			response.append(wishes_dict)
			response.append({'total':outParam[0][0]})
			
			return json.dumps(response)
		else:
			return render_template('error.html', error = 'Unauthorized Access')
	except Exception as e:
		return render_template('error.html', error = str(e))
		
@app.route('/getWishById',methods=['POST'])
def getWishById():
    try:
        if session.get('user'):
 
            _id = request.form['id']
            _user = session.get('user')
 
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_GetSakkoById',(_id,_user))
            result = cursor.fetchall()
 
            wish = []
            wish.append({'Id':result[0][0],'Title':result[0][1],'Description':result[0][3],'Maara':result[0][2]})
 
            return json.dumps(wish)
        else:
            return render_template('error.html', error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
		
@app.route('/updateWish', methods=['POST'])
def updateWish():
	try:
		if session.get('user'):
			_user = session.get('user')
			_title = request.form['title']
			_maara = request.form['maara']
			_description = request.form['description']
			_wish_id = request.form['id']


			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.callproc('sp_updateSakko',(_title,_maara,_description,_wish_id,_user))
			data = cursor.fetchall()

			if len(data) is 0:
				conn.commit()
				return json.dumps({'status':'OK'})
			else:
				return json.dumps({'status':'ERROR'})
	except Exception as e:
		return json.dumps({'status':'Unauthorized access'})
	finally:
		cursor.close()
		conn.close()
		
@app.route('/deleteWish',methods=['POST'])
def deleteWish():
    try:
        if session.get('user'):
            _id = request.form['id']
            _user = session.get('user')
 
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_deleteSakko',(_id,_user))
            result = cursor.fetchall()
 
            if len(result) is 0:
                conn.commit()
                return json.dumps({'status':'OK'})
            else:
                return json.dumps({'status':'An Error occured'})
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return json.dumps({'status':str(e)})
    finally:
        cursor.close()
        conn.close()
		

@app.route('/getAllWishes')
def getAllWishes():
	try:
		if session.get('user'):

			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.callproc('sp_GetAllSakko')
			result = cursor.fetchall()

			wishes_dict = []
			for wish in result:
				wish_dict = {
					'Id': wish[0],
					'Title': wish[1],
					'Description': wish[3],
					'Maara': wish[2],
					'Date': wish[5]}
				wishes_dict.append(wish_dict)
			
			return json.dumps(wishes_dict)
		else:
			return render_template('error.html', error = 'Unauthorized Access')
	except Exception as e:
		return render_template('error.html', error = str(e))


@app.route('/getUser', methods=['POST'])
def getUser():
	try:
		if session.get('user'):
			_user = session.get('user')

			con = mysql.connect()
			cursor = con.cursor()
			cursor.callproc('sp_GetUserByUser',(_user,))
			users = cursor.fetchall()
            
			users_dict = []
			for user in users:
				user_dict={
					'Id': user[0],
					'Name': user[1],
					'Username': user[2],
					'Email': user[3]}
				users_dict.append(user_dict)
					
			return json.dumps(users_dict)
		else:
			return render_template('error.html', error = 'Unauthorized Access')
	except Exception as e:
		return json.dumps(str(e)) #render_template('error.html', error = str(e))

@app.route('/getUserById',methods=['POST'])
def getUserById():
	try:
		if session.get('user'):
			_user = session.get('user')

			con = mysql.connect()
			cursor = con.cursor()
			cursor.callproc('sp_GetUserByUser',(_user,))
			users = cursor.fetchall()
            
			users_dict = []
			for user in users:
				user_dict={
					'Id': user[0],
					'Name': user[1],
					'Username': user[2],
					'Email': user[3]}
				users_dict.append(user_dict)
			
			
			return json.dumps(users_dict)
		else:
			return render_template('error.html', error = 'Unauthorized Access')
	except Exception as e:
		return json.dumps(str(e)) #render_template('error.html', error = str(e))

		
@app.route('/updateUser', methods=['POST'])
def updateUser():
	try:
		if session.get('user'):
			_user = session.get('user')
			
			_username = request.form['username']
			_name = request.form['name']
			_email = request.form['email']
			_user_id = request.form['id']


			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.callproc('sp_updateUser',(_username,_name,_email,_user_id))
			data = cursor.fetchall()

			if len(data) is 0:
				conn.commit()
				return json.dumps({'status':'OK'})
			else:
				return json.dumps({'status':'ERROR'})
	except Exception as e:
		return json.dumps({'status':'Unauthorized accessA'})
	finally:
		cursor.close()
		conn.close()
		
@app.route('/deleteUser',methods=['POST'])
def deleteUser():
    try:
        if session.get('user'):
            _id = request.form['id']
            _user = session.get('user')
 
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_deleteUser',(_user))
            result = cursor.fetchall()
 
            if len(result) is 0:
                conn.commit()
                return json.dumps({'status':'OK'})
            else:
                return json.dumps({'status':'An Error occured'})
        else:
            return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return json.dumps({'status':str(e)})
    finally:
        cursor.close()
        conn.close()
		


@app.route('/youtube_search', methods=['POST'])
def youtube_search():
	youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
	developerKey=DEVELOPER_KEY)

	# Call the search.list method to retrieve results matching the specified
	# query term.
	search_response = youtube.search().list(
		q=request.form['tubehaku'],
		part="id,snippet",
		maxResults=25
	).execute()

	videos = {}
	channels = {}
	playlists = {}

	# Add each result to the appropriate list, and then display the lists of
	# matching videos, channels, and playlists.
	for search_result in search_response.get("items", []):
		if search_result["id"]["kind"] == "youtube#video":
			videos[search_result["snippet"]["title"]]="http://youtube.com/watch?v={0:.50s}".format(search_result["id"]["videoId"])
		elif search_result["id"]["kind"] == "youtube#channel":
			channels[search_result["snippet"]["title"]]="http://youtube.com/channel/{0:.50s}".format(search_result["id"]["channelId"])
		elif search_result["id"]["kind"] == "youtube#playlist":
			playlists[search_result["snippet"]["title"]]="http://youtube.com/playlist?list={0:.50s}".format(search_result["id"]["playlistId"])

	print ("Videos:\n", "\n".join(videos), "\n")
	print ("Channels:\n", "\n".join(channels), "\n")
	print ("Playlists:\n", "\n".join(playlists), "\n")



	return render_template('/videotulokset.html', videos=videos, playlists=playlists, channels=channels)	
	
	try:
		youtube_search(args)
	except HttpError as e:
		print ("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))
	
