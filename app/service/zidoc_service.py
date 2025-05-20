import requests
from app.config import ZIDOC_CLIENT_ID, ZIDOC_CLIENT_SECRET, ZIDOC_TOKEN_URL, ZIDOC_SCOPE, ZIDOC_DATA_API_URL
from app.utils.logger import log

_token_cache = {"access_token": None}

def flatten_dict(nested_dict, prefix=""):
    flat = {}
    for key, value in nested_dict.items():
        if isinstance(value, dict):
            for sub_key, sub_val in value.items():
                flat[f"{key}_{sub_key}"] = sub_val
        else:
            flat[f"{prefix}{key}"] = value
    return flat

def get_new_token():
    log("Requesting new ZIDOC token")
    payload = {
        "client_id": ZIDOC_CLIENT_ID,
        "client_secret": ZIDOC_CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    if ZIDOC_SCOPE:
        payload["scope"] = ZIDOC_SCOPE

    response = requests.post(ZIDOC_TOKEN_URL, data=payload)
    if response.status_code == 200:
        access_token = response.json().get("access_token")
        _token_cache["access_token"] = access_token
        log("ZIDOC token acquired")
        return access_token
    else:
        log(f"ZIDOC token fetch failed: {response.status_code} {response.text}")
        return None

def call_zidoc_api(flat=False):
    token = _token_cache.get("access_token") or get_new_token()
    headers = {"Authorization": f"Bearer {token}"}

    log("Calling ZIDOC data API with token")
    response = requests.get(ZIDOC_DATA_API_URL, headers=headers)

    # if response.status_code == 401:
    #     log("ZIDOC token expired — fetching new token")
    #     token = get_new_token()
    #     headers["Authorization"] = f"Bearer {token}"
    #     response = requests.get(ZIDOC_DATA_API_URL, headers=headers)

    # return response.status_code, response.json() if response.ok else response.text
    # Retry if token expired
    if response.status_code == 401:
        log("ZIDOC token expired — refreshing")
        token = get_new_token()
        headers["Authorization"] = f"Bearer {token}"
        response = requests.get(ZIDOC_DATA_API_URL, headers=headers)

    if not response.ok:
        return response.status_code, response.text

    if flat:
        log("Flattening ZIDOC response")
        original_list = response.json()
        flat_list = [flatten_dict(entry) for entry in original_list]
        return 200, flat_list

    return 200, response.json()
