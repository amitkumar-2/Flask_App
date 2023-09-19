from flask import Flask, render_template, flash, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
from wtforms.widgets import TextArea
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

# Create a flask Instance
app = Flask(__name__)
# Add database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user_ravi:user_ravi@54.175.148.134/mydb1'
# Secret Key
app.config['SECRET_KEY'] = "This is my super secret key"

# Initialize the database
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# Flask_Login Stuff
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))



# Create Login Form
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(username = form.username.data).first()
        if user:
            # check the hash
            if check_password_hash(user.password_hash, form.password.data):
                login_user(user)
                flash("Login Successfull!!")
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong password try again!")
        else:
            flash("That user doesn't Exits! Try Again...")
            
    return render_template('login.html', form=form)

# Create Logout Page
@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    flash("You Have been Loged out!  Thanks for stopping Bye...")
    return redirect(url_for('login'))

# Create dashboard page
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')



# Create a Blog Post model
class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    slug = db.Column(db.String(255))


# Create a Post Form
class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = StringField("Content", validators=[DataRequired()], widget=TextArea())
    author = StringField("Author", validators=[DataRequired()])
    slug = StringField("Slug", validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route("/posts/delete/<int:id>")
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)

    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        
        # Return a message
        flash("Blog post deleted successfully!")
        
        return redirect(url_for("posts"))
        
        
    except:
        # Return a message
        flash("Woops! there was a problem deleting post, try again...")
        
        return redirect(url_for("posts"))

@app.route("/posts")
def posts():
    # Grab All the post from the Database
    posts = Posts.query.order_by(Posts.date_posted)
    return render_template("posts.html", posts=posts)

@app.route('/posts/<int:id>')
def post(id):
    post = Posts.query.get_or_404(id)
    return  render_template('post.html', post=post)

@app.route("/posts/edit/<int:id>", methods=['POST', 'GET'])
@login_required
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.author = form.author.data
        post.slug = form.slug.data
        post.content = form.content.data
        
        # Update Database
        db.session.add(post)
        db.session.commit()
        flash("Post Has Been Updated!")
        return redirect(url_for('post', id=post.id))
    
    form.title.data = post.title
    form.author.data = post.author
    form.slug.data = post.slug
    form.content.data = post.content

    return render_template('edit_post.html', form=form)


# Add Post Page
@app.route("/add-post", methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    
    if form.validate_on_submit():
        post = Posts(title=form.title.data, content=form.content.data, author=form.author.data, slug=form.slug.data)
        # Clear the form
        form.title.data=""
        form.content.data=""
        form.author.data=""
        form.slug.data=""
        
        # Add post data to database
        db.session.add(post)
        db.session.commit()
        
        # Return a Message
        flash("Blog Post Submitted Successfully!")
    
    # Redirect to the webpage
    return render_template("add_post.html", form=form)



@app.route("/date")
def get_current_data():
    favorite_color = {
        "john": "Pepperoni",
        "Mary": "Cheese",
        "Time": "Mushroom"
    }
    return favorite_color
    # return {"Date": date.today()}


# Create Model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True,)
    username = db.Column(db.String(20), nullable=False, unique=True)
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
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    favorite_color = StringField("Favorite color")
    password_hash = PasswordField("password", validators=[DataRequired(), EqualTo('password_hash2', message='Password Must Match!')])
    password_hash2 = PasswordField("Confirm Password", validators=[DataRequired()])
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
        name_to_update.username = request.form['username']
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
class PasswordForm(FlaskForm):
    email = StringField("What's your email", validators=[DataRequired()])
    password_hash = PasswordField("What's your password", validators=[DataRequired()])
    submit = SubmitField("Submit")

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
            hashed_pw = generate_password_hash(form.password_hash.data, 'sha256')
            user = Users(username=form.username.data, name=form.name.data, email=form.email.data, favorite_color=form.favorite_color.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        name = form.name.data
        print(name)
        form.name.data = ''
        form.username.data = ''
        form.email.data = ''
        form.favorite_color.data = ''
        form.password_hash  = ''
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

# create password test page
@app.route("/test_pw", methods=["GET", "POST"])
def test_pw():
    email = None
    password = None
    pw_to_check = None
    passed = None
    form = PasswordForm()
    
    # Validate form
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        print(form.submit.type)
        form.email.data = ''
        form.password_hash.data = ''
        
        # user details from database
        pw_to_check = Users.query.filter_by(email=email).first()
        
        # check hashed password
        passed = check_password_hash(pw_to_check.password_hash, password)
        
        # flash("From submited successfully!")
        
    return render_template('test_pw.html',
                           email = email,
                           password = password,
                           pw_to_check = pw_to_check,
                           passed = passed,
                           form = form)

# create name page
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