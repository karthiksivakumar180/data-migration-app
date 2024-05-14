import re

PATTERN = r"<(.*?)>"


async def get_batch_id_from_error(message: str):
    match = re.search(PATTERN, message)
    if not match:
        return None
    return match.group(1)
