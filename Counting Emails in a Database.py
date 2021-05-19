import sqlite3

conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS Counts")
cur.execute("CREATE TABLE Counts (org TEXT, count INTEGER)")

fh = open('mbox.txt')
for lines in fh:
    if not lines.startswith('From: '): continue
    lines = lines.split()
    email = lines[1]
    org = email.split('@')
    org = org[1]

    cur.execute("SELECT count FROM Counts WHERE org = ?", (org,))
    row = cur.fetchone()                                                #fetches one row at a time
    if row is None:
        cur.execute("INSERT INTO Counts (org,count) VALUES (?,1)", (org,))
    else:
        cur.execute("UPDATE Counts SET count = count + 1 WHERE org = ?", (org,))

conn.commit()
for row in cur.execute("SELECT org,count FROM Counts ORDER BY count DESC"):
    print(row[0], row[1])

