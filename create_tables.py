import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def create_database():

    """
    Connects to the default `studentdb` database in order to set up the
    required `sparkifydb` datbase, before connecting to it.

    Paramters:
    None

    Returns:
    cur (psycopg2.cursor()) - cursor of the (Postgres) `sparkifydb` db
    conn (psycopg2.connect()) - connection to the (Postgres) `sparkifydb` db
    """

    # connect to default database
    # DB connection error handling code adapted from Udacity exercises.

    try:
        conn = psycopg2.connect("host=127.0.0.1 dbname=studentdb user=student\
            password=student")
    except psycopg2.Error as error:
        print("Error: Could not make connection to the Postgres database.")
        print(error)

    conn.set_session(autocommit=True)

    try:
        cur = conn.cursor()
    except psycopg2.Error as error:
        print("Error: Could not get cursor.")
        print(error)

    # create sparkify database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS sparkifydb")
    cur.execute("CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE\
        template0")

    # close connection to default database
    conn.close()

    # connect to sparkify database
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student\
        password=student")
    cur = conn.cursor()

    return cur, conn


def drop_tables(cur, conn):

    """
    Uses the connection and cursor passed in drop any exisitng tables
    with the same names before we run create_tables() to create the tables
    we need.

    Uses the `drop_table_queries` list from the `sql_queries` custom module.

    Parameters:
    cur (psycopg2.cursor()) - cursor of the (Postgres) `sparkifydb` db
    conn (psycopg2.connect()) - connection to the (Postgres) `sparkifydb` db
    """

    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Uses the connection and cursor passed in to create the necessary tables in
    the `sparkifydb` database.

    Uses the `create_table_queries` list from the `sql_queries` custom module.

    Parameters:
    cur (psycopg2.cursor()) - cursor of the (Postgres) `sparkifydb` db
    conn (psycopg2.connect()) - connection to the (Postgres) `sparkifydb` db
    """

    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    cur, conn = create_database()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
