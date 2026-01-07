from http.server import BaseHTTPRequestHandler
import json
import os

# Просто перенаправляем на основной endpoint
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'use POST to update'}).encode())
    
    def do_POST(self):
        # Перенаправляем запрос в get-bot-link.py
        from get_bot_link import handler as main_handler
        main_handler.do_POST(self)

if __name__ == '__main__':
    from http.server import HTTPServer
    server = HTTPServer(('localhost', 8081), handler)
    print('Starting update server...')
    server.serve_forever()