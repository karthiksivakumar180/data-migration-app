import os


# Load environment variables
# from dotenv import load_dotenv

# load_dotenv()


def connect_to_db():
    # Define DB2 connection parameters
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    
    try:
        # Establish DB2 connection
        conn_str = f"DSN={db_host};DATABASE={db_name};UID={db_user};PWD={db_password}"
        conn = True
        return conn
    except Exception as e:
        print("Error connecting to DB2:", e)
        return None

    # try:
    #     # Establish DB2 connection
    #     conn = pyodbc.connect(dsn=dsn, user=user, password=password)
    #     return conn
    # except pyodbc.Error as e:
    #     print("Error connecting to DB2:", e)
    #     return None


# def get_db_connection():
#     db_user = os.getenv("DB_USER")
#     db_password = os.getenv("DB_PASSWORD")
#     db_host = os.getenv("DB_HOST")
#     db_port = os.getenv("DB_PORT")
#     db_name = os.getenv("DB_NAME")

#     conn_str = f"DATABASE={db_name};HOSTNAME={db_host};PORT={db_port};PROTOCOL=TCPIP;UID={db_user};PWD={db_password};"
#     conn = ibm_db.connect(conn_str, "", "")
#     return conn
