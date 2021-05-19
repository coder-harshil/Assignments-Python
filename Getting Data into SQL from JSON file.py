import sqlite3
import json

conn = sqlite3.connect('rosterdb.sqlite')
cur = conn.cursor()

cur.executescript("DROP TABLE IF EXISTS Member; DROP TABLE IF EXISTS User; DROP TABLE IF EXISTS Course")
cur.execute("CREATE TABLE User (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name TEXT UNIQUE)")
cur.execute("CREATE TABLE Member (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, user_id INTEGER, course_id INTEGER, role INTEGER)")
cur.execute("CREATE TABLE Course (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, title TEXT UNIQUE)")

with open("roster_data.json") as f:
    js = json.load(f)

for lists in js:
    name = lists[0]
    course = lists[1]
    role = lists[2]

    if name is None or course is None or role is None:
        continue

    cur.execute("INSERT OR IGNORE INTO User (name) VALUES (?)", (name,))
    cur.execute("SELECT id from User WHERE name = ?", (name,))
    user_id = cur.fetchone()[0]

    cur.execute("INSERT OR IGNORE INTO Course (title) VALUES (?)", (course,))
    cur.execute("SELECT id FROM Course WHERE title = ?", (course,))
    course_id = cur.fetchone()[0]

    cur.execute("INSERT OR IGNORE INTO Member (user_id, course_id, role) VALUES (?,?,?)", (user_id,course_id,role))

conn.commit()
for row in cur.execute("SELECT User.name, Course.title, Member.role FROM User JOIN Member JOIN Course ON Member.user_id = User.id AND Member.course_id = Course.id ORDER BY User.name DESC, Course.title DESC, Member.role DESC LIMIT 2"):
    print(row[0], row[1], row[2])

