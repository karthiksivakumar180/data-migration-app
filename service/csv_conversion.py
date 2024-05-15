import pandas as pd
import io

 
chunk_df['id'] = [uuid.uuid4() for _ in range(len(chunk_df))]
df_bytes = df.to_csv(index=False).encode()
chunk_size = 100 * 1024 * 1024  # 100MB in bytes

# Chunk the DataFrame
chunks = []
start = 0
while start < len(df_bytes):
    end = start + chunk_size
    chunk_data = df_bytes[start:end].decode()
    chunk_df = pd.read_csv(pd.compat.StringIO(chunk_data))
    chunks.append(chunk_df)
    start = end
    
async def convert_json_to_file(json_data, file_format="csv"):
    # Convert JSON data to Pandas DataFrame
    df = pd.DataFrame(json_data)

    # Save DataFrame to file
    if file_format.lower() == "csv":
        # Save as CSV
        file_buffer = io.StringIO()
        df.to_csv(file_buffer, index=False)
        file_content = file_buffer.getvalue()
        file_extension = "csv"
    elif file_format.lower() == "excel":
        # Save as Excel
        file_buffer = io.BytesIO()
        df.to_excel(file_buffer, index=False)
        file_content = file_buffer.getvalue()
        file_extension = "xlsx"
    # else:
    #     raise ValueError("Unsupported file format. Please choose 'csv' or 'excel'.")

    return file_content, file_extension


# async def convert_json_to_file(json_data, file_format='csv'):
#     accepted_file_format=["csv","xlsx"]
#     if len(json_data) <=0:
#         raise ValueError("Invalid or empty json data.")

#     if file_format not in accepted_file_format:
#         raise ValueError(f"Unsupported file format. Please choose {"".join(accepted_file_format)}")
#     # Convert JSON data to Pandas DataFrame
#     df = pd.DataFrame(json_data)
#     # Save DataFrame to file buffer
#     file_buffer = io.BytesIO()
#     # Save DataFrame to file
#     if file_format.lower() == 'csv':
#         # Save as CSV
#         # file_buffer = io.StringIO()
#         # df.to_csv(file_buffer, index=False)
#         # file_content = file_buffer.getvalue()
#         df.to_csv(file_buffer, index=False)
#         file_extension = 'csv'
#     elif file_format.lower() == 'excel':
#         # Save as Excel
#         # file_buffer = io.BytesIO()
#         # df.to_excel(file_buffer, index=False)
#         # file_content = file_buffer.getvalue()
#         df.to_excel(file_buffer, index=False)
#         file_extension = 'xlsx'
#     # Set the file buffer position to the beginning
#     file_buffer.seek(0)
#     return file_buffer, file_extension
