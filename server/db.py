import psycopg2
from dotenv import load_dotenv
import os 

load_dotenv()
postgrespass = os.getenv("POSTGRES")

conn = psycopg2.connect(f"user=postgres.mqgqgjeeferesmhxgiew password={postgrespass} host=aws-0-us-east-1.pooler.supabase.com port=6543 dbname=postgres")

def getitem(item):
    with conn: # assuming we have connection
        with conn.cursor() as dbcurs:
            try:
                dbcurs.execute(f"SELECT * FROM items where itemname = '{item}'")
                results = dbcurs.fetchall()
                # result = dbcurs.fetchone() # fetch only one row
                # print(results)
                for row in results:
    	            print(row)
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)

getitem("milk")