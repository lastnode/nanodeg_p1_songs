"""
This module is loaded by `create_tables.py` and `etl.py`
as it contains the SQL queries needed to create the tables
necessary for this project, and insert data into them.
"""

# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplay"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES
# Using Postgres' REFERENCES -
# https://www.postgresql.org/docs/8.3/tutorial-fk.html

songplay_table_create = ("""CREATE TABLE songplays (
songplay_id serial,
start_time timestamp references time(start_time),
user_id int references users(user_id),
level text,
song_id text references songs(song_id),
artist_id text references artists(artist_id),
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
name text,
location text,
latitude double precision,
longitude double precision,
PRIMARY KEY (artist_id))
""")

time_table_create = ("""CREATE TABLE time (
start_time timestamp,
hour int,
day int,
week_of_year int,
month int,
year int,
weekday int,
PRIMARY KEY (start_time))
""")

# INSERT RECORDS

songplay_table_insert = ("""

INSERT INTO songplays
(start_time, user_id, level, song_id, artist_id,
 session_id,location, user_agent)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (songplay_id) DO UPDATE SET
start_time=EXCLUDED.start_time,
user_id=EXCLUDED.user_id,
level=EXCLUDED.level,
song_id=EXCLUDED.song_id,
artist_id = EXCLUDED.artist_id,
session_id=EXCLUDED.session_id,
location=EXCLUDED.location,
user_agent=EXCLUDED.user_agent

""")

user_table_insert = ("""

INSERT INTO users
(user_id, first_name, last_name, gender, level)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (user_id) DO UPDATE SET
first_name=EXCLUDED.first_name,
last_name=EXCLUDED.last_name,
gender=EXCLUDED.gender,
level=EXCLUDED.level

""")

song_table_insert = ("""

INSERT INTO songs
(song_id, title, artist_id, year, duration)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (song_id) DO UPDATE SET
title=EXCLUDED.title,
artist_id=EXCLUDED.artist_id,
year=EXCLUDED.year,
duration=EXCLUDED.duration

""")

artist_table_insert = ("""

INSERT INTO artists
(artist_id, name, location, latitude, longitude)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT (artist_id) DO UPDATE SET
artist_id=EXCLUDED.artist_id,
name=EXCLUDED.name,
location=EXCLUDED.location,
latitude=EXCLUDED.latitude,
longitude=EXCLUDED.longitude

""")


time_table_insert = ("""

INSERT INTO time
(start_time, hour, day, week_of_year, month, year, weekday)
VALUES (%s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (start_time) DO UPDATE SET
hour=EXCLUDED.hour,
day=EXCLUDED.day,
week_of_year=EXCLUDED.week_of_year,
month=EXCLUDED.month,
year=EXCLUDED.year,
weekday=EXCLUDED.weekday

""")

# FIND SONGS

song_select_artist_song_ids = ("""

SELECT songs.song_id, artists.artist_id
FROM songs
JOIN artists on songs.artist_id = artists.artist_id
WHERE songs.title = %s and
artists.name = %s and
songs.duration = %s
""")

# QUERY LISTS

create_table_queries = [user_table_create, song_table_create,
                        artist_table_create, time_table_create,
                        songplay_table_create]
drop_table_queries = [user_table_drop, song_table_drop, artist_table_drop,
                      time_table_drop, songplay_table_drop]
