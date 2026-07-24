import mysql.connector
from mysql.connector import Error


def koneksi_db():

    try:

        conn = mysql.connector.connect(

            host="localhost",

            user="root",

            password="",

            database="db_simpro"

        )

        if conn.is_connected():

            return conn

    except Error as e:

        print("Gagal koneksi :", e)

        return None