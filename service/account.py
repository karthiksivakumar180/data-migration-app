from service.api_abstract import send_post_request
from service.csv_conversion import convert_json_to_file
import re
from utils.helpers import get_batch_id_from_error

ACCCOUNT_SUB_URL = "/data/v58.0/jobs/ingest"


async def create_job():
    url = ACCCOUNT_SUB_URL
    post_data = {
        "object": "Account",
        "externalIdFieldName": "EXT_ID__c",
        "contentType": "CSV",
        "operation": "upsert",
        "lineEnding": "CRLF",
    }
    header = {"Content-Type": "application/json"}
    # create_job_response = await send_post_request(
    #     url, "POST", post_data, None, None, header
    # )
    create_job_response = {"id": "750H1000005JFA4IAO"}
    print("create_job_response", create_job_response)
    if create_job_response is not None:
        batch_id = create_job_response.get("id", None)
        if batch_id is not None:
            sample_data = [
                {"LastName": "test2", "EXT_ID__c": 3245325323},
                {"LastName": "test1", "EXT_ID__c": 324532532},
            ]
            file, _ = await convert_json_to_file(sample_data)
            print("batch id", batch_id)
            await csv_import(batch_id, file)


async def csv_import(batch_id: str, csv_file):
    url_format = f"{ACCCOUNT_SUB_URL}/{batch_id}/batches/"
    file_data = {"file": csv_file}
    header = {"Content-Type": "text/csv"}
    csv_import_response = await send_post_request(
        url_format, "PUT", None, file_data, None, header
    )
    print("csv_import_response", csv_import_response)
    if (
        csv_import_response
        and "id" not in csv_import_response
        and len(csv_import_response)
    ):
        error_message = csv_import_response[0]["message"]
        print("error_message", error_message)

        prev_batch_id = await get_batch_id_from_error(error_message)
        if prev_batch_id is not None:
            update_job_resp = await update_job(prev_batch_id)
            print("update_job_resp", update_job_resp)
            if "id" in update_job_resp:
                print("Job ID:", prev_batch_id)


async def get_patch_success(batch_id: str):
    url = f"{ACCCOUNT_SUB_URL}/{batch_id}/successfulResults/"


async def get_patch_failed_result(batch_id: str):
    url = f"{ACCCOUNT_SUB_URL}{batch_id}/failedResults/"


async def update_job(batch_id: str, status: str = "UploadComplete"):
    url = f"{ACCCOUNT_SUB_URL}/{batch_id}"
    post_data = {"state": "UploadComplete"}

    update_job_response = await send_post_request(
        url, "PATCH", post_data, None, None, {"Content-Type": "application/json"}
    )
    return update_job_response
    # prev_batch_id = match.group(1)
