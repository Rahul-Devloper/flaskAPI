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
        # Add multiple employees
        emp1 = Employee(first_name="John", last_name="Doe",
                        gender="Male", salary=60000)
        emp2 = Employee(first_name="Jane", last_name="Smith",
                        gender="Female", salary=65000)
        emp3 = Employee(first_name="Alice", last_name="Brown",
                        gender="Female", salary=70000)
        db.session.add_all([emp1, emp2, emp3])
        db.session.commit()
    print("Database tables created and employees added.")
    # Optionally, start the Flask app
    # app.run(debug=True)


# create a resource for the API
class GetEmployee(Resource):
    def get(self):
        employees = Employee.query.all()
        emp_list = []
        for emp in employees:
            emp_data = {
                "id": emp.id,
                "first_name": emp.first_name,
                "last_name": emp.last_name,
                "gender": emp.gender,
                "salary": emp.salary

            }
            emp_list.append(emp_data)
            return {"employees": emp_list}, 200

# add the resource to the API through POST request


class AddEmployee(Resource):
    def post(self):
        if request.is_json:
            emp = Employee(
                first_name=request.json['FirstName'],
                last_name=request.json['LastName'],
                gender=request.json['Gender'],
                salary=request.json['Salary']
            )
            db.session.add(emp)
            db.session.commit()
            return make_response(jsonify({"Id": emp.id, 'FirstName': emp.first_name, 'LastName': emp.last_name, 'Gender': emp.gender, 'Salary': emp.salary, 'message': 'Employee added successfully'}), 201)
        else:
            return make_response(jsonify({"message": "Request must be JSON"}), 400)


api.add_resource(GetEmployee, '/')
api.add_resource(AddEmployee, '/add')


if __name__ == "__main__":
    app.run(debug=True)
