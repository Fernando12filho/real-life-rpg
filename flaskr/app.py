from flask import Flask, g, render_template, request, redirect, url_for
import sqlite3, datetime, os

DB = "rpg.db"
app = Flask(__name__)

def get_db():
    db = getattr(g, "_db", None)
    if db is None:
        db = sqlite3.connect(DB)
        db.row_factory = sqlite3.Row
        g._db = db
    return db

@app.teardown_appcontext
def close_db(exc):
    db = getattr(g, "_db", None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    db = get_db()
    character = db.execute("SELECT * FROM character LIMIT 1").fetchone()
    if not character:
        return render_template("setup.html")
    
    attrs = db.execute("SELECT * FROM attribute").fetchall()
    quests = db.execute("SELECT * FROM quest WHERE status='open'").fetchall()
    return render_template("index.html", attrs=attrs, quests=quests)

@app.route("/add", methods=["GET","POST"])
def add_quest():
    if request.method == "POST":
        title = request.form["title"]
        desc = request.form["description"]
        attr = request.form["attr"]
        xp = int(request.form["xp"])
        qtype = request.form.get("type","side")
        db = get_db()
        db.execute("""INSERT INTO quest(title, description, attr, xp, type, created_at)
                      VALUES(?,?,?,?,?,?)""",
                   (title, desc, attr, xp, qtype, datetime.datetime.now().isoformat()))
        db.commit()
        return redirect(url_for("index"))
    attrs = get_db().execute("SELECT name FROM attribute").fetchall()
    return render_template("add_quest.html", attrs=attrs)

@app.route("/complete/<int:qid>")
def complete(qid):
    db = get_db()
    q = db.execute("SELECT * FROM quest WHERE id=?", (qid,)).fetchone()
    if q and q["status"] == "open":
        db.execute("UPDATE quest SET status='done' WHERE id=?", (qid,))
        db.execute("UPDATE attribute SET xp = xp + ? WHERE name=?", (q["xp"], q["attr"]))
        db.commit()
    return redirect(url_for("index"))

@app.route("/journal", methods=["GET","POST"])
def journal():
    db = get_db()
    if request.method == "POST":
        note = request.form["note"]
        db.execute("INSERT INTO journal(note, created_at) VALUES(?,?)",
                   (note, datetime.datetime.now().isoformat()))
        db.commit()
        return redirect(url_for("journal"))
    entries = db.execute("SELECT * FROM journal ORDER BY created_at DESC").fetchall()
    return render_template("journal.html", entries=entries)

if __name__ == "__main__":
    if not os.path.exists(DB):
        import init_db
        init_db.init_db()
    app.run(debug=True)
