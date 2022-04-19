from flask import Flask
from flask_restx import Api, Resource, fields
import RPi.GPIO as GPIO
import os
import glob
import time
import base64
from picamera import PiCamera

app = Flask(__name__)
api = Api(app,
          version='1.0',
          title='Used Tire Database',
          description="Database of current used tires",
          doc='/docs')

ns = api.namespace('tires', description='Tire operations')

tire = api.model('Tire', {
    'id': fields.Integer(readonly=True, description='The tire unique identifier'),
    'first': fields.String(required=True, description='First tire size number'),
    'second': fields.String(required=True, description='Second tire size number'), 
    'third': fields.String(required=True, description='Third tire size number'),
    'desc': fields.String(required=False, description='Tire description')

})

host = "0.0.0.0"
port = '8090'

tireid = '1'


class TireClass(object):
    def __init__(self):
    	self.counter = 0
    	self.tires = []
    def get(self, id):
    	for tire in self.tires:
    		if tire['id'] == id:
    			return tire
    	api.abort(404, "Tire {} doesn't exist".format(id))
    def create(self, data):
    	tire = data
    	tire['id'] = self.counter = self.counter + 1
    	self.tires.append(tire)
    	return tire
    def update(self, id, data):
    	tire = self.get(id)
    	tire.update(data)
    	return tire
    def delete(self, id):
    	tire = self.get(id)
    	self.tires.remove(tire)

DAO = TireClass()

@ns.route("/")
class Tires(Resource):

    @ns.doc('list_tires')
    @ns.marshal_list_with(tire)
    def get(self):
    	return DAO.tires

    @ns.doc('create_tire')
    @ns.expect(tire)
    @ns.marshal_with(tire, code=201)
    def post(self):
    	return DAO.create(api.payload), 201

@ns.route('/<int:id>')
@ns.response(404, 'Tire not found')
@ns.param('id', 'The tire identifier')
class Tire(Resource):
    @ns.doc('get_tire')
    @ns.marshal_with(tire)
    def get(self, id):
    	return DAO.get(id)
    @ns.doc('delete_tire')
    @ns.response(204, 'Tire Deleted')
    def delete(self, id):
    	DAO.delete(id)
    	return '', 204
    @ns.expect(tire)
    @ns.marshal_with(tire)
    def put(self, id):
    	return DAO.update(id, api.payload) 

if __name__ == '__main__':
    app.run(host, port, debug=True)
