# DROP TABLES

songplay_table_drop = ""
user_table_drop = ""
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = ""
time_table_drop = ""

# CREATE TABLES

songplay_table_create = ("""
""")

user_table_create = ("""
""")

song_table_create = ("""CREATE TABLE songs (
song_id text, 
title text, 
artist_id text, 
year int, 
duration int,
PRIMARY KEY (song_id))
""")

artist_table_create = ("""
""")

time_table_create = ("""
""")

# INSERT RECORDS

songplay_table_insert = ("""
""")

user_table_insert = ("""
""")

song_table_insert = ("""

INSERT INTO songs (song_id, title, artist_id, year, duration) VALUES (%s, %s, %s, %s, %s) ON CONFLICT (song_id) DO NOTHING

""")

artist_table_insert = ("""
""")


time_table_insert = ("""
""")

# FIND SONGS

song_select = ("""
""")

# QUERY LISTS

create_table_queries = [song_table_create]

drop_table_queries = [song_table_drop]

# create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
# drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]