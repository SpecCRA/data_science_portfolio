#!/usr/bin/env python

"""
This file writes my csv files into database files
"""

import sqlite3
import csv
from pprint import pprint

sqlite_file = "map_data.db"
conn = sqlite3.connect(sqlite_file)
cur = conn.cursor()

def add_table(add_table_query):
    cur.execute(add_table_query)
    conn.commit()

# Each of these are the table creation queries from data_wrangling_schema.sql
add_nodes = "CREATE TABLE nodes (id INTEGER PRIMARY KEY NOT NULL,lat REAL,lon REAL,user TEXT,uid INTEGER,version INTEGER,changeset INTEGER,timestamp TEXT)"

add_nodes_tags = "CREATE TABLE nodes_tags (id INTEGER,key TEXT,value TEXT,type TEXT,FOREIGN KEY (id) REFERENCES nodes(id))"

add_ways = "CREATE TABLE ways (id INTEGER PRIMARY KEY NOT NULL,user TEXT,uid INTEGER,version TEXT,changeset INTEGER,timestamp TEXT)"

add_ways_tags = "CREATE TABLE ways_tags (id INTEGER NOT NULL,key TEXT NOT NULL,value TEXT NOT NULL,type TEXT,FOREIGN KEY (id) REFERENCES ways(id))"

add_ways_nodes = "CREATE TABLE ways_nodes (id INTEGER NOT NULL,node_id INTEGER NOT NULL,position INTEGER NOT NULL,FOREIGN KEY (id) REFERENCES ways(id),FOREIGN KEY (node_id) REFERENCES nodes(id))"

# drop tables I want to write if they exist right now
cur.execute("""DROP TABLE IF EXISTS nodes_tags""")
cur.execute("""DROP TABLE IF EXISTS nodes""")
cur.execute("""DROP TABLE IF EXISTS ways""")
cur.execute("""DROP TABLE IF EXISTS ways_tags""")
cur.execute("""DROP TABLE IF EXISTS ways_nodes""")
conn.commit()

# Add all the tables to the db file!
add_table(add_nodes)
add_table(add_nodes_tags)
add_table(add_ways)
add_table(add_ways_tags)
add_table(add_ways_nodes)

# Read each csv file into a dictionary and format the data into a list of tuples
with open("nodes.csv", "rb") as fin:
    dr = csv.DictReader(fin)
    nodes_db = [(i['id'], i['lat'], i['lon'], i['user'].decode("utf-8"), i['uid'], i['version'], i['changeset'], i['timestamp']) for i in dr]

with open ("nodes_tags.csv", "rb") as fin:
    dr = csv.DictReader(fin)
    nodes_tags_db = [(i['id'], i['key'], i['value'].decode("utf-8"), i['type']) for i in dr]

with open("ways.csv", "rb") as fin:
    dr = csv.DictReader(fin)
    ways_db = [(i['id'], i['user'].decode("utf-8"), i['uid'], i['version'], i['changeset']) for i in dr]

with open("ways_tags.csv", "rb") as fin:
    dr = csv.DictReader(fin)
    ways_tags_db = [(i['id'], i['key'], i['value'].decode("utf-8"), i['type']) for i in dr]

with open("ways_nodes.csv", "rb") as fin:
    dr = csv.DictReader(fin)
    ways_nodes_db = [(i['id'], i['node_id'], i['position']) for i in dr]

# Insert each value into their respective tables
cur.executemany("INSERT INTO nodes(id, lat, lon, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ? ,?, ?)", nodes_db)
cur.executemany("INSERT INTO nodes_tags(id, key, value, type) VALUES (?, ?, ?, ?);", nodes_tags_db)
cur.executemany("INSERT INTO ways(id, user, uid, version, changeset) VALUES (?, ?, ?, ?, ?);", ways_db)
cur.executemany("INSERT INTO ways_tags(id, key, value, type) VALUES (?, ?, ?, ?)", ways_tags_db)
cur.executemany("INSERT INTO ways_nodes(id, node_id, position) VALUES (?, ?, ?)", ways_nodes_db)
conn.commit()

#cur.execute("SELECT * FROM nodes_tags")
#all_rows = cur.fetchall()
#print ('1):')
#pprint (all_rows)

conn.close()

