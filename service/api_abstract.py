import httpx, os, requests
from fastapi import HTTPException, status
from config import settings

# AUTH_TOKEN = None
BASE_URL = settings.BASE_URL
# HEADERS = {"Authorization": f"Bearer {AUTH_TOKEN}"}


async def set_auth_token():
    print("set auth token")
    # print(settings)
    # if not BASE_URL:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="Unable to find BASE_URL in .env",
    #     )

    check_required_keys = [
        "BASE_URL",
        "CLIENT_ID",
        "CLIENT_SECRET",
        "USERNAME",
        "PASSWORD",
    ]
    missing_keys = []
    for key in check_required_keys:
        # print(key)
        if not settings.dict()[key]:
            missing_keys.append(key)
    # print("missing_keys", missing_keys)

    if len(missing_keys):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=",".join(missing_keys) + " keys are missing",
        )

    # if not os.getenv("CLIENT_ID"):
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, detail="please set client id in .env"
    #     )

    # if not os.getenv("CLIENT_SECRET"):
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="please set client secret in .env",
    #     )
    # if not os.getenv("USERNAME"):
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, detail="please set username in .env"
    #     )

    # if not os.getenv("PASSWORD"):
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND, detail="please set password in .env"
    #     )

    params = {
        "grant_type": "password",
        "client_id": settings.CLIENT_ID,
        "client_secret": settings.CLIENT_SECRET,
        "username": settings.USERNAME,
        "password": settings.PASSWORD,
    }
    auth_url = "/oauth2/token"

    # print("BASE_URL", BASE_URL)
    # auth_response = await send_post_request(auth_url, None, params)
    auth_response = requests.post(BASE_URL + auth_url, params=params)
    # print("auth_response", auth_response)
    dict_resp = auth_response.json()
    if auth_response.status_code == 200:
        # print("auth_response", auth_response.text)
        if dict_resp and "access_token" in dict_resp:
            auth_token = dict_resp["access_token"]
            return {"Authorization": f"Bearer {auth_token}"}
    # print("AUTH_TOKEN", AUTH_TOKEN)
    return dict_resp


async def send_get_request(url, params=None):
    get_header = await set_auth_token()
    async with httpx.AsyncClient() as client:
        try:
            full_url = f"{BASE_URL}{url}"
            print("full_url get", full_url)
            response = await client.get(
                full_url, params=params, headers=get_header, timeout=20
            )
            return  response.json() if response.text  else None
        except httpx.HTTPError as exc:
            print("HTTP error:", exc)
            return None
        except Exception as exc:
            print("An error occurred:", exc)
            return None


async def send_post_request(
    url, method="POST", data=None, files=None, params=None, new_headers=None
):
    try:
        # Set the request headers
        headers = await set_auth_token()
        if new_headers:
            headers.update(new_headers)

        # Validate the HTTP method
        method = method.upper()
        if method not in ["POST", "PUT", "PATCH"]:
            raise ValueError(
                "Unsupported HTTP method. Please use 'POST', 'PATCH', or 'PUT'."
            )

        async with httpx.AsyncClient() as client:
            full_url = f"{BASE_URL}{url}"
            if method == "POST":
                response = await client.post(
                    full_url,
                    json=data,
                    params=params,
                    files=files,
                    headers=headers,
                    timeout=20,
                )
            elif method == "PUT":
                response = await client.put(
                    full_url,
                    data=data,
                    params=params,
                    files=files,
                    headers=headers,
                    timeout=20,
                )
            elif method == "PATCH":
                response = await client.patch(
                    full_url,
                    json=data,
                    params=params,
                    files=files,
                    headers=headers,
                    timeout=20,
                )
            #print("response", response.text)
            response_data = None
            if response.text:
                response_data = response.json()
            #print("response.status_code", response.status_code)
            return response_data, response.status_code
    except httpx.HTTPError as exc:
        print("HTTP error:", exc)
        return None, None
    except Exception as exc:
        print("An error occurred:", exc)
        return None, None


# async def send_post_request(
#     url, method="POST", data=None, files=None, params=None, header=None
# ):
#     post_header = await set_auth_token()
#     if header:
#         post_header.update(header)

#     async with httpx.AsyncClient() as client:
#         try:
#             full_url = f"{BASE_URL}{url}"
#             if method.upper() not in ["POST", "PUT", "PATCH"]:
#                 raise ValueError(
#                     "Unsupported HTTP method. Please use 'POST','PATCH' or 'PUT'."
#                 )

#             if method.upper() == "POST":
#                 response = await client.post(
#                     full_url,
#                     json=data,
#                     params=params,
#                     files=files,
#                     headers=post_header,
#                     timeout=20,
#                 )
#             elif method.upper() == "PUT":
#                 response = await client.put(
#                     full_url,
#                     data=data,
#                     params=params,
#                     files=files,
#                     headers=post_header,
#                     timeout=20,
#                 )
#             elif method.upper() == "PATCH":
#                 response = await client.patch(
#                     full_url,
#                     json=data,
#                     params=params,
#                     files=files,
#                     headers=post_header,
#                     timeout=20,
#                 )
#             return response.json(), response.status_code
#         except httpx.HTTPError as exc:
#             print("HTTP error:", exc)
#             return None
#         except Exception as exc:
#             print("An error occurred:", exc)
#             return None


# https://mrfcorplimited--oidev.sandbox.my.salesforce.com/services/data/v58.0/jobs/ingest/

# {
#     "object":"Account",
#     "externalIdFieldName" :"EXT_ID__c",
#     "contentType":"CSV",
#     "operation":"upsert",
#     "lineEnding":"CRLF"
# }

# https://mrfcorplimited--oidev.sandbox.my.salesforce.com/services/data/v58.0/jobs/ingest/750H1000005JEAcIAO/batches/

# https://mrfcorplimited--oidev.sandbox.my.salesforce.com/services/data/v58.0/jobs/ingest/750H1000005JE4KIAW/

# {
#     "state": "UploadComplete"
# }


# https://mrfcorplimited--oidev.sandbox.my.salesforce.com/services/data/v56.0/jobs/ingest/750H1000005JEADIA4/successfulResults/
# https://mrfcorplimited--oidev.sandbox.my.salesforce.com/services/data/v56.0/jobs/ingest/750H1000005JE4KIAW/failedResults/
