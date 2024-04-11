#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)


class Plants(Resource):

    def get(self):
        plants = [plant.to_dict() for plant in Plant.query.all()]
        return make_response(jsonify(plants), 200)

    def post(self):
        data = request.get_json()

        new_plant = Plant(
            name=data['name'],
            image=data['image'],
            price=data['price'],
        )

        db.session.add(new_plant)
        db.session.commit()

        return make_response(new_plant.to_dict(), 201)
    
    

api.add_resource(Plants, '/plants')


class PlantByID(Resource):

    def get(self, id):
        plant = Plant.query.filter_by(id=id).first().to_dict()
        return make_response(jsonify(plant), 200)
    
    def patch(self, id):
        # Get the plant record from the database
        record = Plant.query.filter_by(id=id).first()
        
        # Check if the record exists
        if record:
            # Update the record with data from the JSON request body
            data = request.json
            for key, value in data.items():
                setattr(record, key, value)

            # Commit changes to the database
            db.session.commit()

            # Return the updated record in the response
            response_dict = record.to_dict()
            return make_response(jsonify(response_dict), 200)
        else:
            # Return 404 if the record does not exist
            return make_response(jsonify({'error': 'Plant not found'}), 404)

    def delete(self, id):
        # Get the plant record from the database
        record = Plant.query.filter_by(id=id).first()

        # Check if the record exists
        if record:
            # Delete the record from the database
            db.session.delete(record)
            db.session.commit()

            # Return a success response with status code 204
            return '', 204
        else:
            # Return 404 if the record does not exist
            return make_response(jsonify({'error': 'Plant not found'}), 404)

api.add_resource(PlantByID, '/plants/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
