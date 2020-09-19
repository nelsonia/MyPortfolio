from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://portfolio:jommo@localhost/porfolio'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://fxpusgkkadodhn:2cf75df4f148f1bcd89a18d4b68d1f07a7ed81fc7c4ea2b6a26ab3065b2e639c@ec2-52-200-48-116.compute-1.amazonaws.com:5432/d2v9slmmft84pm'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Feedbacks(db.Model):
    __tablename__ = 'feedbacks'
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(200), unique=True)
    Email = db.Column(db.String(200))
    Subject = db.Column(db.String(200))
    Message = db.Column(db.Text())

    def __init__(self, Name, Email, Subject, Message):
        self.Name = Name
        self.Email = Email
        self.Subject = Subject
        self.Message = Message


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        Name = request.form['Name']
        Email = request.form['Email']
        Subject = request.form['Subject']
        Message = request.form['Message']
        # print(customer, dealer, rating, comments)
        if Name == '' or Name == '':
            return render_template('index.html', message='Please enter required fields')
        if db.session.query(Feedbacks).filter(Feedbacks.Name == Name).count() == 0:
            data = Feedbacks(Name, Email, Subject, Message)
            db.session.add(data)
            db.session.commit()
            return render_template('index.html')
        return render_template('index.html', message='Thank You for your Feedback')


if __name__ == '__main__':
    app.run()
