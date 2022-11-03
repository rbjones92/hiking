from cs50 import SQL
import sqlite3
def create_connection(db_file):
    """ create a database connection to a SQLite database """
        
    conn = sqlite3.connect("hikes.db")

    #sql_drop_table = "DROP TABLE hikes"
    #conn.execute(sql_drop_table)

    sql_create_table = """ CREATE TABLE IF NOT EXISTS hikes (
                                    id integer PRIMARY KEY,
                                    location text NOT NULL,
                                    date text,
                                    distance float
                                ); """

    conn.execute(sql_create_table)

    conn.execute("INSERT INTO hikes (location,date,distance) VALUES('big sur','11/01/2022',10.00)")
    conn.execute("INSERT INTO hikes (location,date,distance) VALUES('fort ord','11/20/2022',8.45)")
    conn.execute("INSERT INTO hikes (location,date,distance) VALUES('pinnacles','12/03/2022',3.15)")


    for row in conn.execute("SELECT * FROM hikes"):
        print(row)


create_connection("sqlite:///hikes.db")