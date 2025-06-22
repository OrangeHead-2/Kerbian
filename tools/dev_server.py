import socketserver
import http.server

def start_dev_server(port=8000):
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", port), Handler) as httpd:
        print(f"Serving Kerbian dev server at http://localhost:{port}")
        httpd.serve_forever()