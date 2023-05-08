from flask import *
from database import init_db, db_session
from models import *

app = Flask(__name__)

app.secret_key = "J/2G4+0u2jlwJocEsQ=="

@app.route("/signin", methods=["GET", "POST"])
def signin():
    if request.method == "GET":
        return render_template("signin.html")
    elif request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        # check if user exists
        existing = db_session.query(User.username).all()
        existing = [r for (r,) in existing]
        if u not in existing:
            flash("Incorrect username or password", "error")
            # always need to return something
            return render_template("signin.html")

        # check if password matches the username
        this_user_password = db_session.query(User.password).where(User.username == u).first()[0]
        if this_user_password == p:
            session["username"] = u
            return redirect(url_for("matches"))
        else:
            flash("Incorrect username or password", "error")
            # always need to return something
            return render_template("signin.html")
        
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    elif request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        p2 = request.form["password2"]

        # find all existing usernames
        existing = db_session.query(User.username).all()
        # list comprehension to get rid of the tuples
        existing = [r for (r,) in existing]
        
        # check if username is already taken
        if u in existing:
            flash("Username is already taken", "error")
            return render_template("signup.html")
        elif p != p2:
            flash("Passwords don't match", "error")
            return render_template("signup.html")
        else:
            session["username"] = u
            # add a new user to the database
            new_user = User(username=u, password=p)
            db_session.add(new_user)
            db_session.commit()
            return redirect(url_for("matches"))
        
@app.route("/")
@app.route("/home")
def home():
    # only show the home page if the user is NOT logged in
    if "username" not in session:
        return render_template("home.html")
    else:
        return redirect(url_for("matches"))
    
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "GET":
        # only show the add page if the user is logged in
        if "username" in session:
            return render_template("add.html")
        else:
            return redirect(url_for("signin"))
    elif request.method == "POST":
        # add a new match to the database
        d = request.form["date"]
        o = request.form["opponent"]
        s = request.form["score"]
        n = request.form["notes"]
        new_match = Match(date=d, opponent=o, score=s, notes=n, user_id=session["username"])
        db_session.add(new_match)
        db_session.commit()
        return redirect(url_for("matches"))
    
    
@app.route("/matches", methods=["GET", "POST"])
def matches():
    if request.method == "GET":
        # only show the matches page if the user is logged in
        if "username" in session:
            this_user = db_session.query(User).where(User.username == session["username"]).first()
            all_matches = this_user.matches
            return render_template("matches.html", user=session["username"], matches=all_matches)
        else:
            return redirect(url_for("signin"))
    elif request.method == "POST":
        # delete the match from the database
        match_id = request.form["match"]
        match_to_delete = db_session.query(Match).where(Match.id == match_id).first()
        db_session.delete(match_to_delete)
        db_session.commit()
        return redirect(url_for("matches"))

@app.route("/logout")
def logout():
    if "username" in session:
        session.pop("username")
    return redirect(url_for("home"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)