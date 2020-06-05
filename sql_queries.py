# DROP TABLES

songplay_table_drop = ""
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""
""")

user_table_create = ("""CREATE TABLE users (
user_id int,
first_name text,
last_name text, 
gender text,
level text,
PRIMARY KEY (user_id))
""")

song_table_create = ("""CREATE TABLE songs (
song_id text, 
title text, 
artist_id text, 
year int, 
duration int,
PRIMARY KEY (song_id))
""")

artist_table_create = ("""CREATE TABLE artists (
artist_id text,
artist_name text,
artist_location text, 
artist_latitude double precision, 
artist_longitude double precision, 
PRIMARY KEY (artist_id))
""")

time_table_create = ("""CREATE TABLE time (
ts timestamp,
hour int,
day int,
week_of_year int,
month int,
year int,
weekday int,
PRIMARY KEY (ts))
""")

# INSERT RECORDS

songplay_table_insert = ("""
""")

user_table_insert = ("""

INSERT INTO users (user_id, first_name, last_name, gender, level) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (user_id) DO NOTHING

""")

song_table_insert = ("""

INSERT INTO songs (song_id, title, artist_id, year, duration) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (song_id) DO NOTHING

""")

artist_table_insert = ("""

INSERT INTO artists (artist_id, artist_name, artist_location, artist_latitude, artist_longitude) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (artist_id) DO NOTHING

""")


time_table_insert = ("""

INSERT INTO time (ts, hour, day, week_of_year, month, year, weekday) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (ts) DO NOTHING

""")

# FIND SONGS

song_select = ("""
""")

# QUERY LISTS
# Only enabling the queries we have completed so far.

create_table_queries = [song_table_create,artist_table_create,time_table_create,user_table_create]

drop_table_queries = [song_table_drop,artist_table_drop,time_table_drop,user_table_drop]

# create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
# drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]