from flask import Flask, request, jsonify, make_response
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

# create an instance of Flask
app = Flask(__name__) # __name__ is the name of the current module

# creating an instance of Api
api = Api(app)

# create database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# create a model for the database


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    salary = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"{self.first_name} {self.last_name} ({self.gender}) - ${self.salary}"


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # Example: add a test employee (optional)
        emp = Employee(first_name="John", last_name="Doe",
                       gender="Male", salary=60000)
        db.session.add(emp)
        db.session.commit()
    print("Database tables created.")
    # Optionally, start the Flask app
    # app.run(debug=True)
