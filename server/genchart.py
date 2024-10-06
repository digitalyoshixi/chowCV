import psycopg2
from dotenv import load_dotenv
from flask import jsonify
import os 

load_dotenv()
postgrespass = os.getenv("POSTGRES")

conn = psycopg2.connect(f"user=postgres.mqgqgjeeferesmhxgiew password={postgrespass} host=aws-0-us-east-1.pooler.supabase.com port=6543 dbname=postgres")

# get all items
allitems = []
aitems = []

def getitems():
    with conn:
        with conn.cursor() as dbcurs:
            try:
                dbcurs.execute(f"SELECT * FROM itemlist")
                results = dbcurs.fetchmany(2000)  # Get the first row
                for row in results:
                    print(row[2])
                    if not(str(row[2]) in aitems):
                        aitems.append(row[2])
                        allitems.append([str(row[2]),1])
                    else:
                        allitems[aitems.index(row[2])][1] +=1
                thedict = {}
                for i in range(len(allitems)):
                    thedict.update({allitems[i][0] : allitems[i][1]})
                return thedict
            except (Exception, psycopg2.DatabaseError) as error:
                print(error)

print(getitems())