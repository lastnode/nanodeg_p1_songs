import os
import glob
import psycopg2
import numpy as np
from sql_queries import *
import pandas as pd

# Import some psycopg2 extensions so that we don't get numpy type errors like this when inserting into Postgres:
# > can't adapt type 'numpy.int64'
# Via this StackOverflow answer - https://stackoverflow.com/a/56766135
from psycopg2.extensions import register_adapter, AsIs
psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)

try:
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
except psycopg2.Error as error: 
    print("Error: Could not make connection to the Postgres database.")
    print(error)

try:
    cur = conn.cursor()
except psycopg2.Error as error: 
    print("Error: Could not get cursor.")
    print(error)

def process_song_file(cur, filepath):
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].iloc[0].tolist()
    assert isinstance(song_data, list)
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id','artist_name','artist_location','artist_latitude','artist_longitude']].iloc[0].tolist()
    assert isinstance(artist_data, list)
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    # open log file
    df_log_data = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df_nextsong = df_log_data[df_log_data['page'] == 'NextSong']

    assert isinstance(df_nextsong, pd.DataFrame)

    # convert timestamp column to datetime
    df_nextsong['ts'] = pd.to_datetime(df_nextsong['ts'], unit='ms')
    
    # insert time data records
    time_data = [df_nextsong['ts'], df_nextsong['ts'].dt.hour, df_nextsong['ts'].dt.day, df_nextsong['ts'].dt.weekofyear, df_nextsong['ts'].dt.month, df_nextsong['ts'].dt.year, df_nextsong['ts'].dt.weekday]

    column_labels = ['ts', 'hour', 'day', 'week_of_year', 'month', 'year', 'weekday']

    assert isinstance(time_data, list)
    assert isinstance(column_labels, list)

    time_dict = dict(zip(column_labels,time_data))

    time_df = pd.DataFrame.from_dict(time_dict)

    assert isinstance(time_df, pd.DataFrame)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df_nextsong[['userId', 'firstName', 'lastName', 'gender', 'level']]

    assert isinstance(user_df, pd.DataFrame)

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    df_songplays = df_nextsong

    assert isinstance(df_songplays, pd.DataFrame)

    # insert songplay records
    for index, row in df_songplays.iterrows():

        results = cur.execute(song_select_artist_song_ids, (row.song, row.artist, row.length))
        
        if results:
            song_id, artist_id

        else: 
            song_id = None
            artist_id = None
        
    songplay_data = (row.ts, row.userId, row.level, song_id, artist_id, row.sessionId, row.location, row.userAgent)
    cur.execute(songplay_table_insert, songplay_data)
    conn.commit()
        

def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))

        # Order files by modified date - https://stackoverflow.com/a/168424
        # (So more recently modified files will show up later in the list.)

        assert isinstance(files, list)

        files.sort(key=lambda x: os.path.getmtime(x))
        
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()