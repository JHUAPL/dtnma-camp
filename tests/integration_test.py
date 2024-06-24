import camp
import psycopg2

# taken from https://www.postgresqltutorial.com/postgresql-python/connect/
def connect():
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(
            host="localhost",
            port=5432,
            database="amp_core",
            user="root",
            password="root"
        ) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


print("hello world")

connect()
