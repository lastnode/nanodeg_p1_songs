# Introduction

This ETL project looks to collect and present user activity information for a fictional music streaming service called Sparkify. To do this, data is gathered from song information and application `.json` log files (which were generated from the [Million Song Dataset](http://millionsongdataset.com/) and from [eventsim](https://github.com/Interana/eventsim) respectively and given to us). The data in these datasets are first loaded into [pandas](https://pandas.pydata.org/) dataframes so they can be filtered, before being inserted into a Postgres SQL database where they are then transformed to create a final `songplays` table that is optimized for queries on the song playback habits of users. 

# Files
```
- data/ -- the folder with song information and user log information, all in .json format
- README.md -- this file
- create_tables.py -- creates tables necessary for ETL script
- etl.py - the main ETL script that reads the .json files and inserts them into the database
- sql_queries.py - a module that create_tables.py and etl.py load to run the SQL queries
- etl.ipynb -- the preliminary Jupyter notebook that was used to develop etl.py
- test.ipynb -- a Jupyter notebook that can be run to test the data in the db
```

# ETL Scripts

## Primary
There are two primary scripts that will need to be run for this project, in the order that they need to be run.

1) `create_tables.py`  - This script drops any existing tables in the `sparkifydb` and creates the necesary tables for our `etl.py` script to run. `etl.py` will not execute correctly if you first do not run this script.

2) `etl.py` - This is the main ETL script for the project. It reads the data from the `data/` folder and inserts it into the `sparkifydb` database.

## Secondary
3) `sql_queries.py` - This is a module that both `create_tables.py` and `etl.py` load to run the SQL queries needed to both set up the tables required by this project, and then insert data into them. This script is not executed directly.

4) `test.ipynb` - This is a [Jupyter](https://jupyter.org/) notebook that will test that all the databases have been created and that data has been correctly inserted into them.

# Database Schema
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


## Normalization and Error-checking

### Postgres UPSERT
This schema is in 2nd Normal Form. However, the source data are in denormalized datasets (log files). Thus, the `etl.py` script uses [Postgres' _UPSERT_ function](https://wiki.postgresql.org/wiki/UPSERT) (`ON CONFLICT (user_id) DO UPDATE SET`) to only UPDATE (and **not** INSERT) rows with newer information if the row being inserted matches each dimension table's primary key. 

The rationale behind this is that log and song file data that are read later via the `process_data` function are newer and therefore more accurate. Thus, if we find duplicate song information or log entries in them, we should update the relevant row in the database. In order to make sure that we're reading files in ascending order, based on their modified date, we've added this line to the `process_data` function:

`files.sort(key=lambda x: os.path.getmtime(x))`

### Python assert()

Also, since we're reading `.json` files via pandas in `etl.py`, we we use Python's [assert statement](https://www.programiz.com/python-programming/assert-statement) to check types (lists, dataframes) throughout the ETL process. This will make it easier to debug data quality issues if they ever arise.




# Example Queries 

#### Which hour of the day are users starting to play the most songs?

`select hour, count(songplay_id) from songplays inner join time on songplays.start_time = time.start_time group by hour;`

```
 hour | count 
------+-------
    0 |   155
    1 |   154
    2 |   117
    3 |   109
    4 |   136
    5 |   162
    6 |   183
    7 |   179
    8 |   207
    9 |   270
   10 |   312
   11 |   336
   12 |   308
   13 |   324
   14 |   432
   15 |   477
   16 |   542
   17 |   494
   18 |   498
   19 |   367
   20 |   360
   21 |   280
   22 |   217
   23 |   201
(24 rows)
```

#### Which 50 users have started listening to the most songs?

`select user_id, count(songplay_id) from songplays group by user_id;`

```
 user_id | count 
---------+-------
      49 |   689
      80 |   665
      97 |   557
      15 |   463
      44 |   397
      29 |   346
      24 |   321
      73 |   289
      88 |   270
      36 |   248
      16 |   223
      95 |   213
      85 |   179
      30 |   178
      25 |   169
      42 |   140
      58 |   140
      26 |   114
      82 |    87
      72 |    72
      32 |    56
     101 |    55
      50 |    48
      86 |    45
      66 |    37
      37 |    34
      70 |    33
      69 |    29
      10 |    28
      54 |    27
      83 |    27
      92 |    27
       8 |    27
      67 |    25
      61 |    24
       6 |    23
      14 |    22
      53 |    20
      63 |    20
      33 |    20
     100 |    19
      60 |    18
      75 |    18
      52 |    17
      65 |    17
       9 |    16
      35 |    16
      55 |    15
      51 |    15
      78 |    14
(50 rows)

```


#### What are the most popular user agents among users who have played songs?

`select user_agent, count(songplay_id) from songplays group by user_agent order by count(songplay_id) desc;`

```
user_agent                                                                  | count 
---------------------------------------------------------------------------------------------------------------------------------------------+-------
 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36"                  |   971
 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.78.2 (KHTML, like Gecko) Version/7.0.6 Safari/537.78.2"                     |   708
 Mozilla/5.0 (Windows NT 5.1; rv:31.0) Gecko/20100101 Firefox/31.0                                                                           |   696
 "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/36.0.1985.125 Chrome/36.0.1985.125 Safari/537.36"   |   577
 "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36"                                  |   573
 Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:31.0) Gecko/20100101 Firefox/31.0                                                           |   443
 "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36"                             |   427
 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"                             |   419
 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.77.4 (KHTML, like Gecko) Version/7.0.5 Safari/537.77.4"                     |   319
 Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0                                                                    |   310
 "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36"                                    |   259
 "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_2 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D257 Safari/9537.53" |   228
 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36"                 |   179
 "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"                             |   148
 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"                  |   111
 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36"                   |    87
 Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:30.0) Gecko/20100101 Firefox/30.0                                                           |    72
 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36"                   |    45
 Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0                                                                    |    30
 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36"                             |    27
 Mozilla/5.0 (Windows NT 6.1; rv:31.0) Gecko/20100101 Firefox/31.0                                                                           |    26
 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.103 Safari/537.36"                             |    20
 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14"                   |    18
 Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko                                                                        |    16
 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.102 Safari/537.36"                             |    15
 "Mozilla/5.0 (iPhone; CPU iPhone OS 7_1_1 like Mac OS X) AppleWebKit/537.51.2 (KHTML, like Gecko) Version/7.0 Mobile/11D201 Safari/9537.53" |    11
 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"                  |    10
 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/538.46 (KHTML, like Gecko) Version/8.0 Safari/538.46"                            |    10
 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36"                             |    10
 Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)                                                                     |     9
 "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36"                                    |     9
 Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:31.0) Gecko/20100101 Firefox/31.0                                                           |     9
 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/534.59.10 (KHTML, like Gecko) Version/5.1.9 Safari/534.59.10"                   |     8
 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.143 Safari/537.36"                  |     5
 "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14"                   |     5
 Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0                                                                        |     3
 Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)                                                                             |     2
 "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.94 Safari/537.36"                              |     2
 "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36"                             |     2
 Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko                                                                        |     1
(40 rows)                           |     1
```


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
        2428 |      1153 |    3239 |        239 |           0
(1 row)
```
