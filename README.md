# Introduction

This ETL project looks to collect and present user activity information for a fictional music streaming service called Sparkify. To do this, data is gathered from song information and application `.json` log files (which were generated from the [Million Song Dataset](http://millionsongdataset.com/) and from [eventsim](https://github.com/Interana/eventsim) respectively and given to us). The data in these datasets are first loaded into [pandas](https://pandas.pydata.org/) dataframes so they can be filtered, before being inserted into a Postgres SQL database where they are then transformed to create a final `songplays` table that is optimized for queries on the song playback habits of users. 

# Schema
Given that the primary purpose of this project is to show _what songs users are listening to_, the `songplays` table is our fact table, with several other dimension tables feeding into it. Based on the relative simplicity of the relationships in this project, we have opted to organise these tables in a straightforward star schema.

```
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
```


## Normalization

### Postgres UPSERT
This schema is in 2nd Normal Form. However, the source data are in denormalized datasets (log files). Thus, the `etl.py` script uses [Postgres' _UPSERT_ function](https://wiki.postgresql.org/wiki/UPSERT) (`ON CONFLICT (user_id) DO UPDATE SET`) to only UPDATE (and **not** INSERT) rows with newer information if the row being inserted matches each dimension table's primary key. 

The rationale behind this is that log and song file data that are read later via the `process_data` function are newer and therefore more accurate. In order to make sure that we're reading files in ascending order, based on their modified date, we've added this line to the `process_data` function:

`files.sort(key=lambda x: os.path.getmtime(x))`

### Python assert()

Also, since we're reading `.json` files via pandas in `etl.py`, we we use Python's [assert statement](https://www.programiz.com/python-programming/assert-statement) to check types (lists, dataframes) throughout the ETL process. This will make it easier to debug data quality issues if they ever arise.

# ETL Scripts

## Primary
There are two primary scripts that will need to be run for this project, in the order that they need to be run.

1) `create_tables.py`  - This script drops any existing tables in the `sparkifydb` and creates the necesary tables for our `etl.py` script to run. `etl.py` will not execute correctly if you first do not run this script.

2) `etl.py` - This is the main ETL script for the project. It reads the data from the `data/` folder and inserts it into the `sparkifydb` database.

## Secondary
3) `sql_queries.py` - This is a module that both `create_tables.py` and `etly.py` load to run the SQL queries needed to both set up the tables required by this project, and then insert data into them. This script is not executed directly.


# Example Queries 

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


#### What are the most popular user agents among users who have played songs?

`select user_agent, count(songplay_id) from songplays group by user_agent order by count(songplay_id) desc;`

```
                                                                 user_agent                                                                  | count 
---------------------------------------------------------------------------------------------------------------------------------------------+-------
 Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0                                                                    |     4
 "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36"                             |     4
 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36"                  |     4
 Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0                                                                           |     3
 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2"                     |     3
 "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36"                                  |     2
 "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/36.0.1985.125 Chrome/36.0.1985.125 Safari/537.36"   |     2
 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"                  |     1
 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36"                   |     1
 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.77.4 (KHTML, like Gecko) Version/7.0.5 Safari/537.77.4"                     |     1
 "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53" |     1
 Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:31.0) Gecko/20100101 Firefox/31.0                                                           |     1
 Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0                                                                    |     1
 Mozilla/5.0 (Windows NT 6.1; rv:31.0) Gecko/20100101 Firefox/31.0                                                                           |     1
 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"                             |     1
```

#### What are the most popular browsaers among users who have played songs?





#### What are the most popular operating systems among users who have played songs?

```
select 
sum(case when user_agent like '%Windows%' then 1 else 0 end) as windows_sum, 
sum(case when user_agent like '%Linux%' then 1 else 0 end) as linux_sum, 
sum(case when user_agent like '%Mac%' then 1 else 0 end) as mac_sum, 
sum(case when user_agent like '%iPhone%' then 1 else 0 end) as iphone_sum, 
sum(case when user_agent like '%Android%' then 1 else 0 end) as anrdoid_sum 
from songplays;
```

```
 windows_sum | linux_sum | mac_sum | iphone_sum | anrdoid_sum 
-------------+-----------+---------+------------+-------------
          14 |         4 |      12 |          1 |           0
```
