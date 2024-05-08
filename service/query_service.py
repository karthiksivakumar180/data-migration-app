from database import connect_to_db


def execute_dynamic_query(table_name, dynamic_where=None, page_number=1, page_size=10):
    conn = connect_to_db()
    if conn:
        try:
            # Execute queries or perform database operations
            cursor = conn.cursor()
            # Construct the SQL query without the WHERE clause if dynamic_where is None
            if dynamic_where is None:
                query = f"SELECT * FROM {table_name}_SF ORDER BY id OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
                cursor.execute(query, ((page_number - 1) * page_size, page_size))
            else:
                # Construct the SQL query with the WHERE clause
                offset = (page_number - 1) * page_size
                query = f"SELECT * FROM {table_name}_SF WHERE {dynamic_where} ORDER BY id OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
                cursor.execute(query, (offset, page_size))

            rows = cursor.fetchall()
            # Extract column names
            columns = [column[0] for column in cursor.description]
            result = [
                {column: value for column, value in zip(columns, row)} for row in rows
            ]

            cursor.close()
            conn.close()
            return {"data": result}
        except Exception as e:
            return {"error": str(e)}
    else:
        return {"error": "Failed to establish database connection"}
