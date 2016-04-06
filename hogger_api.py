from flask import Flask, jsonify, abort, request, url_for
from flask_sqlalchemy import SQLAlchemy
from schema import app, db, Customer, 

def make_public_details(customer):
    new_customer = {}
    for field in customer:
        if field == 'ID':
            new_customer['uri'] = url_for('get_customer', customer_id=customer['ID'], _external=True)
        else:
            new_customer[field] = customer[field]
    return new_customer

@app.route('/hogger/api/customers', methods=['GET'])
def get_customers():
	customers = Customer.query.all()
	customers = customers.fetchall()
	return jsonify({'customers': customers})

@app.route('/hogger/api/customers/<int:customer_id>')
def get_customer(customer_id):
	customer = Customer.query.get(customer_id)
	
	#if type(customer) != dict:
	#	abort(404)
	return jsonify({'customer': [make_public_details(customer)]})

@app.route('/hogger/api/customers', methods=['POST'])
def new_customer():
	if not request.json or not 'Name' in request.json or not 'Mobile' in request.json:
		abort(400)
	
	customer = Customer(request.json.Name, request.json.Mobile, request.json.get('Item',""), request.json.get('Quantity',""))
	#customer = Customer("pratyush","9574110221","CCD","1")
	
	db.session.add(customer)
	db.session.commit()
	
	return jsonify({'customer': customer}), 201

@app.route('/hogger/api/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
	customer = Customer.query.get(customer_id)
	
	if len(customer) == 0:
	   abort(404)
	if not request.json:
		abort(400)
	if 'Name' in request.json and type(request.json['Name']) != unicode:
		abort(400)
	if 'Mobile' in request.json and type(request.json['Mobile']) is not unicode:
		abort(400)
	if 'Item' in request.json and type(request.json['Item']) is not unicode:
		abort(400)
	if 'Quantity' in request.json and type(request.json['Quantity']) is not unicode:
		abort(400)
	
	customer.Name = request.json.get('Name', customer.Name)
	customer.Mobile = request.json.get('Mobile', customer.Mobile)
	customer.Item = request.json.get('Item', customer.Item)
	customer.Quantity = request.json.get('Quantity', customer.Quantity)
	
	db.session.commit()
	
	return jsonify({'customer': customer})

@app.route('/hogger/api/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
	customer = Customer.query.get(customer_id)
	
	if len(customer) == 0:
		abort(404)
	
	db.session.delete(customer)
	db.session.commit()
	
	return jsonify({'result': True})

if __name__ == '__main__':
	db.create_all()
	app.run(debug = True)
