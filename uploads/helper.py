# from urllib.parse import urlparse
import pandas as pd
import re
import psycopg2
df = pd.read_excel('superstore.xlsx')

conn = psycopg2.connect(
    host = 'tiny.db.elephantsql.com',
    user = 'ctcxsudy',
    password = 'IfJNqXnwyiEsTNJDfXdjNVbvv11X6Vi1',
    database = 'ctcxsudy',
    port = 5432
)

cur = conn.cursor()

def to_snake_case(column_name):
    # Remove special characters
    column_name = re.sub(r'[^\w\s]', '', column_name)
    
    # Replace spaces with underscores and convert to lowercase
    column_name = re.sub(r'\s+', '_', column_name).lower()
    
    return column_name

# Rename columns using snake case
df = df.rename(columns=lambda x: to_snake_case(x) if re.search(r'\s|[^A-Za-z0-9_]', x) else x)

# Print the updated column names
print(df.columns)

def createDataTable():
    # -------------------------------------------------
    #                      Setup Block
    # -------------------------------------------------
    # Get the excel file
    inputFile = 'superstore.xlsx'
    fileName = 'uploads/' + inputFile
    fileName = 'superstore.xlsx'
    print(fileName)

    # Create a Dataframe of that excel file
    df = pd.read_excel(fileName, index_col= False)
    # Define the table name and column names
    table_name = 'DataTable'
    column_names = df.columns.tolist()

    # Define the data types mapping for PostgreSQL
    data_type_mapping = {
        'int64': 'INTEGER',
        'float64': 'NUMERIC',
        'object': 'TEXT',
        'datetime64': 'TIMESTAMP'
    }


    cur.execute("DROP TABLE IF EXISTS {table_name}")

    # Generate the CREATE TABLE statement
    create_table_query = f"CREATE TABLE {table_name} ("

    for col in column_names:
        data_type = data_type_mapping.get(str(df[col].dtype), 'TEXT')
        create_table_query += f"{col} {data_type}, "

    # Remove the trailing comma and space
    create_table_query = create_table_query[:-2]
    create_table_query += ");"

    # Execute the CREATE TABLE statement
    cur.execute(create_table_query)

    # Commit the changes
    conn.commit()

# createDataTable()
# df = pd.read_excel('superstore.xlsx', index_col= False)
