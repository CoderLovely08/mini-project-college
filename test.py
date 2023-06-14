import pandas as pd
import re
import matplotlib.pyplot as plt
from db import createConnection
from graphs import create_bar_chart, create_bubble_chart,create_heatmap, create_line_chart, create_scatter_plot

# Create connection
conn = createConnection()

# df = pd.read_excel('uploads/superstore.xlsx')

# Returns dataframe for the provided file
def readDataFile(fileName):
    fileName = str(fileName).strip()
    if fileName.endswith('.csv'):
        df = pd.read_csv(f'uploads/{fileName}.csv')
    else:
        df = pd.read_excel(f'uploads/{fileName}.xlsx')
        # df = pd.read_excel((f'uploads/{fileName}.xlsx'))
    
    # Rename columns using snake case
    df = df.rename(columns=lambda x: to_snake_case(x) if re.search(r'\s|[^A-Za-z0-9_]', x.lower()) else x.lower())
    return df


# Method to rename columns
def to_snake_case(column_name):
    # Remove special characters
    column_name = re.sub(r'[^\w\s]', '', column_name)
    
    # Replace spaces with underscores and convert to lowercase
    column_name = re.sub(r'\s+', '_', column_name).lower()
    
    return column_name


def is_phone_number(value):
    # Define a regular expression pattern to match phone numbers
    pattern = r'\d{3}-\d{3}-\d{4}'  # Example: xxx-xxx-xxxx
    return bool(re.match(pattern, str(value)))


def createDataTable(df):
    global conn
    # -------------------------------------------------
    #                      Setup Block
    # -------------------------------------------------
    try:
        # Create a Dataframe of that excel file
        # df = pd.read_excel(fileName, index_col=False)
        # Define the table name and column names
        table_name = 'DataTableDev'
        column_names = df.columns.tolist()

        # Define the data types mapping for PostgreSQL
        data_type_mapping = {
            'int64': 'INTEGER',
            'float64': 'NUMERIC',
            'object': 'TEXT',
            'datetime64': 'TIMESTAMP'
        }
        cur = conn.cursor()

        cur.execute(f"DROP TABLE IF EXISTS {table_name}")
        conn.commit()

        cur = conn.cursor()
        # Generate the CREATE TABLE statement
        create_table_query = f"CREATE TABLE {table_name} ("

        for col in column_names:
            data_type = data_type_mapping.get(str(df[col].dtype), 'TEXT')
            if('phone' in col):
                create_table_query += f"{col} TEXT, "
            else:
                create_table_query += f"{col} {data_type}, "

        # Remove the trailing comma and space
        create_table_query = create_table_query[:-2]
        create_table_query += ");"
        
        print(df, create_table_query)
        # Execute the CREATE TABLE statement
        cur.execute(create_table_query)

        # Commit the changes
        conn.commit()
        print("Table Created!")

                # Loop through each row and insert the data into the table
        for row in df.itertuples(index=False):
            # Convert row values to SQL-compatible format
            converted_values = []
            for value in row:
                if isinstance(value, str):
                    # Escape single quotes by doubling them
                    value = value.replace("'", "''")
                    converted_values.append(f"'{value}'")
                elif pd.isnull(value):
                    converted_values.append('NULL')
                elif isinstance(value, pd.Timestamp):
                    converted_values.append(f"'{value.strftime('%Y-%m-%d %H:%M:%S')}'")
                elif isinstance(value, (int, float)):
                    if is_phone_number(value):
                        converted_values.append(f"'{str(value)}'")
                    # Format numeric values without scientific notation
                    else: converted_values.append('{:.6f}'.format(value))

            # Generate the INSERT query for the row
            insert_query = f"INSERT INTO {table_name} VALUES ({', '.join(converted_values)})"
            
            # Execute the INSERT query
            cur.execute(insert_query)
        
        # Commit the changes
        conn.commit()
        print("Rows Inserted!")
        return 0

#         print("Rows Inserted!")

    except Exception as e:
        # Handle the exception here
        conn.rollback()
        print("An error occurred:", str(e))
        return 1


def fetchAllData():
    global conn
    cur = conn.cursor()
    cur.execute("SELECT * FROM DataTable")
    results = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]  # Get column names
    return [results, column_names]
# createCharts(1,'Name','Percentage',readDataFile('inputfile'))

def getColumns():
    global conn
    cur = conn.cursor()
    cur.execute("SELECT * FROM DataTable LIMIT 1")
    column_names = [desc[0] for desc in cur.description]  # Get column names
    return column_names

def createChart(id, xLabel, yLabel, dataframe):
    z_values = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    bubbleValues = [20, 30, 40, 50, 60]
    match id:
        case 1: return create_bar_chart(dataframe[str(xLabel)], dataframe[str(yLabel)], xLabel, yLabel,'bar_chart')
        case 2: return create_line_chart(dataframe[str(xLabel)], dataframe[str(yLabel)], xLabel, yLabel,'line_chart')
        case 3: return create_scatter_plot(dataframe[str(xLabel)], dataframe[str(yLabel)], xLabel, yLabel,'scatter_plot')
        case 4: return create_heatmap(z_values, dataframe[str(xLabel)], dataframe[str(yLabel)], xLabel, yLabel,'heatmap')
        case 5: return create_bubble_chart(dataframe[str(xLabel)], dataframe[str(yLabel)], bubbleValues , xLabel, yLabel,'bubble_chart')


def runQuery(query):
    global conn
    cur = conn.cursor()
    cur.execute(f"{query}")
    results = cur.fetchall()
    column_names = [desc[0] for desc in cur.description]  # Get column names
    return [results, column_names ,query]