from dotenv import load_dotenv
import psycopg2
import os

# Load environment variables from .env file
load_dotenv()

def createConnection():
    # Database setup
    conn = psycopg2.connect(
        host = os.getenv('DB_HOST'),
        user = os.getenv('DB_USER'),
        password = os.getenv('DB_PASSWORD'),
        database = os.getenv('DB_DATABASE'),
        port = 5432
    )

    return conn
