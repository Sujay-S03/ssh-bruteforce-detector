from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

DB_NAME = "attacks.db"


def get_attacks():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM attacks")

    data = cursor.fetchall()

    conn.close()

    return data


@app.route("/")
def dashboard():

    attacks = get_attacks()

    return render_template("dashboard.html", attacks=attacks)


if __name__ == "__main__":
    app.run(debug=True)