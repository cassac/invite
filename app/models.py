from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager
import datetime
import forgery_py
import random

class User(UserMixin, db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(64), unique=True, index=True)
	# password = db.Column(db.String(128))
	is_admin = db.Column(db.Boolean, default=0)
	name = db.Column(db.String(100))
	status = db.Column(db.String(20), default='Unconfirmed')
	last_contacted = db.Column(db.DateTime, default=datetime.datetime.now)
	emails_sent = db.Column(db.Integer, default=0)
	last_seen = db.Column(db.DateTime(), default=datetime.datetime.now)
	pictures = db.relationship('Picture', backref='user', lazy='dynamic')

	def __init__(self, name, email):
		self.name = name		
		self.email = email

	def __repr__(self):
		return '<%s, %s>' % (self.name, self.email)

	# @property
	# def password(self):
	# 	raise AttributeError('password is not a readable attribute')

	# @password.setter
	# def password(self, password):
	# 	self.password_hash = generate_password_hash(password)

	def verify_password(self, password):
		return password == 'password'
		## self not used
		# return check_password_hash(self.password_hash, password)

	## USED TO GENERATE FAKE USERS FOR TESTING
	@staticmethod
	def generate_fake(count=5):
		from sqlalchemy.exc import IntegrityError
		from random import seed
		import forgery_py
		seed()
		for i in range(count):
			u = User(email=forgery_py.internet.email_address(),
				name=forgery_py.name.first_name(),
				is_admin=False,
				status=random.choice(['unconfirmed', 'yes', 'no', 'maybe'])
				)
			db.session.add(u)
			try:
				db.session.commit()
			except IntegrityError:
				db.session.rollback()			

class Picture(db.Model):
	__tablename__ = 'picture'
	id = db.Column(db.Integer, primary_key=True)
	filename = db.Column(db.String(100))
	timestamp = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __init__(self, filename, user_id):
		self.filename = filename
		self.user_id = user_id

	def __repr__(self):
		return '<Picture %d, %s, %s>' % (self.id, self.filename, self.user_id)

	## USED TO GENERATE FAKE USERS FOR TESTING
	@staticmethod
	def generate_fake(count=5):
		from sqlalchemy.exc import IntegrityError
		from random import seed
		import forgery_py
		seed()
		for i in range(count):
			p = Picture(
				filename=random.choice(['image.jpg', 'picture.gif', 'photo.png']),
				user_id=1 #random.choice(range(1, 40))
				)
			db.session.add(p)
			try:
				db.session.commit()
			except IntegrityError:
				db.session.rollback()	

## HELPER FUNCTION
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))