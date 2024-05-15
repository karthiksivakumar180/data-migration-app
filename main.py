from fastapi import FastAPI
from database import connect_to_db
from service.account import create_job, get_patch_info

# import pyodbc
import os
from cron.index import start_scheduler

# from service.account import create_job

app = FastAPI()
# https://663b1359fee6744a6ea0354b.mockapi.io/api/v1/contacts/create

# Manually load environment variables from .env file
# with open(".env") as f:
#     for line in f:
#         if line.strip() and not line.startswith("#"):
#             key, value = line.strip().split("=", 1)
#             # print("key",key,"value",value)
#             os.environ[key] = value


@app.get("/sales_district")
async def read_root():
    print("route new")
    # Establish database connection
    # return await get_patch_info("750H1000005JFsQIAW")
    return await create_job()
    return {"error": "Failed to establish database connection"}


# if __name__ == "__main__":
start_scheduler()
