from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import date, datetime

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


    def __repr__(self):
        return "{} - {}".format(self.aadhar, self.fname)


class Request(db.Model):

    aadhar = db.Column(db.Integer, unique=False, primary_key=True)
    fname = db.Column(db.String(30), unique=False, nullable=False)
    req_amount = db.Column(db.Integer, unique=False, nullable=False)
    dt = db.Column(db.DateTime, unique=False, nullable=False)

    def __repr__(self):
        return "{} - {} - {}".format(self.aadhar, self.fname, self.req_amount)



class Lending(db.Model):

    from_aadhar = db.Column(db.Integer, unique=False, primary_key=True)
    from_fname = db.Column(db.String(30), unique=False, nullable=False)
    to_aadhar = db.Column(db.Integer, unique=False)
    to_fname = db.Column(db.String(30), unique=False, nullable=False)
    amount = db.Column(db.Integer, unique=False, nullable=False)
    roi = db.Column(db.Float, unique=False, nullable=False)
    dt = db.Column(db.DateTime, unique=False, nullable=False)

    def __repr__(self):
        return "{}({}) lended {}({})  Rs{} at an interest rate of {}.".format(self.from_fname, self.from_aadhar, self.to_fname, self.to_aadhar, self.amount, self.roi)



@app.route("/")
def index():
    return render_template('index.html')


@app.route("/login")
def login():
    return render_template('login.html')


@app.route("/signup")
def signup():
    return render_template('signup.html')


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():

    params={}

    params['requests'] = []

    for req in Request.query.all():
        params['requests'].append((req.aadhar, req.fname, req.req_amount, req.dt))

    params['lendings'] = []

    for lending in Lending.query.all():
        params['lendings'].append((lending.from_aadhar, lending.from_fname, lending.to_aadhar, lending.to_fname, lending.amount, lending.roi, lending.dt))

    print(params)

    if request.method == 'POST':
        aadhar = request.form.get('aadhaar')
        fname = request.form.get('first-name')
        lname = request.form.get('last-name')
        email = request.form.get('email')
        password = request.form.get('pass')
        phone = request.form.get('phnno')
        occupation = request.form.get('occupation')
        
        year  = int(request.form.get('dob')[:4])
        month =  int(request.form.get('dob')[5:7])
        day = int(request.form.get('dob')[8:10])
        dob = date(year,month,day)

        income = request.form.get('income')


        peer = Peer(aadhar=aadhar, fname=fname, lname=lname, email=email, password=password, phone=phone, occupation=occupation, dob=dob, income=income)
        db.session.add(peer)
        db.session.commit()

    return render_template('dashboard.html', params=params)


@app.route('/request_confirm', methods=['GET', 'POST'])
def request_confirm():
    if request.method == 'POST':
        aadhar = request.form.get('aadhaar')
        fname = request.form.get('name')
        req_amount = request.form.get('reqamount')
        dt = datetime.now()

        req = Request(aadhar=aadhar, fname=fname, req_amount=req_amount, dt=dt)
        db.session.add(req)
        db.session.commit()

    return render_template('req_cnf.html')


@app.route('/transact_confirm', methods=['GET', 'POST'])
def transact_confirm():
    if request.method == 'POST':
        from_aadhar = request.form.get('from_aadhaar')  
        from_fname = request.form.get('from_fname')
        to_aadhar = request.form.get('to_aadhaar')
        to_fname = request.form.get('to_fname')
        amount = request.form.get('amount')
        roi = request.form.get('roi')
        dt = datetime.now()

        lending = Lending(from_aadhar=from_aadhar, from_fname=from_fname, to_aadhar=to_aadhar, to_fname=to_fname, amount=amount, roi=roi, dt=dt)
        db.session.add(lending)
        db.session.commit()

    return render_template('txn_cnf.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)