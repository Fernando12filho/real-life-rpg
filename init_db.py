import sqlite3, os, datetime

DB = "rpg.db"

def init_db():
    with open("schema.sql") as f:
        schema = f.read()
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.executescript(schema)

    # Create character
    c.execute("INSERT OR IGNORE INTO character(id, name) VALUES(1, 'Fernando')")

    # Attributes
    attrs = ["Knowledge", "Career", "Health", "Relationships", "Mindset"]
    for a in attrs:
        c.execute("INSERT OR IGNORE INTO attribute(name, xp, base_level) VALUES(?,0,1)", (a,))

    # Starter quests
    quests = [
        ("Daily Study Ritual", "Study 1h focused", "Knowledge", 10, "side"),
        ("Pomodoro Knight", "4 Pomodoros without distractions", "Knowledge", 20, "side"),
        ("Health Potion", "Go to gym or do physio", "Health", 15, "side"),
        ("Meal Prep Mage", "Prepare meals for the week", "Health", 25, "side"),
        ("Friendship Bond", "Quality time with friends/family", "Relationships", 15, "side"),
        ("Journal of Insight", "Write daily reflection", "Mindset", 10, "side"),
        ("Exam Guardian", "Pass an exam", "Knowledge", 100, "main"),
        ("The Interviewer", "Ace a job interview", "Career", 60, "main"),
        ("The Deadline Beast", "Finish project on time", "Career", 50, "main"),
    ]
    for q in quests:
        c.execute("""INSERT INTO quest(title, description, attr, xp, type, created_at)
                     VALUES(?,?,?,?,?,?)""",
                  (*q, datetime.datetime.now().isoformat()))

    conn.commit()
    conn.close()
    print("✅ Database initialized with starter data.")

if __name__ == "__main__":
    init_db()
