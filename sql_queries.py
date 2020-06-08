# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplay"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""CREATE TABLE songplays (
songplay_id serial,
ts timestamp,
user_id int,
level text,
song_id text, 
artist_id text,
session_id int,
location text,
user_agent text,
PRIMARY KEY (songplay_id))
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
duration double precision,
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

INSERT INTO songplays (ts, user_id, level, song_id, artist_id, session_id, location, user_agent) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (songplay_id) DO UPDATE SET ts=EXCLUDED.ts, user_id=EXCLUDED.user_id, level=EXCLUDED.level, song_id=EXCLUDED.song_id, artist_id = EXCLUDED.artist_id, session_id=EXCLUDED.session_id, location=EXCLUDED.location, user_agent=EXCLUDED.user_agent

""")

user_table_insert = ("""

INSERT INTO users (user_id, first_name, last_name, gender, level) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (user_id) DO UPDATE SET first_name=EXCLUDED.first_name, last_name=EXCLUDED.last_name, gender=EXCLUDED.gender, level=EXCLUDED.level 

""")

song_table_insert = ("""

INSERT INTO songs (song_id, title, artist_id, year, duration) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (song_id) DO UPDATE SET title=EXCLUDED.title,  artist_id=EXCLUDED.artist_id, year=EXCLUDED.year, duration=EXCLUDED.duration
""")

artist_table_insert = ("""

INSERT INTO artists (artist_id, artist_name, artist_location, artist_latitude, artist_longitude) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (artist_id) DO UPDATE SET artist_id=EXCLUDED.artist_id, artist_name=EXCLUDED.artist_name, artist_location=EXCLUDED.artist_location, artist_latitude=EXCLUDED.artist_latitude, artist_longitude=EXCLUDED.artist_longitude

""")


time_table_insert = ("""

INSERT INTO time (ts, hour, day, week_of_year, month, year, weekday) VALUES (%s, %s, %s, %s, %s, %s, %s) ON CONFLICT (ts) DO UPDATE SET hour=EXCLUDED.hour, day=EXCLUDED.day, week_of_year=EXCLUDED.week_of_year, month=EXCLUDED.month, year=EXCLUDED.year, weekday=EXCLUDED.weekday 

""")

# FIND SONGS

song_select_artist_song_ids = ("""

SELECT songs.song_id, artists.artist_id
FROM songs
JOIN artists on songs.artist_id = artists.artist_id
WHERE songs.title = %s and
			artists.artist_name = %s and
			songs.duration = %s
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]