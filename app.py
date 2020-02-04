from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy			# instead of mysqlconnection
from sqlalchemy.sql import func                         # ADDED THIS LINE FOR DEFAULT TIMESTAMP
from flask_migrate import Migrate			# this is new
app = Flask(__name__)
# configurations to tell our app about the database we'll be connecting to
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_table.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# an instance of the ORM
db = SQLAlchemy(app)
# a tool for allowing migrations/creation of tables
migrate = Migrate(app, db)




#### ADDING THIS CLASS ####
# the db.Model in parentheses tells SQLAlchemy that this class represents a table in our database



class User(db.Model):	
    # __tablename__ = "users"    # optional		
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    email = db.Column(db.String(45))
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=func.now())    # notice the extra import statement above
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
# routes go here...



@app.route('/')
def index():
    return render_template('index.html')



@app.route('/create_user', methods=['POST'])
def create_user():

    first_name = request.form['fname']
    last_name = request.form['lname']
    email = request.form['email']
    age = request.form['age']

    new_user = User(first_name=first_name, last_name = last_name, email=email, age=age)
    db.session.add(new_user)
    db.session.commit()

    list_of_users = User.query.all()


    return render_template('index.html', userList=list_of_users)







if __name__ == "__main__":
    app.run(debug=True)




















