import re,json

PATTERN = r"<(.*?)>"
async def convert_json_to_binary(json_data):
    # Serialize JSON object into bytes
    json_bytes = json.dumps(json_data).encode('utf-8')
    return json_bytes

async def get_batch_id_from_error(message: str):
    match = re.search(PATTERN, message)
    if not match:
        return None
    return match.group(1)
