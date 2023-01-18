from flask import Flask,render_template, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
 
 # flask instance
app = Flask(__name__)
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'scraping'

mysql = MySQL(app)

# # create database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql:///' + 'scraping'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

# APi object
api = Api(app)
# mysql = MySQL(app)
db = SQLAlchemy(app)

class insta_record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    posts = db.Column(db.String(80), nullable=False)
    followers = db.Column(db.String(80), nullable=False)
    following = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return f"{self.name} - {self.posts} - {self.followers} - {self.following}"


# Get
class GetPerson(Resource):
    def get(self):
        people_record = insta_record.query.all()
        people_record_list = []
        for people in people_record:
            peo_data = {'Id': people.id, 'Name': people.name, 'Posts': people.posts, 'Followers': people.followers, 'Following': people.following}
            people_record_list.append(peo_data)
        return {"people_record": people_record_list}, 200


api.add_resource(GetPerson, '/')

if __name__ == "__main__":
    app.run(host='localhost', port=5000)