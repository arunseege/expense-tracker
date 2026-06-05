import os
import sqlite3
from flask import Flask, flash, redirect, render_template, request, session, url_for
from database.db import init_db, seed_db, create_user, verify_user, get_expenses

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-in-prod")

with app.app_context():
    init_db()
    seed_db()


def login_required():
    if "user_id" not in session:
        flash("Please log in to continue.", "error")
        return redirect(url_for("login"))
    return None


@app.route("/")
def index():
    guard = login_required()
    if guard:
        return guard
    expenses = get_expenses(session["user_id"])
    total = sum(e["amount"] for e in expenses)
    top_category = None
    category_totals = {}
    highest_cat = lowest_cat = middle_cat = None
    if expenses:
        from collections import Counter
        top_category = Counter(e["category"] for e in expenses).most_common(1)[0][0]
        for e in expenses:
            category_totals[e["category"]] = round(
                category_totals.get(e["category"], 0) + e["amount"], 2
            )
        sorted_cats = sorted(category_totals.items(), key=lambda x: x[1])
        lowest_cat  = sorted_cats[0][0]
        highest_cat = sorted_cats[-1][0]
        if len(sorted_cats) >= 3:
            middle_cat = sorted_cats[len(sorted_cats) // 2][0]
    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        top_category=top_category,
        category_totals=category_totals,
        highest_cat=highest_cat,
        lowest_cat=lowest_cat,
        middle_cat=middle_cat,
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if "user_id" in session:
        return redirect(url_for("index"))
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()

        if not name or not email or not password or not confirm_password:
            flash("All fields are required.", "error")
            return render_template("register.html")

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return render_template("register.html")

        try:
            create_user(name, email, password)
        except sqlite3.IntegrityError:
            flash("An account with that email already exists.", "error")
            return render_template("register.html")

        flash("Account created! Please log in.", "success")
        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("index"))
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()

        if not email or not password:
            flash("Email and password are required.", "error")
            return render_template("login.html")

        user = verify_user(email, password)
        if user is None:
            flash("Invalid email or password.", "error")
            return render_template("login.html")

        session["user_id"] = user["id"]
        session["user_name"] = user["name"]
        return redirect("/")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect("/login")


if __name__ == "__main__":
    app.run(debug=True)
