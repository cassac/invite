import os
from flask import render_template, url_for, redirect, request, flash
from flask.ext.login import login_required, login_user, logout_user, current_user
from . import main
from ..models import *
from forms import *
from .. import db, mail
from ..decorators import *
from werkzeug import secure_filename
from flask.ext.mail import Message
import datetime
from config import UPLOAD_FOLDER, email_config
import shortuuid
from sqlalchemy import desc

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'jpe' 'gif', 'pdf', 'wmv', 
	'mov', 'mpg', 'mpg4', 'mpeg', 'avi', 'mp4', 'doc', 'docx', 'txt'])
##################################
# HELPER FUNCTION FOR FLASK-UPLOAD
##################################
def allowed_file(filename):
	return '.' in filename and \
	       filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

############################
# VIEWS FOR 'MAIN' BLUEPRINT
############################
@main.route('/', methods=['GET', 'POST'])
@main.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			user.last_seen = datetime.datetime.utcnow()
			db.session.commit()
			return redirect(url_for('main.dashboard'))
		flash('Invalid username or password.')
	## USER REROUTED IF ALREADY LOGGED IN
	if not current_user.is_anonymous():
		return redirect(url_for('main.dashboard'))
	return render_template('login.html', form=form)

@main.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('main.login'))

@main.route('/guest/<email>/<status>', methods=['GET', 'POST'])
def guest_status(email, status):
	user = User.query.filter_by(email=email).first()
	user.status = status
	db.session.commit()
	flash("Invitation status updated to " + status)
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			user.last_seen = datetime.datetime.utcnow()
			db.session.commit()
			return redirect(url_for('main.dashboard'))
		flash('Invalid username or password.')

	return render_template('updatestatus.html', form=form, user=user)

@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
	user = User.query.filter_by(id=current_user.id).first()
	form = StatusForm(obj=user)
	if form.validate_on_submit():
		form.populate_obj(user)
		db.session.commit()
		flash('Your status was updated to ' + '"' + form.status.data + '"')
		return redirect(url_for('main.dashboard'))
	return render_template('dashboard.html', user=user, form=form)

@main.route('/pictures/add', methods=['GET', 'POST'])
@login_required
def add_pictures():
	form = AddPictureForm()
	if form.validate_on_submit():
		uploaded_files = request.files.getlist("file[]")
		filepath = []
		for file in uploaded_files:
			if file and allowed_file(file.filename.lower()):
				extension = file.filename.rsplit('.')[-1].lower()
				filename = (shortuuid.ShortUUID().random(length=3) + '_photo.' + extension)
				file.save(UPLOAD_FOLDER + '/' + filename)
				filepath.append(filename)
		for item in filepath:
			picture = Picture(filename=item, user_id=current_user.id)
			db.session.add(picture)
		db.session.commit()
		return redirect(url_for('main.dashboard'))
	return render_template('addpictures.html', form=form)

@main.route('/guests/view')
@login_required
def view_guests():
	guests = User.query.all()
	## USER'S OWN PICTURES ARE FILTERED OUT, RETRIEVES 8 MOST RECENT PICTURES
	pictures = Picture.query.filter(Picture.user_id!=current_user.id).order_by(Picture.timestamp.desc())[:8]
	return render_template('guests.html', guests=guests, pictures=pictures)

@main.route('/email/invitation', methods=['GET', 'POST'])
@login_required
@admin_required
def email_initation():
	form = EmailInvitationForm()
	if form.validate_on_submit():
		guests = User.query.filter(User.status=='Unconfirmed', User.emails_sent==0).all()
		for guest in guests:
			RECIPIENTS=[guest.email]
			SENDERINFO = ('Your name here', email_config['MAIL_USERNAME'])
			msg = Message(
		              "Title Of Email Here",
			       sender=SENDERINFO,
			       recipients=RECIPIENTS
			       )
			msg.body = render_template('email/invitation.txt', guest=guest)
			mail.send(msg)
			flash('Invitations sent')
			return redirect(url_for('main.dashboard'))
	return render_template('emailinvitation.html', form=form)

##############################
## POSSIBLE ADDITIONAL FEATURE
##############################
# @main.route('/guests/add')
# @login_required
# @admin_required
# def add_guests():
# 	return render_template('addguests.html')