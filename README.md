# Introduction

This ETL project looks to collect and present user activity information for a fictional music streaming service called Sparkify. To do this, data is gathered from song information and application log files, both stored in `.json` format, and then loaded into a Postgres SQL database where it can then be transformed to create a final `songplays` table. 

# Schema
Given that the primary purpose of this project is to show _what songs users are listening to_, the `songplays` table is our fact table, with several other dimension tables feeding into it. Based on the relative simplicity of the relationships in this project, we have opted to organise these tables in a straightforward star schema.

```
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
```

Given the denormalized data sources (log files) that this project is drawing information from here, the `etl.py` script uses Postgres' _UPSERT_ function (`ON CONFLICT (user_id) DO UPDATE SET `) to update rows with newer information if the new row being inserted matches each dimension table's primary key. The rationale behind this is that log and song file data that are read later via the `process_data` function are newer and therefore more accurate.

## Example Queries 

#### Which hour of the day are users starting to play the most songs?

`select hour, count(songplay_id) from songplays inner join time on songplays.start_time = time.start_time group by hour;`

```
 hour | count 
------+-------
   19 |     2
   21 |     1
   20 |     1
   22 |     3
   23 |    23
(5 rows)
```

#### Which users have started playing the most songs?

`select user_id, count(songplay_id) from songplays group by user_id;`

```
 user_id | count 
---------+-------
      52 |     1
      70 |     1
      80 |     3
     101 |     1
      97 |     1
      11 |     1
      44 |     1
      42 |     1
      15 |     1
      26 |     1
      95 |     1
       3 |     1
      37 |     1
       5 |     1
      54 |     1
      83 |     1
      35 |     1
       6 |     1
      86 |     1
      89 |     1
      12 |     1
      24 |     1
      25 |     2
      49 |     3
      47 |     1
(25 rows)
```