import camp
import psycopg2

# taken from https://www.postgresqltutorial.com/postgresql-python/connect/
def connect():
    try:
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


cursor = connect().cursor()

cursor.execute(open("amp-sql/Agent_Scripts/adm_ietf-dtnma-agent.sql", "r").read())

