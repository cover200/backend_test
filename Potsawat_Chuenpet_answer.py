from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import sqlite3

app = Flask(__name__)
api = Api(app)

class User_Id(Resource):
    def get(self, id):
        with sqlite3.connect('user.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE id=?",(id,))
            row = c.fetchone()
            if type(row) is not tuple:
                return 'No Content!', 204
            else: return row

class User_Fname(Resource):
    def get(self, fName):
        with sqlite3.connect('user.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE first_name=?",(fName,))
            rows = c.fetchall()
            if len(rows) < 1:
                return 'No Content!', 204
            else :
                return rows

class User_Lname(Resource):
    def get(self, lName):
         with sqlite3.connect('user.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE last_name=?",(lName,))
            rows = c.fetchall()
            if len(rows) < 1:
                return 'No Content!', 204
            else :
                return rows

class User_Email(Resource):
    def get(self, email):
        with sqlite3.connect('user.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE email=?",(email,))
            row = c.fetchone()
            if type(row) is not tuple:
                return 'No Content!', 204
            else: return row               

class User_Age(Resource):
    def get(self, age):
        with sqlite3.connect('user.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE age=?",(age,))
            rows = c.fetchall()
            if len(rows) < 1:
                return 'No Content!', 204
            else: return rows

class User_RangeAge(Resource):
    def get(self, age1, age2):
         with sqlite3.connect('user.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE age BETWEEN ? AND ?",(age1,age2,))
            rows = c.fetchall()
            if len(rows) < 1:
                return 'No Content!', 204
            else :
                return rows

class User_Gender(Resource):
    def get(self, gender):
         with sqlite3.connect('user.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE gender=?",(gender,))
            rows = c.fetchall()
            if len(rows) < 1:
                return 'No Content!', 204
            else :
                return rows

class User_Edit(Resource):      #Not working yet
    def put(self):
        data = request.get_json()

        user_id = data['id']
        fName = data['first_name']
        lName = data['last_name']
        email = data['email']
        gender = data['gender']
        age = data['age']

        with sqlite3.connect('user.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE id=?",(user_id,))
            row = c.fetchone()
            if type(row) is not tuple:
                return 'No Content!', 204
            else:
                c = conn.cursor()
                c.execute("UPDATE users SET first_name=?, last_name=?, email=?, gender=?,\
                        age=? WHERE id=?",(fName, lName, email, gender, age, user_id,))
                c.commit()
                return 200

    def post(self):
        data = request.get_json()
        
        user_id = data['id']
        fName = data['first_name']
        lName = data['last_name']
        email = data['email']
        gender = data['gender']
        age = data['age']
        
        with sqlite3.connect('user.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE id=? OR (first_name=? AND last_name=?)\
                        OR email=?", (user_id, fName, lName, email,))
            row = c.fetchone()
            if type(row) is tuple:
                return 'Conflict Resource', 409
            else:
                c.execute("INSERT INTO users (id, first_name, last_name, email, gender, age)\
                            VALUES (?, ?, ?, ?, ?, ?)", (user_id, fName, lName, email, gender, age))
                c.commit()
                return 201

    def delete(self):
        data = request.get_json()

        user_id = data['id']
        
        with sqlite3.connect('user.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM users WHERE id=?",(user_id,))
            row = c.fetchone()
            if type(row) is not tuple:
                return 'No Content!!', 204
            else: 
                c.execute("DELETE FROM users WHERE id=?", (user_id,))
                c.commit()
                return 202

api.add_resource(User_Id, '/users/id=<int:id>')
api.add_resource(User_Fname, '/users/fName=<string:fName>')
api.add_resource(User_Lname, '/users/lName=<string:lName>')
api.add_resource(User_Email, '/users/email=<string:email>')
api.add_resource(User_Age, '/users/age=<int:age>')
api.add_resource(User_RangeAge, '/users/age=<int:age1>-<int:age2>')
api.add_resource(User_Gender, '/users/gender=<string:gender>')
api.add_resource(User_Edit, '/user/edit')

if __name__ == '__main__':
    app.run(debug=True)