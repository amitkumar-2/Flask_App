from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Create a flask Instance
app = Flask(__name__)
app.config['SECRET_KEY'] = "This is my super secret key"

# create a form class
class NamerForm(FlaskForm):
    name = StringField("What's your name", validators=[DataRequired()])
    submit = SubmitField("Submit")

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
    app.run(debug=True)