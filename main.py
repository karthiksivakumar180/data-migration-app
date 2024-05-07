from fastapi import FastAPI
import database

app = FastAPI()

@app.get("/")
async def read_root():
    conn = database.get_db_connection()
    # Execute database queries here
    return {"message": "Hello World"}
