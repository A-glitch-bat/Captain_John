"""
1) python wsgi.py
2) gunicorn --bind 127.0.0.1:8000 wsgi:server
"""
import sys
from raspberry_code.server.main import server

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    server.run(host="127.0.0.1", port=port)
