from http.server import BaseHTTPRequestHandler
import json
import os

# Храним ссылку в памяти (в продакшене лучше использовать кэш или БД)
current_bot_link = "https://t.me/DreamGirlBot"
current_bot_username = "DreamGirlBot"

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global current_bot_link, current_bot_username
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        
        response = {
            'bot_link': current_bot_link,
            'bot_username': current_bot_username,
            'updated': True
        }
        
        self.wfile.write(json.dumps(response).encode())
    
    def do_POST(self):
        global current_bot_link, current_bot_username
        
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            if 'bot_link' in data and 'bot_username' in data:
                current_bot_link = data['bot_link']
                current_bot_username = data['bot_username']
                
                print(f"Bot link updated: {current_bot_link}")
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'updated'}).encode())
            else:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Invalid data'}).encode())
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())

# Для обратной совместимости
if __name__ == '__main__':
    from http.server import HTTPServer
    server = HTTPServer(('localhost', 8080), handler)
    print('Starting server...')
    server.serve_forever()