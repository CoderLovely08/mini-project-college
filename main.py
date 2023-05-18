import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import os

# Step 1: give location of file
file_name = "data/format_xlsx/pokemon_data_250.xlsx"

if file_name.endswith('.csv'):
    df = pd.read_csv(file_name)
else:
    df = pd.read_excel(file_name)

# Step 2: Set up a connection to your PostgreSQL database
db_host = 'your_database_host'
db_port = 'your_database_port'
db_name = 'your_database_name'
db_user = 'your_database_user'
db_password = 'your_database_password'

conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    database=db_name,
    user=db_user,
    password=db_password
)

# Step 3: Create an SQLAlchemy engine using the connection
engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')

# Step 4: Extract table name from the file name
table_name = os.path.splitext(os.path.basename(file_name))[0]

# Step 5: Upload the DataFrame to the database as a table
df.to_sql(table_name, engine, index=False, if_exists='replace')
