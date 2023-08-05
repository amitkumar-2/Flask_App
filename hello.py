from flask import Flask, render_template

# Create a flask Instance
app = Flask(__name__)

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







if __name__=="__main__":
    app.run(debug=True)