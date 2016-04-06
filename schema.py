from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/customers.db'
db = SQLAlchemy(app)

class Customer(db.Model):
	ID = db.Column(db.Integer, primary_key=True)
	Name = db.Column(db.String(25), nullable=False)
	Mobile = db.Column(db.String(10), nullable=False)
	Item = db.Column(db.String(25))
	Quantity = db.Column(db.Integer)

	def __init__(self, Name, Mobile, Item, Quantity):
		self.Name = Name
		self.Mobile = Mobile
		self.Item = Item
		self.Quantity = Quantity
