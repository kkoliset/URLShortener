import sqlite3
from flask import Flask, render_template, request, redirect, url_for
import string
import random
import logging
from logging import Formatter, FileHandler
from datetime import datetime

'''*****************************************************************************
 * @app.py
 *
 * @date 08/23/22
 * @author Keerthana Kolisetty
 *
 * @Summary
 * Create short urls from user inputted URls.
 *
 *****************************************************************************'''


app = Flask(__name__)
app.debug = True

handler = logging.FileHandler("test.log")
app.logger.addHandler(handler)
app.logger.setLevel(logging.DEBUG) 

@app.route('/', methods=('GET', 'POST'))
def index():
	error = "Incorrect Username/Password"
	conn = get_db_connection()

	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']

		#Get associated username and password from database and see if they match
		userData = conn.execute("SELECT password FROM AuthenticatedUsers WHERE username='%s'" % (username)).fetchone()
		if(userData is not None):
			dbPassword = userData['password']
			conn.close()
			
			if dbPassword==password:
				#Username and pawssword that user put it correct take user to Url Shortener page.
				app.logger.info(getCurrentDateTime()+'%s Logged in', username)
				return redirect(url_for('urlShortener'))

		#Username/password was incorrect		
		app.logger.info(getCurrentDateTime()+ username + " - Failure to Login")
		return render_template('index.html', error=error)
	return render_template('index.html')


@app.route('/urlShortener', methods=('GET', 'POST'))
def urlShortener():
    conn = get_db_connection()
    if request.method == 'POST':
        url = request.form['url']
        app.logger.info(getCurrentDateTime()+"URL To Shorten: "+ url)

        customerURLOption = request.form['chk']

        # If customer wanted a custom short URl
        if(customerURLOption == "Yes"):
            app.logger.info(getCurrentDateTime()+"Custom URL option was choosen")
            customUrl = request.form['custom_url'].lower()
            app.logger.info(getCurrentDateTime()+"Custom URL choosen: customUrl")
            
            #check to see if URL already exists in database
            short_url=URLExist(conn, url)
            if (short_url !=""):
                app.logger.info(getCurrentDateTime()+"URL Already Exists: "+ url)
                return render_template('urlShortener.html',short_url_exist=short_url, customURLCheck="YES")
            
            #Check to see if custom short url that user provided exists in database   
            if (DoesCustomURLExist(conn, customUrl)):
                app.logger.info(getCurrentDateTime()+"Custom Short URL Already Exists")
                return render_template('urlShortener.html', customURLCheck = "YES", error="Custom URL Already exists, please try another one")
      
            # update url with custom short url in database
            updateURLShortURL(conn, url, customUrl)
            app.logger.info(getCurrentDateTime()+"Custom Short URL created"+ request.host_url+customUrl)
            return render_template('urlShortener.html',short_url=request.host_url+customUrl, customURLCheck="YES")

        #If customer deosnt want a custom short URl
        #check to see if URL already exists in database
        short_url=URLExist(conn, url)
        if (short_url !=""):
            app.logger.info(getCurrentDateTime()+"URL Already Exists: "+ url)
            return render_template('urlShortener.html',short_url_exist=short_url, customURLCheck="NO")
        
        #randomly create short URL and check to see if already in database. If so, keep creating another one.
        short_url_id = createShortURLID()
        app.logger.info(getCurrentDateTime()+"Short URL Randonmly Generated: "+ short_url_id)
        while(DoesCustomURLExist(conn,short_url_id)):
            short_url_id=createShortURLID()
            app.logger.info(getCurrentDateTime()+"Short URL Randonmly Generated Again, Previous one Existed: "+ short_url_id)
       
        # update url with short url in database
        short_url = request.host_url + short_url_id
        updateURLShortURL(conn, url, short_url_id)
        app.logger.info(getCurrentDateTime()+"Random Short URL created"+ short_url)
        return render_template('urlShortener.html', short_url=short_url,  customURLCheck="NO")

    return render_template('urlShortener.html')




@app.route('/<short_url_id>')
def url_redirect(short_url_id):
    conn = get_db_connection()

    #get data from database based on short_url_id
    url_data = conn.execute("SELECT original_url, count FROM urls WHERE short_url_id='%s'" % (short_url_id)).fetchone()
    if(url_data is not None):
        #if short_url_id was found in database
        original_url = url_data['original_url']

        #update count of url in database
        count = url_data['count']
        conn.execute("UPDATE urls SET count = '%i' WHERE original_url = '%s'" % (count+1, original_url))
        conn.commit()
        conn.close()

        #Redirect to original url
        return redirect(original_url)
    else:
        #if short_url_id was not found in database
        return render_template('urlShortener.html', error="Invalid URL")


@app.route('/allURLs')
def allURLs():
    conn = get_db_connection()
    #get all URL data from databasde
    allURLs = conn.execute('SELECT * FROM urls ORDER BY count DESC').fetchall()

    urls = []
    for url in allURLs:
        url = dict(url)
        url['short_url'] = request.host_url + url['short_url_id']
        urls.append(url)

    conn.close()
    return render_template('allURLs.html', urls=urls)


#Get Database connection
def get_db_connection():
    conn = sqlite3.connect('URLShortenerDB.db')
    conn.row_factory = sqlite3.Row
    return conn

def getCurrentDateTime():
	#getting current date and time for logging
	dt_string = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
	dt_string = dt_string + " - "
	return dt_string

#Check if url already exists in database. 
def URLExist(conn, url):
	doesURLExist = conn.execute("SELECT short_url_id FROM urls WHERE original_url='%s'" % (url)).fetchone()
	if(doesURLExist is not None):
		short_url_id = doesURLExist['short_url_id']
		short_url = request.host_url + short_url_id
		return short_url
	else:
 		return ""

#Check if customer short_url_id exists
def DoesCustomURLExist(conn, customUrl):
	doesShortURLExist = conn.execute("SELECT short_url_id FROM urls WHERE short_url_id='%s'" % (customUrl)).fetchone()
	if(doesShortURLExist is not None):
		return True
	else:
		False

#Update database with url and associated short_url_id
def updateURLShortURL(conn, url, short_url_id):
	url_data = conn.execute("INSERT INTO urls (original_url, short_url_id) VALUES ('%s', '%s')" % (url, short_url_id))
	conn.commit()
	conn.close()

#Create a 4-letter random short_url_id
def createShortURLID():
	short_url_id = ""
	for x in range(0,4):
		#randomly creating letters
		randomLetter = random.choice(string.ascii_lowercase)
		short_url_id = short_url_id+randomLetter
	return short_url_id

