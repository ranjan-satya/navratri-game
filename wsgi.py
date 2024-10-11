# wsgi.py
from app import server  # Import the server from your main app file

if __name__ == "__main__":
    server.run(debug=True)