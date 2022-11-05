from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import date

db_name = 'users.sqllite3'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Peer(db.Model):

    aadhar = db.Column(db.Integer, unique=True, primary_key=True)
    fname = db.Column(db.String(30), unique=False, nullable=False)
    lname = db.Column(db.String(30), unique=False, nullable=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=False, nullable=False)
    phone = db.Column(db.Integer, unique=True, nullable=False)
    occupation = db.Column(db.String(30), unique=False, nullable=False) 
    dob = db.Column(db.DateTime, unique=False, nullable=False)
    income = db.Column(db.Integer, unique=False, nullable=False)

    # def __init__(self, aadhar, ):
        
    #     self.aadhar = aadhar

    def __repr__(self):
        return "{} - {}".format(self.aadhar, self.fname)



@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/signup")
def signup():
    aadhar = request.form['']
    peer = Peer(aadhar=123, fname='Vishesh', lname='Kumar Singh', email='visheshkrsinghofficial@gmail.com', password='password', phone='8057900850', occupation='Student', dob=date(2001, 11, 4), income=4000)
    db.session.add(peer)
    db.session.commit()
    return render_template('signup.html')

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)