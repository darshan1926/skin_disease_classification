# Store this code in 'app.py' file
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
from keras.preprocessing.image import save_img
import cv2 as cv
import numpy as np
import keras.models
import re
import sys 
import os
import base64
sys.path.append(os.path.abspath("./model"))
from load import * 


app = Flask(__name__)
app.config["ALLOWED_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF"]
app.config['UPLOAD_FOLDER'] = 'uploads'

def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_EXTENSIONS"]:
        return True
    else:
        return False

app.secret_key = 'Darshan'

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['PORT']='3306'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Darshan@1926'
app.config['MYSQL_DB'] = 'skin'

mysql = MySQL(app)

@app.route('/')
@app.route('/Login', methods =['GET', 'POST'])
def login():
    
	msg = ''
	if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
		email = request.form['email']
		password = request.form['password']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM singup WHERE email = % s AND password = % s', (email, password, ))
		account = cursor.fetchone()
		if account:
			session['loggedin'] = True
			session['email'] = account['email']
			session['password'] = account['password']
			msg = 'Logged in successfully !'
			return render_template('afterlogin.html',msg = msg)
		else:
			msg = 'Incorrect username / password !'
	return render_template('Login.html', msg = msg)
"""def convertImage(imgData1):
	imgstr = re.search(b'base64,(.*)',imgData1).group(1)
	with open('output.png','wb') as output:
	    output.write(base64.b64decode(imgstr))"""
        
        
@app.route('/predict_image/', methods=['GET', 'POST'])
def render_message():
    # Loading CNN model
    if request.method == 'POST':
        file = request.file['desises_image']
        if 'file' not in request.files:
            return render_template('afterlogin.html')

        if file.filename == '':
            return render_template('afterlogin.html')

        if file and allowed_image(file.filename):
            filename = secure_filename(file.filename)
            full_filename=file.save(os.path.join(app.config['UPLOAD_FOLDER'],  filename))
            

    predict()
    return render_template("afterlogin.html", user_image = full_filename)

"""@app.route('/predict/',methods=['GET','POST'])
def predict():
    
	imgData = request.file()
	img=convertImage(imgData)
	x = cv.imread('ISIC_0034316.jpg',mode='L')
	x = np.invert(x)
	x = cv.imresize(x,(28,28))
	x = x.reshape(1,28,28,1)

	with graph.as_default():
		out = model.predict(x)
		print(out)
		print(np.argmax(out,axis=1))

		response = np.array_str(np.argmax(out,axis=1))
		return response	"""

@app.route('/logout')
def logout():
	session.pop('Loggedin', None)
	session.pop('email', None)
	session.pop('password', None)
	return redirect(url_for('Login'))

@app.route('/register', methods =['GET', 'POST'])
def register():
	msg = ''
	if request.method == 'POST' and 'username'  in request.form and 'email' in request.form and 'password'  in request.form :
		name = request.form['username']
		password = request.form['password']
		email = request.form['email']
		cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
		cursor.execute('SELECT * FROM singup WHERE name = % s', (name, ))
		account = cursor.fetchone()
		if account:
			msg = 'Account already exists !'
		elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
			msg = 'Invalid email address !'
		elif not re.match(r'[A-Za-z0-9]+', name):
			msg = 'Username must contain only characters and numbers !'
		elif not name or not password or not email:
			msg = 'Please fill out the form !'
		else:
			cursor.execute('INSERT INTO singup VALUES ( % s, % s, % s)', (name, email, password, ))
			mysql.connection.commit()
			msg = 'You have successfully registered !'
	elif request.method == 'POST':
		msg = 'Please fill out the form !'
	return render_template('registration.html', msg = msg)
if __name__ == '__main__':
    app.run(debug=True, port=8000)


