from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
# from flask_mail import Mail, Message


app = Flask(__name__)

ENV = 'dev'

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
        Subject = request.form['Subject']
        Message = request.form['Message']
        Email = request.form['Email']

        # message ="your feedback is well received"
        # server = smtplib.SMTP("smtp.gmail.com" , 587)
        # server.starttls()
        # server.login ("dvjnelsonia@gmail.com", "")
        # server.sendmail("dvjnelsonia@gmail.com" ,Email, message)
        


        # mail= Mail(app)

        # app.config['MAIL_SERVER']='smtp.gmail.com'
        # app.config['MAIL_PORT'] = 465
        # app.config['MAIL_USERNAME'] = 'dvjstaciah@gmail.com'
        # app.config['MAIL_PASSWORD'] = ''
        # app.config['MAIL_USE_TLS'] = False
        # app.config['MAIL_USE_SSL'] = True
        # mail = Mail(app)


        # msg = Message('Hello', sender = 'dvjstaciah@gmail.com', recipients = 'dvjstaciah@gmail.com')
        # msg.body = "Hello Flask message sent from Flask-Mail"
        # mail.send(msg)
        # return "Sent"

        # print(customer, dealer, rating, comments)
        if Name == '' or Name == '':
            return render_template('index.html', message='Please enter required fields')
        if db.session.query(Feedbacks).filter(Feedbacks.Name == Name).count() == 0:
            data = Feedbacks(Name, Email, Subject, Message)
            db.session.add(data)
            db.session.commit()
            return render_template('success.html')
        return render_template('success.html', message='Thank You for your Feedback')


if __name__ == '__main__':
    app.run()
