import sqlite3
import xml.etree.ElementTree as ET

conn = sqlite3.connect('tracksdb1.sqlite')
cur = conn.cursor()

cur.executescript("DROP TABLE IF EXISTS Album; DROP TABLE IF EXISTS Artist; DROP TABLE IF EXISTS Genre; DROP TABLE IF EXISTS Track")
cur.execute("CREATE TABLE Artist (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name TEXT UNIQUE)")
cur.execute("CREATE TABLE Album (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, artist_id INTEGER, title TEXT UNIQUE)")
cur.execute("CREATE TABLE Genre (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name TEXT UNIQUE)")
cur.execute("CREATE TABLE Track (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, title TEXT UNIQUE, genre_id INTEGER, album_id INTEGER)")

fh = open('Library.xml')

def lookup(d,key):                                          #done to make navigation seamless in XML file
    found = False
    for child in d:
        if found: return child.text
        if child.tag == 'key' and child.text == key:
            found = True
    return None

xdata = ET.parse(fh)
all = xdata.findall('dict/dict/dict')
for entry in all:
    if lookup(entry, 'Track ID') is None: continue
    name = lookup(entry, 'Name')
    artist = lookup(entry, 'Artist')
    album = lookup(entry, 'Album')
    genre = lookup(entry, 'Genre')

    if name is None or artist is None or album is None or genre is None:
        continue

    cur.execute("INSERT OR IGNORE INTO Artist (name) VALUES (?)", (artist,))                        #INSERT OR IGNORE is used so that UNIQUE condition does not get compromised
    cur.execute("SELECT id FROM Artist WHERE name = ?", (artist,))
    artist_id = cur.fetchone()[0]

    cur.execute("INSERT OR IGNORE INTO Album (title,artist_id) VALUES (?,?)", (album,artist_id))
    cur.execute("SELECT id FROM Album WHERE title = ?", (album,))
    album_id = cur.fetchone()[0]

    cur.execute("INSERT OR IGNORE INTO Genre (name) VALUES(?)", (genre,))
    cur.execute("SELECT id FROM Genre WHERE name = ?", (genre,))
    genre_id = cur.fetchone()[0]

    cur.execute("INSERT OR IGNORE INTO Track (title, album_id, genre_id) VALUES (?,?,?)", (name,album_id,genre_id))

conn.commit()

for row in cur.execute("SELECT Track.title, Artist.name, Album.title, Genre.name FROM Track JOIN Artist JOIN Album JOIN Genre ON Track.genre_id = Genre.id AND Track.album_id = Album.id AND Album.artist_id = Artist.id ORDER by Artist.name LIMIT 3"):
    print(row[0],row[1],row[2],row[3])