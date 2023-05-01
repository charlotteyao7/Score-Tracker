from flask import *
from database import init_db, db_session
from models import *

app = Flask(__name__)

app.secret_key = "J/2G4+0u2jlwJocEsQ=="

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        return render_template("signin.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        # cannot use instance variables with Flask
        # must add it to this session (saving data on the browser)

        # for now, only let user in if password is 123
        if password == "123":
            session["username"] = username
            return redirect(url_for("matches"))
        else:
            flash("Incorrect username or password", "error")
            # always need to return something
            return render_template("signin.html")
        
@app.route("/signup", methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        return render_template("signin.html")
    else:
        username = request.form["username"]
        password = request.form["password"]
        # cannot use instance variables with Flask
        # must add it to this session (saving data on the browser)

        # for now, only let user in if password is 123
        if password == "123":
            session["username"] = username
            return redirect(url_for("matches"))
        else:
            flash("Incorrect username or password", "error")
            # always need to return something
            return render_template("signin.html")

@app.route("/")
@app.route("/home")
def home():
    # only show the home page if the user is NOT logged in
    if "username" not in session:
        return render_template("home.html")
    else:
        return redirect(url_for("matches"))
    
@app.route("/add")
def add():
    # only show the add page if the user is logged in
    if "username" in session:
        return render_template("add.html")
    else:
        return redirect(url_for("signin"))
    
@app.route("/matches")
def matches():
    # only show the matches page if the user is logged in
    if "username" in session:
        return render_template("matches.html")
    else:
        return redirect(url_for("signin"))

@app.route("/logout")
def logout():
    if "username" in session:
        session.pop("username")
    return redirect(url_for("home"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)