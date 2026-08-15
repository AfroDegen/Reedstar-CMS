import sqlite3
from flask import Flask, request, redirect, render_template_string
from config import DATABASE

app = Flask(__name__)

HTML = """
<!doctype html>
<title>Reedstar CMS</title>
<h1>Reedstar CMS</h1>

<form method="post" action="/new">
  <input name="title" placeholder="Title" required><br><br>
  <textarea name="body" rows="15" cols="60"
            placeholder="Write your content..." required></textarea><br><br>
  <button>Publish</button>
</form>

<hr>

{% for post in posts %}
  <article>
    <h2>{{ post[1] }}</h2>
    <p>{{ post[2] }}</p>
  </article>
{% endfor %}
"""

def db():
    conn = sqlite3.connect(DATABASE)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            body TEXT NOT NULL
        )
    """)
    return conn

@app.get("/")
def home():
    posts = db().execute(
        "SELECT id, title, body FROM posts ORDER BY id DESC"
    ).fetchall()
    return render_template_string(HTML, posts=posts)

@app.post("/new")
def new_post():
    conn = db()
    conn.execute(
        "INSERT INTO posts (title, body) VALUES (?, ?)",
        (request.form["title"], request.form["body"])
    )
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    db().close()
    app.run(host="0.0.0.0", port=8080)
