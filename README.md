# python-crm

Basic Flask api that allows anyone to create a new employee, given the data in a JSON format with name, job_title, and years_xp<br>
a simple example:<br>
{"name":"James","job_title":"xxxxx","years_xp":"0"}<br>
<br>
localhost:5000/employees (accepts GET and POST requests)<br>
localhost:5000/employee/<id> (accepts GET, PUT, DELETE requests)<br>
these are the only two open endpoints within the api. There is no authentication needed, its simply an open api.
