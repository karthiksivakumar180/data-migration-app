from service.api_abstract import send_post_request, send_get_request
from service.csv_conversion import convert_json_to_file
import re
from utils.helpers import get_batch_id_from_error, convert_json_to_binary

ACCCOUNT_SUB_URL = "/data/v58.0/jobs/ingest"
JOB_STATUS_LIST = ["Open", "UploadComplete", "Aborted", "JobComplete", "Failed"]

SAMPLE_DATA = [
                {"LastName": "jacky", "EXT_ID__c": 32453253230012},
                {"LastName": "roopin", "EXT_ID__c": 3245325320013},
            ]
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
    create_job_response, _ = await send_post_request(
        url, "POST", post_data, None, None, header
    )
    # create_job_response = {"id": "750H1000005JFbZIAW"}
    print("create_job_response", create_job_response)
    # return
    if create_job_response is not None:
        batch_id = create_job_response.get("id", None)
        if batch_id is not None:
            
            file, file_type = await convert_json_to_file(SAMPLE_DATA)
            # file=await convert_json_to_binary(sample_data)
            print("batch id", batch_id)
            await csv_import(batch_id, file)


async def csv_import(batch_id: str, csv_file):
    url_format = f"{ACCCOUNT_SUB_URL}/{batch_id}/batches/"
    file_data = str(csv_file)
    print("file_data",file_data)
    header = {"Content-Type": "text/csv", "Accept": "application/json"}
    csv_import_response, response_code = await send_post_request(
        url_format, "PUT", file_data, None, None, header
    )
    print("csv_import_response code", response_code)
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
            # print("update_job_resp", update_job_resp)
            if "id" in update_job_resp:
                print("Job ID:", prev_batch_id)


async def get_patch_unprocessed(batch_id: str):
    get_batch_unprocessed_url = f"{ACCCOUNT_SUB_URL}/{batch_id}/unprocessedrecords/"
    return await send_get_request(get_batch_unprocessed_url)


async def get_patch_info(batch_id: str):
    get_batch_info_url = f"{ACCCOUNT_SUB_URL}/{batch_id}/"
    batch_data = await send_get_request(get_batch_info_url)
    print("batch_data", batch_data)
    return batch_data


async def get_patch_success(batch_id: str):
    get_batch_success_url = f"{ACCCOUNT_SUB_URL}/{batch_id}/successfulResults/"
    return await send_get_request(
        get_batch_success_url,
        None,
        {"Content-Encoding": "gzip", "Transfer-Encoding": "chunked"},
    )


async def get_patch_failed_result(batch_id: str):
    get_batch_failed_url = f"{ACCCOUNT_SUB_URL}{batch_id}/failedResults/"
    return await send_get_request(
        get_batch_failed_url,
        None,
        {"Content-Encoding": "gzip", "Transfer-Encoding": "chunked"},
    )


async def update_job(batch_id: str, status: str = "UploadComplete"):
    url = f"{ACCCOUNT_SUB_URL}/{batch_id}"
    post_data = {"state": "UploadComplete"}

    update_job_response, _ = await send_post_request(
        url, "PATCH", post_data, None, None, {"Content-Type": "application/json"}
    )
    return update_job_response
    # prev_batch_id = match.group(1)
