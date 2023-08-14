from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a flask Instance
app = Flask(__name__)
# Add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user_ravi:user_ravi@54.175.148.134/mydb'
# Secret Key
app.config['SECRET_KEY'] = "This is my super secret key"

# Initialize the database
db = SQLAlchemy(app)

# Create Model
class Users(db.Model):
    id = db.Column(db.Integer(), primary_key=True,) 
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Create A String
    def __repr__(self):
        return '<Name %r>' % self.name



# create a form class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    submit = SubmitField("Submit")

# create a form class
class NamerForm(FlaskForm):
    name = StringField("What's your name", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/user/add", methods = ['GET', 'POST'])
def add_user():
    name = None
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        print(name)
        form.name.data = ''
        form.email.data = ''
        flash("From submited successfully!")
    our_users = Users.query.order_by(Users.id)
    return render_template("add_user.html",
                            form=form,
                            name = name,
                            our_users = our_users)

# Create a route decorator
@app.route('/')
def index():
    return render_template("index.html")
# local host:500/user/ravi
@app.route('/user/<name>')
def user(name):
    return render_template("user.html", name=name)

# create Custom Error Pages

#Invalid ULR
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

# internal Server Error
@app.errorhandler(500)
def server_error(e):
    return render_template("500.html")

@app.route("/name", methods=["GET", "POST"])
def name():
    name = None
    form = NamerForm()
    # Validate form
    if form.validate_on_submit():
        name = form.name.data
        print(form.submit.type)
        form.name.data = ''
        flash("From submited successfully!")
        
    return render_template('name.html',
                           name = name,
                           form = form)






if __name__=="__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)