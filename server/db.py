import psycopg2
from dotenv import load_dotenv
import os 

load_dotenv()
postgrespass = os.getenv("POSTGRES")

conn = psycopg2.connect(f"user=postgres.mqgqgjeeferesmhxgiew password={postgrespass} host=aws-0-us-east-1.pooler.supabase.com port=6543 dbname=postgres")

def getitemclass(item):
    with conn:
        with conn.cursor() as dbcurs:
            try:
                dbcurs.execute(f"SELECT * FROM items WHERE itemname = '{item}'")
                result = dbcurs.fetchone()  # Get the first row
                if result:
                    return {
                        'itemname': result[1],
                        'expiry': result[2],
                        'price': result[3],
                        'info': result[4]  # Include `info` in the return
                    }
                return None
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)

def additemclass(itemname, expiry, price, info):
    with conn: # assuming we have connection
        with conn.cursor() as dbcurs:
                try:
                    dbcurs.execute(f"""
                        INSERT INTO items (itemname,expiry,price, info) VALUES
                        ('{itemname}',{expiry},{price}, {info})
                    """)
                except (Exception, psycopg2.DatabaseError) as error:
                    print(error)

def additem(itemname, locx, locy):
    with conn: # assuming we have connection
        with conn.cursor() as dbcurs:
                try:
                    dbcurs.execute(f"""
                        INSERT INTO itemlist (item,location) VALUES
                        ('{itemname}',ARRAY[{locx},{locy}])
                    """)
                except (Exception, psycopg2.DatabaseError) as error:
                    print(error)

