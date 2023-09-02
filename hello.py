from flask import Flask, render_template, flash, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Create a flask Instance
app = Flask(__name__)
# Add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user_ravi:user_ravi@54.175.148.134/mydb1'
# Secret Key
app.config['SECRET_KEY'] = "This is my super secret key"

# Initialize the database
db = SQLAlchemy(app)

migrate = Migrate(app, db)




# Create Model
class Users(db.Model):
    id = db.Column(db.Integer(), primary_key=True,) 
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False, unique=True)
    favorite_color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    # create some password stuff...
    password_hash = db.Column(db.String(128))
    
    @property
    def password(self):
        raise AttributeError('Password is not a readable Attribute!')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    # Create A String
    def __repr__(self):
        return '<Name %r>' % self.name


@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    name=None
    form = UserForm()

    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User deleted successfully!!")

        our_users = Users.query.order_by(Users.id)
        return render_template("add_user.html",
                            form=form,
                            name=name,
                            our_users=our_users)
    except:
        flash("Whoops! There was a problem deleting user, Try again...")
        return render_template("add_user.html",
                            form=form, name=name, our_users=our_users)


# create a form class
class UserForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite color")
    submit = SubmitField("Submit")
    
#update database record
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    form = UserForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.name = request.form['name']
        name_to_update.email = request.form['email']
        name_to_update.favorite_color = request.form['favorite_color']
        try:
            db.session.commit()
            flash("User updated successfully")
            return render_template("update.html",
                                   form = form,
                                   name_to_update = name_to_update)
        except:
            flash('Error in updating user')
            return render_template("update.html",
                                   form = form,
                                   name_to_update = name_to_update)
    else:
        return render_template("update.html",
                                   form = form,
                                   name_to_update = name_to_update,
                                   id=id)

# create a form class
class NamerForm(FlaskForm):
    name = StringField("What's your name", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route("/user/add", methods = ['GET', 'POST'])
def add_user():
    name = None
    # if request.method == 'POST':
        # print(request.form)
        # return request.form
    form = UserForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            user = Users(name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        print(name)
        form.name.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
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
    
    
# to create venv set the system permission
# Set-ExecutionPolicy -Scope Process -ExecutionPolicy Default

# initializing db and migrating and upgrading db
# flask db migrate -m "meassage"
# flask db init
# flask db upgrade