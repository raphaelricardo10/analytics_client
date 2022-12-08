from app import app
import dashboard
import callbacks

from dotenv import load_dotenv

load_dotenv('./env')
server=app.server

if __name__ == '__main__':
    app.run_server(debug=True)