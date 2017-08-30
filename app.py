# """ module for the routes and views """
from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from models.user import User
from models.store import Store
from werkzeug.security import generate_password_hash, \
     check_password_hash
from datetime import datetime
from forms import RegisterForm, LoginForm

app = Flask(__name__)

# Configurations
app.secret_key = "&\xb2\xc8\x80^H\xef\xb7\xc9\xb11\\\xf0\xe5}\xdd\xb8[O\x0b\tK\x0e\xbe"

def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('Please Log into your ShoppingList Account first')
			return redirect(url_for('login'))
	return wrap

@app.route('/', methods=['GET', 'POST'])
def home():
	print(check_password_hash(session['storage']['password'], 'test'))
	error = None
	form = RegisterForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			new_user = User(
				username=request.form['username'],
				email=request.form['email'],
				password=generate_password_hash(request.form['password']),
				created_on=datetime.now()
			)			
			new_user.save_user()
			session['logged_in'] = True
			Store().store_session(new_user.user_data())
			flash('Welcome ' + session['storage']['username'])
			return redirect(url_for('dashboard'))
		return render_template("homepage.html", form=form, error=error)
	return render_template("homepage.html", form=form, error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	form = LoginForm(request.form)
	if request.method == 'POST':
		if form.validate_on_submit():
			if(request.form['username'] != session['storage']['email'])\
				or check_password_hash(session['storage']['password'], request.form['password']) is False:
				error = 'Invalid Credentials, Try Again'
			else:
				session['logged_in'] = True
				flash('Welcome back ' + session['storage']['username'])
				return redirect(url_for('dashboard'))
		else:
			return render_template("login.html", form=form, error=error)
	return render_template("login.html", form=form, error=error)

@app.route('/dashboard')
@login_required
def dashboard():
	return render_template("dashboard.html")

@app.route('/logout')
@login_required
def logout():
	session.pop('logged_in', None)
	flash('We hope you enjoyed organizing and sharing list see you soon')
	return redirect(url_for('home'))

if __name__ == '__main__':
	app.run(debug=True)