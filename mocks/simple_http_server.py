#!/usr/bin/env python3
"""Simple HTTP server for serving test pages."""
import http.server
import os
import socketserver

DEFAULT_PORT = 8000

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Print log messages to stdout
        super().log_message(format, *args)

def run(port: int = DEFAULT_PORT):
    pages_dir = os.path.join(os.path.dirname(__file__), 'pages')
    os.chdir(pages_dir)
    with socketserver.TCPServer(('', port), Handler) as httpd:
        print(f"Serving mock pages at http://localhost:{port}/")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Start simple HTTP server for tests')
    parser.add_argument('--port', type=int, default=DEFAULT_PORT, help='Port to serve on')
    args = parser.parse_args()
    run(args.port)
