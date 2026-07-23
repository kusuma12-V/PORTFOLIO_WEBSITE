from flask import Flask, render_template, request
import sqlite3
from models import create_database

app = Flask(__name__,
            template_folder="templates",
            static_folder="static")

create_database()
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

conn = get_db_connection()

conn.execute("""
CREATE TABLE IF NOT EXISTS contacts(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    subject TEXT NOT NULL,
    message TEXT NOT NULL
)
""")

conn.commit()
conn.close()

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/projects")
def projects():
    return render_template("projects.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        conn = sqlite3.connect("portfolio.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO contact(name,email,message) VALUES(?,?,?)",
            (name, email, message)
        )

        conn.commit()
        conn.close()

        return "<h2>Message Sent Successfully!</h2>"

    return render_template("contact.html")

@app.route("/admin")
def admin():

    conn = sqlite3.connect("portfolio.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM contact")

    messages = cursor.fetchall()

    conn.close()

    return render_template("admin.html",
                           messages=messages)


if __name__ == "_main_":
    app.run(debug=True)

