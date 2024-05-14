import pandas as pd
import io
async def convert_json_to_file(json_data, file_format='csv'):
    accepted_file_format=["csv","xlsx"]
    if len(json_data) <=0:
        raise ValueError("Invalid or empty json data.")
        
    if file_format not in accepted_file_format:
        raise ValueError(f"Unsupported file format. Please choose {"".join(accepted_file_format)}")
    # Convert JSON data to Pandas DataFrame
    df = pd.DataFrame(json_data)

    # Save DataFrame to file
    if file_format.lower() == 'csv':
        # Save as CSV
        file_buffer = io.StringIO()
        df.to_csv(file_buffer, index=False)
        file_content = file_buffer.getvalue()
        file_extension = 'csv'
    elif file_format.lower() == 'excel':
        # Save as Excel
        file_buffer = io.BytesIO()
        df.to_excel(file_buffer, index=False)
        file_content = file_buffer.getvalue()
        file_extension = 'xlsx'

    return file_content, file_extension    
    
