from dotenv import load_dotenv
import openai
import os
from test import getColumns

# Load environment variables from .env file
load_dotenv()

def convert_prompt_to_sql(prompt):
    openai.api_key = os.getenv('OPEN_AI_API_KEY')

    # Generate SQL query using the prompt
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.0,
    )

    # Extract the SQL query from the API response
    sql_query = response.choices[0].text.strip()

    return sql_query


def generate_query(query):
    columns = getColumns()
    # Example usage
    prompt = f"""
    Generate SQL query for the following
    The table name is DataTable
    The columns are {columns} \n""" + query + " Return only SQL Query nothing else"
    sql_query = convert_prompt_to_sql(prompt)
    print("Generated SQL query:", sql_query)
    return sql_query
