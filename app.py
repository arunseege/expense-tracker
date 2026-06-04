from flask import Flask
from database.db import init_db, seed_db

app = Flask(__name__)

with app.app_context():
    init_db()
    seed_db()


@app.route("/")
def index():
    return {"status": "ok", "message": "Spendly API is running"}


if __name__ == "__main__":
    app.run(debug=True)
