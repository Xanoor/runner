# backend/main.py

from app import app
from services.app_service import read_data

if __name__ == "__main__":
    read_data(True)
    app.run(debug=True)
