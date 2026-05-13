import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    
    user_id = session["user_id"]

    stocks = db.execute(
        """
        SELECT symbol, SUM(shares) AS shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING shares > 0
        """,
        user_id
    )

    portfolio = []
    grand_total = 0

    for stock in stocks:
        quote = lookup(stock["symbol"])

        if quote is None:
            continue

        price = quote["price"]
        total = stock["shares"] * price

        portfolio.append({
            "symbol": stock["symbol"],
            "name": quote["name"],
            "shares": stock["shares"],
            "price": price,
            "total": total
        })

        grand_total += total

    rows = db.execute(
        "SELECT cash FROM users WHERE id = ?",
        user_id
    )

    cash = rows[0]["cash"]
    grand_total += cash

    return render_template(
        "index.html",
        portfolio=portfolio,
        cash=cash,
        grand_total=grand_total
    )

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol", 400)

        if not shares:
            return apology("must provide shares", 400)

        try:
            shares = int(shares)
        except ValueError:
            return apology("shares must be a positive integer", 400)

        if shares <= 0:
            return apology("shares must be a positive integer", 400)

        stock = lookup(symbol)

        if stock is None:
            return apology("invalid symbol", 400)

        user_id = session["user_id"]
        price = stock["price"]
        total = price * shares

        rows = db.execute(
            "SELECT cash FROM users WHERE id = ?",
            user_id
        )

        cash = rows[0]["cash"]

        if cash < total:
            return apology("can't afford", 400)

        db.execute(
            "UPDATE users SET cash = cash - ? WHERE id = ?",
            total,
            user_id
        )

        db.execute(
            """
            INSERT INTO transactions (user_id, symbol, shares, price)
            VALUES (?, ?, ?, ?)
            """,
            user_id,
            stock["symbol"],
            shares,
            price
        )

        return redirect("/")

    return render_template("buy.html")

@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    
    user_id = session["user_id"]

    transactions = db.execute(
        """
        SELECT symbol, shares, price, created_at
        FROM transactions
        WHERE user_id = ?
        ORDER BY created_at DESC
        """,
        user_id
    )

    return render_template("history.html", transactions=transactions)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    
    if request.method == "POST":
        symbol = request.form.get("symbol")

        if not symbol:
            return apology("must provide symbol", 400)

        stock = lookup(symbol)

        if stock is None:
            return apology("invalid symbol", 400)

        return render_template("quoted.html", stock=stock)

    return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username", 400)

        if not password:
            return apology("must provide password", 400)

        if not confirmation:
            return apology("must confirm password", 400)

        if password != confirmation:
            return apology("passwords do not match", 400)

        hash_password = generate_password_hash(password)

        try:
            db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                username,
                hash_password
            )
        except ValueError:
            return apology("username already exists", 400)

        return redirect("/login")

    return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    
    user_id = session["user_id"]

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("must provide symbol", 400)

        if not shares:
            return apology("must provide shares", 400)

        try:
            shares = int(shares)
        except ValueError:
            return apology("shares must be a positive integer", 400)

        if shares <= 0:
            return apology("shares must be a positive integer", 400)

        rows = db.execute(
            """
            SELECT SUM(shares) AS shares
            FROM transactions
            WHERE user_id = ? AND symbol = ?
            GROUP BY symbol
            """,
            user_id,
            symbol
        )

        if len(rows) != 1:
            return apology("you don't own this stock", 400)

        owned_shares = rows[0]["shares"]

        if owned_shares < shares:
            return apology("not enough shares", 400)

        stock = lookup(symbol)

        if stock is None:
            return apology("invalid symbol", 400)

        price = stock["price"]
        total = price * shares

        db.execute(
            "UPDATE users SET cash = cash + ? WHERE id = ?",
            total,
            user_id
        )

        db.execute(
            """
            INSERT INTO transactions (user_id, symbol, shares, price)
            VALUES (?, ?, ?, ?)
            """,
            user_id,
            stock["symbol"],
            -shares,
            price
        )

        return redirect("/")

    symbols = db.execute(
        """
        SELECT symbol, SUM(shares) AS shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
        HAVING shares > 0
        """,
        user_id
    )

    return render_template("sell.html", symbols=symbols)

@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """Allow user to add additional cash"""

    if request.method == "POST":
        amount = request.form.get("amount")

        if not amount:
            return apology("must provide amount", 400)

        try:
            amount = float(amount)
        except ValueError:
            return apology("amount must be a number", 400)

        amount = round(amount, 2)

        if amount <= 0:
            return apology("amount must be positive", 400)

        user_id = session["user_id"]

        db.execute(
            "UPDATE users SET cash = cash + ? WHERE id = ?",
            amount,
            user_id
        )

        return redirect("/")

    return render_template("add_cash.html")
    