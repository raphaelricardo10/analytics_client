from app import app
import dashboard
import callbacks

from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    app.run_server(debug=True)