from fastapi import FastAPI
from database import connect_to_db
# import pyodbc
import os
from cron.index import start_scheduler

app = FastAPI()

# Manually load environment variables from .env file
with open(".env") as f:
    for line in f:
        if line.strip() and not line.startswith("#"):
            key, value = line.strip().split("=", 1)
            os.environ[key] = value
            
@app.get("/")
async def read_root():
    print("route new")
    # Establish database connection
    conn = connect_to_db()
    if conn:
        try:
            # Execute queries or perform database operations
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM your_table")
            rows = cursor.fetchall()
            # Extract column names
            columns = [column[0] for column in cursor.description]
            
            # Fetch rows and convert them to key-value pairs
            rows = cursor.fetchall()
            result = [{column: value for column, value in zip(columns, row)} for row in rows]
            
            cursor.close()
            conn.close()
            return {"data": result}
        except Exception as e:
            return {"error": str(e)}
    else:
        return {"error": "Failed to establish database connection"}

# if __name__ == "__main__":
start_scheduler()