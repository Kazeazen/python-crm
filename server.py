'''
Author: James Thomason
'''

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import secrets_for_backend
from utils import format_employee_data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:' + secrets_for_backend.POSTGRES_PASS + '@localhost/crm-db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Employee(db.Model):
    __tablename__ = "Employee"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20), nullable = False)
    job_title = db.Column(db.String(50), nullable = False)
    years_xp = db.Column(db.Integer)

    def __repr__(self):
        return f"{self.name} -- {self.job_title}"
    
    def __init__(self, name, job_title, years_xp):
        self.name = name
        self.job_title = job_title
        self.years_xp = years_xp
        

@app.route("/employees", methods=["GET", "POST"])
def get_all_employees():
    if request.method == "GET":
        all_employees = Employee.query.all()
        output = []
        for employee in all_employees:
            emp_data = {'id':employee.id, 'name': employee.name, 'job_title': employee.job_title, 'years_xp': employee.years_xp}
            output.append(emp_data)
        return {"employees": output}

    if request.method == "POST":
        emp_name = request.json.get("name", None)
        emp_job_title = request.json.get("job_title", None)
        emp_years_xp = request.json.get("years_xp", None)
        if None in (emp_name, emp_job_title, emp_years_xp):
            return "Improper data, retry", 400
        new_employee = Employee(emp_name, emp_job_title, emp_years_xp)
        db.session.add(new_employee)
        db.session.commit()
        return {"Status":"Successfully added new Employee"}

@app.route("/employee/<id>", methods=["GET","DELETE","PUT"])
def get_one_employee(id):
    if request.method == "GET":
        employee_query = Employee.query.get_or_404(id)
        return format_employee_data(employee_query)
    if request.method == "DELETE":
        employee_query = Employee.query.get_or_404(id)
        db.session.delete(employee_query)
        db.session.commit()
        return {"data": format_employee_data(employee_query)}
    if request.method == "PUT":
        employee_query = Employee.query.get_or_404(id)
        emp_name = request.json.get("name", None)
        emp_job_title = request.json.get("job_title", None)
        emp_years_xp = request.json.get("years_xp", None)
        if None in (emp_name, emp_job_title, emp_years_xp):
            return "Improper data, retry", 400
        employee_query.name = emp_name
        employee_query.job_title = emp_job_title
        employee_query.years_xp = emp_years_xp
        db.session.commit()
        return {"status":"Data has been updated"}

if __name__ == "__main__":
    app.run(debug=True)