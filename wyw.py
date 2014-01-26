#all the imports
import sqlite3
import json
from collections import Counter
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, jsonify
from contextlib import closing

DATABASE = 'wyw.db'
DEBUG = True
SECRET_KEY = 'development key'

USERNAME = 'admin'
PASSWORD = 'default'

#session variables
SESSION_USERNAME = ''
SESSION_PASSWORD = ''

adminmode = True

#creating the actual application
app = Flask(__name__)
app.config.from_object(__name__)

#initializes the database
def init_db():
	with closing(connect_db()) as db:
		with app.open_resource('schema.sql', mode='r') as f:
			db.cursor().executescript(f.read())
		db.commit()

#More elegant way of opening and closing requests
@app.before_request
def before_request():
	g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()

# connect to specified database
#can open a connection on request and also from he the interactive Python shell or a script
def connect_db():
	return sqlite3.connect(app.config['DATABASE'])

#Below starts all the code for the various views

@app.route('/')
def show_index():
	return render_template('index.html')

@app.route('/show_login')
def show_login():
	return render_template('login.html')

@app.route('/show_about')
def show_about():
	return render_template('About.html')

@app.route('/show_dishwasherform')
def show_dishwasherform():
	if not session['logged_in']:
		flash("You must login first!")
		return redirect(url_for('show_index'))
	return render_template('DishwasherForm.html')

@app.route('/show_showerform')
def show_showerform():
	if not session['logged_in']:
		flash("You must login first!")
		return redirect(url_for('show_index'))
	return render_template('shower.html')

@app.route('/show_watergardenform')
def show_watergardenform():
	if not session['logged_in']:
		flash("You must login first!")
		return redirect(url_for('show_index'))
	return render_template('watergarden.html')

@app.route('/show_washerform')
def show_washerform():
	if not session['logged_in']:
		flash("You must login first!")
		return redirect(url_for('show_index'))
	return render_template('washer.html')

@app.route('/show_waterconservationtips')
def show_waterconservationtips():
	return render_template("waterconservationtips.html")

@app.route('/show_log')
def show_log():
	return redirect(url_for('log'))

@app.route('/log')
def log():
	cur = g.db.execute('select Username, Password, currenttask, currenttime, currentproperty, id from entries order by id desc')
	entries = [dict(Username=row[0], Password=row[1], currenttask=row[2], currenttime=row[3], currentproperty=row[4], id=row[5]) for row in cur.fetchall()][::-1]

	#getting arrays for pie chart
	ctlistnames = []
	for i in range(len(entries)):
		ctlistnames.append(entries[i]["currenttask"])
	for i in range(len(ctlistnames)):
		for j in range(i + 1, len(ctlistnames)):
			if ctlistnames[i]< ctlistnames[j]:
				ctlistnames[i], ctlistnames[j] = ctlistnames[j], ctlistnames[i]
	lst = Counter(ctlistnames)
	ctlistnames_short = lst.keys()
	ctlistnumbers = lst.values()

	return render_template('log.html', entries=entries, adminmode=adminmode, ctlistnames_short=json.dumps(ctlistnames_short),ctlistnames=json.dumps(ctlistnames), ctlistnumbers=json.dumps(ctlistnumbers))

@app.route('/recording_data/<task>', methods=['GET', 'POST'])
def recording_data(task):
	if task == "dishwasher":
		dishwashertime = request.form['dishwashertime']
		dishwashercycle = request.form['dishwashercycle']
		g.db.execute('insert into entries (Username, Password, currenttask, currenttime, currentproperty) values (?, ?, ?, ?, ?)', [SESSION_USERNAME, SESSION_PASSWORD, 'Dishwasher',dishwashertime, dishwashercycle])
		g.db.commit()
	if task == 'shower':
		showertime = request.form['showertime']
		g.db.execute('insert into entries (Username, Password, currenttask, currenttime, currentproperty) values (?, ?, ?, ?, ?)', [SESSION_USERNAME, SESSION_PASSWORD, "Shower", showertime, ''])
		g.db.commit()
	if task == "watergarden":
		watergardentime = request.form['watergardentime']
		watergardenlevel = request.form['watergardenlevel']
		g.db.execute('insert into entries (Username, Password, currenttask, currenttime, currentproperty) values (?, ?, ?, ?, ?)', [SESSION_USERNAME, SESSION_PASSWORD, "Water Garden", watergardentime, watergardenlevel])
		g.db.commit()
	if task == "washer":
		washertime = request.form['washertime']
		washercycle = request.form['washercycle']
		g.db.execute('insert into entries (Username, Password, currenttask, currenttime, currentproperty) values (?, ?, ?, ?, ?)', [SESSION_USERNAME, SESSION_PASSWORD, "Laundry", washertime, washercycle])
		g.db.commit()
	return redirect(url_for('log'))


@app.route('/login', methods=['GET', 'POST'])
def login():
	global SESSION_USERNAME, SESSION_PASSWORD, adminmode
	error = None
	if request.method == 'POST':
		if request.form['username'] == app.config['USERNAME'] and request.form['password'] == app.config['PASSWORD']:
			session['logged_in'] = True
			adminmode = True
			SESSION_USERNAME = 'admin'
			SESSION_PASSWORD = request.form['password']
			print('You are logged in as ADMIN')
			return redirect(url_for('show_index'))
		else:
			session['logged_in'] = False
			adminmode = False
			flash('Incorrect Password or Username')
			return redirect(url_for('show_index'))
	return render_template('login.html', error=error)

@app.route('/logout')
def logout():
	global adminmode
	adminmode = False
	session['logged_in'] = False
	return redirect(url_for('show_index'))

#fires up server if we want to run this as a stand alone application
if __name__ == '__main__':
	#app.run(host = '0.0.0.0')
	app.run()