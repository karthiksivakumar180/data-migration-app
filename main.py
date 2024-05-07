from fastapi import FastAPI
from database import connect_to_db
import pyodbc

app = FastAPI()


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
            result = [{"column1": row.column1, "column2": row.column2} for row in rows]
            cursor.close()
            conn.close()
            return {"data": result}
        except pyodbc.Error as e:
            return {"error": str(e)}
    else:
        return {"error": "Failed to establish database connection"}
