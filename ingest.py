from unicodedata import decimal
import requests
import psycopg2

with requests.get("http://127.0.0.1:5000/very_large_request/100", stream=True) as r:

    conn = psycopg2.connect(host="localhost",port="5433",dbname="stream_test", user="postgres",password="postgres")
    cur = conn.cursor()
    sql = "INSERT INTO transactions(txid, uid, amount) VALUES (%s, %s, %s)"

    cur.execute("truncate table public.transactions;")
    conn.commit()

    buffer = ""
    for chunk in r.iter_content(chunk_size=1):
        if chunk.endswith(b'\n'):
            t = eval(buffer)
            print(t)
            if float(t[2]) > 200.0:
                print(type(t[2]))
            cur.execute(sql, (t[0],t[1],t[2]))
            conn.commit()
            
            buffer = ""
        else:
            buffer += chunk.decode()

