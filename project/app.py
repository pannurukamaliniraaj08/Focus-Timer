import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from datetime import datetime, timedelta
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "study.db")
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL(f"sqlite:///{db_path}")
users_in_db = db.execute("SELECT * FROM users")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Require that a user input a username, implemented as a text field whose name is username.
    # Render an apology if the user’s input is blank or the username already exists.
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not request.form.get("username"):
            return apology("No Username entered", 400)
        if not request.form.get("password"):
            return apology("No password entered", 400)
        if not request.form.get("confirmation"):
            return apology("Password not Re-Entered", 400)
        if password != confirmation:
            return apology("passwords do not match", 400)

        existing = db.execute("SELECT id FROM users WHERE username = ?", username)
        if len(existing) > 0:
            return apology("username already exists", 400)

        # Require that a user input a password, implemented as a text field whose name is password, and then that same password again, implemented as a text field whose name is confirmation.
        # Render an apology if either input is blank or the passwords do not match.

        # Submit the user’s input via POST to /register.
        hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)
        return redirect("/login")

        # INSERT the new user into users, storing a hash of the user’s password, not the password itself.
        # Hash the user’s password with generate_password_hash Odds are you’ll want to create a new template (e.g., register.html) that’s quite similar to login.html
    else:
        return render_template("register.html")
    # Once you’ve implemented register correctly, you should be able to register for an account and log in (since login and logout already work)!
    # And you should be able to see your rows via phpLiteAdmin or sqlite3.

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")

@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    coins = db.execute("SELECT coins FROM users WHERE id = ?",user_id)
    coin_val = coins[0].get("coins")
    return render_template("index.html", coins=coin_val)

@app.route("/light")
@login_required
def light():
    user_id = session["user_id"]
    coins = db.execute("SELECT coins FROM users WHERE id = ?",user_id)
    coin_val = coins[0].get("coins")
    return render_template("light.html", coins=coin_val )

@app.route("/dark")
@login_required
def dark():
    user_id = session["user_id"]
    coins = db.execute("SELECT coins FROM users WHERE id = ?",user_id)
    coin_val = coins[0].get("coins")
    return render_template("dark.html", coins=coin_val )

@app.route("/pastel")
@login_required
def pastel():
    user_id = session["user_id"]
    coins = db.execute("SELECT coins FROM users WHERE id = ?",user_id)
    coin_val = coins[0].get("coins")
    purchases = db.execute("SELECT theme FROM purchases WHERE user_id = ?", user_id)
    for purchase in purchases:
        if purchase.get("theme") == "pastel":
            return render_template("pastel.html", coins=coin_val )
    return redirect("/")

@app.route("/forest")
@login_required
def forest():
    user_id = session["user_id"]
    coins = db.execute("SELECT coins FROM users WHERE id = ?",user_id)
    coin_val = coins[0].get("coins")
    purchases = db.execute("SELECT theme FROM purchases WHERE user_id = ?", user_id)
    for purchase in purchases:
        if purchase.get("theme") == "forest":
            return render_template("forest.html", coins=coin_val )
    return redirect("/")

@app.route("/cyberpunk")
@login_required
def cyberpunk():
    user_id = session["user_id"]
    coins = db.execute("SELECT coins FROM users WHERE id = ?",user_id)
    coin_val = coins[0].get("coins")
    purchases = db.execute("SELECT theme FROM purchases WHERE user_id = ?", user_id)
    for purchase in purchases:
        if purchase.get("theme") == "cyberpunk":
            return render_template("cyberpunk.html", coins=coin_val )
    return redirect("/")

@app.route("/expresso")
@login_required
def expresso():
    user_id = session["user_id"]
    coins = db.execute("SELECT coins FROM users WHERE id = ?",user_id)
    coin_val = coins[0].get("coins")
    purchases = db.execute("SELECT theme FROM purchases WHERE user_id = ?", user_id)
    for purchase in purchases:
        if purchase.get("theme") == "expresso":
            return render_template("expresso.html", coins=coin_val )
    return redirect("/buy/expresso")

@app.route("/get-daily-stats")
@login_required
def get_daily_stats():
    user_id = session["user_id"]

    db_rows = db.execute("SELECT DATE(created_at) AS date, SUM(duration_minutes) AS total_minutes FROM study_sessions WHERE user_id = ? GROUP BY DATE(created_at)", user_id)

    logged_data = {row["date"]: row["total_minutes"] for row in db_rows}

    full_stats = []
    today = datetime.now().date()
    for i in range(22, -1, -1):  # Past 21 days
        day = today - timedelta(days=i)
        day_str = day.strftime("%Y-%m-%d")
        total_minutes = logged_data.get(day_str, 0)
        total_hours = round(total_minutes / 60, 2)
        full_stats.append({
            "date": day_str,
            "minutes": total_minutes,
            "hours": total_hours
        })
    return jsonify(full_stats)

@app.route("/get-seconds", methods=["POST"])
@login_required
def get_seconds():
    user_id = session["user_id"]
    data = request.get_json() or {}
    total_seconds = data.get("totalSeconds")
    try:
        total_seconds= float(total_seconds)
        if total_seconds <= 0:
            return jsonify({"success": False, "error": "No duration recorded"}), 400
    except(ValueError, TypeError):
        return jsonify({"success": False, "error": "Invalid totalSeconds"}), 400

    duration_minutes = round((total_seconds/60), 2)
    if duration_minutes is None:
        return jsonify({"success": False, "error": "Missing name"}), 400

    db.execute("INSERT INTO study_sessions (user_id, duration_minutes) VALUES (?, ?)", user_id, duration_minutes)
    sessions = db.execute("SELECT duration_minutes FROM study_sessions WHERE user_id = ?", user_id)
    total_minutes = 0
    for row in sessions:
        total_minutes += row["duration_minutes"]

    coins = (total_minutes //60) *10
    db.execute("UPDATE users SET coins = ? WHERE id = ?", coins, user_id)

    return jsonify({"success": True, "message": "User saved!"})

@app.route("/buy/<theme>", methods=["POST"])
@login_required
def buy(theme):
    prices = {
    "pastel": 100,
    "forest": 500,
    "cyberpunk": 600,
    "expresso": 1500
    }
    user_id = session["user_id"]
    coins = db.execute("SELECT coins FROM users WHERE id = ?",user_id)
    coin_val = coins[0].get("coins")
    purchases = db.execute("SELECT theme FROM purchases WHERE user_id = ?", user_id)

    price = prices.get(theme)
    if price is None:
        return jsonify({"success": False, "error": "Invalid item"}), 400
    for purchase in purchases:
        if theme == purchase.get("theme"):
            return jsonify({"success": True, "message": "Purchase exists!"}), 200
    if coin_val >= price:
        db.execute("INSERT INTO purchases (theme, user_id) VALUES(?, ?)", theme, user_id)
        coin_val -= price
        db.execute("UPDATE users SET coins = ? WHERE id = ?", coin_val, user_id)
        return jsonify({"success": True, "message": "Purchase complete!"}), 200
    else:
        return jsonify({"success": False, "error": "Not enough coins for that 🪙"}), 400




