import os
import mysql.connector

COURSES = ['Biology', 'Math', 'Astronomy', 'Physics', 'Computers']


def connect_to_db(host='localhost', user='root', password='', database='school'):
    """ Connect to mysql database """

    # if the password was not supply use the default one
    if not password:
        password = os.getenv('Database')

    conn = mysql.connector.connect(host=host, user=user,
                                   password=password, database=database)
    return conn
