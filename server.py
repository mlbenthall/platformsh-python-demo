import os, time
from http.server import BaseHTTPRequestHandler, HTTPServer

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        body = """
<h1>Hello world!</h1>
<p>With love from Platform.sh</p>
"""
        self.wfile.write(bytes(body, "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer(("localhost", int(os.getenv("PORT"))), MyServer)
    print("Server started http://%s:%s" % ("localhost", os.getenv("PORT")))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
