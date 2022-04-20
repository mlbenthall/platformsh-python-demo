import pymysql
import os, time
from http.server import BaseHTTPRequestHandler, HTTPServer

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        try:
            # Connect to the database.
            conn = pymysql.connect(host=os.getenv("DB_HOST"),
                                port=int(os.getenv("DB_PORT")),
                                database=os.getenv("DB_PATH"),
                                user=os.getenv("DB_USER"),
                                password="")
            print("set query")
            sql = '''
                    CREATE TABLE People (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(30) NOT NULL,
                    city VARCHAR(30) NOT NULL
                    )
                    '''

            cur = conn.cursor()
            cur.execute(sql)
            sql = '''
                    INSERT INTO People (name, city) VALUES
                    ('Neil Armstrong', 'Moon'),
                    ('Buzz Aldrin', 'Glen Ridge'),
                    ('Sally Ride', 'La Jolla');
                    '''

            cur.execute(sql)

            # Show table.
            sql = '''SELECT * FROM People'''
            cur.execute(sql)
            result = cur.fetchall()

            table = '''<table>
    <thead>
    <tr><th>Name</th><th>City</th></tr>
    </thead>
    <tbody>'''

            if result:
                for record in result:
                    table += '''<tr><td>{0}</td><td>{1}</td><tr>\n'''.format(record[1], record[2])
                table += '''</tbody>\n</table>\n'''

            # Drop table
            sql = '''DROP TABLE People'''
            cur.execute(sql)

            # Close communication with the database
            cur.close()
            conn.close()

            # return table

            self.wfile.write(bytes(table, "utf-8"))

        except Exception as e:
            print(e)


if __name__ == "__main__":        
    webServer = HTTPServer(("localhost", int(os.getenv("PORT"))), MyServer)
    print("Server started http://%s:%s" % ("localhost", os.getenv("PORT")))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
