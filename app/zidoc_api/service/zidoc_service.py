# import requests
# from app.config import ZIDOC_CLIENT_ID, ZIDOC_CLIENT_SECRET, ZIDOC_TOKEN_URL, ZIDOC_SCOPE, ZIDOC_DATA_API_URL
# from app.utils.logger import log

# _token_cache = {"access_token": None}

# def flatten_dict(nested_dict, prefix=""):
#     flat = {}
#     for key, value in nested_dict.items():
#         if isinstance(value, dict):
#             for sub_key, sub_val in value.items():
#                 flat[f"{key}_{sub_key}"] = sub_val
#         else:
#             flat[f"{prefix}{key}"] = value
#     return flat

# def get_new_token():
#     log("Requesting new ZIDOC token")
#     payload = {
#         "client_id": ZIDOC_CLIENT_ID,
#         "client_secret": ZIDOC_CLIENT_SECRET,
#         "grant_type": "client_credentials"
#     }
#     if ZIDOC_SCOPE:
#         payload["scope"] = ZIDOC_SCOPE

#     response = requests.post(ZIDOC_TOKEN_URL, data=payload)
#     if response.status_code == 200:
#         access_token = response.json().get("access_token")
#         _token_cache["access_token"] = access_token
#         log("ZIDOC token acquired")
#         return access_token
#     else:
#         log(f"ZIDOC token fetch failed: {response.status_code} {response.text}")
#         return None

# def call_zidoc_api(flat=False):
#     token = _token_cache.get("access_token") or get_new_token()
#     headers = {"Authorization": f"Bearer {token}"}

#     log("Calling ZIDOC data API with token")
#     response = requests.get(ZIDOC_DATA_API_URL, headers=headers)

#     # if response.status_code == 401:
#     #     log("ZIDOC token expired — fetching new token")
#     #     token = get_new_token()
#     #     headers["Authorization"] = f"Bearer {token}"
#     #     response = requests.get(ZIDOC_DATA_API_URL, headers=headers)

#     # return response.status_code, response.json() if response.ok else response.text
#     # Retry if token expired
#     if response.status_code == 401:
#         log("ZIDOC token expired — refreshing")
#         token = get_new_token()
#         headers["Authorization"] = f"Bearer {token}"
#         response = requests.get(ZIDOC_DATA_API_URL, headers=headers)

#     if not response.ok:
#         return response.status_code, response.text

#     if flat:
#         log("Flattening ZIDOC response")
#         original_list = response.json()
#         flat_list = [flatten_dict(entry) for entry in original_list]
#         return 200, flat_list

#     return 200, response.json()
import requests
from app.config import ZIDOC_CLIENT_ID, ZIDOC_CLIENT_SECRET, ZIDOC_TOKEN_URL, ZIDOC_SCOPE, ZIDOC_DATA_API_URL
from app.utils.logger import log, debug_bool
# from app.zidoc_api.api.zidoc_proxy import debug_bool
from app.zidoc_api.utils.flattener import flatten_idoc_response
from app.zidoc_api.utils.preprocessor import compute_idoc_statistics
from app.zidoc_api.utils.point_generators import (
    generate_status_analysis,
    generate_traffic_spike_insight,
    generate_segment_error_focus,
    generate_partner_mismatch_alerts,
    generate_delay_summary
)
from app.zidoc_api.utils.point_generators import generate_all_points_parallel

_token_cache = {"access_token": None}


def get_new_token():
    log("Requesting new ZIDOC token", debug_bool)
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
        log("ZIDOC token acquired", debug_bool)
        return access_token
    else:
        log(f"ZIDOC token fetch failed: {response.status_code} {response.text}", debug_bool)
        return None


def get_raw_idocs() -> list[dict]:
    token = _token_cache.get("access_token") or get_new_token()
    headers = {"Authorization": f"Bearer {token}"}
    log("Calling ZIDOC data API with token", debug_bool)
    response = requests.get(ZIDOC_DATA_API_URL, headers=headers)

    if response.status_code == 401:
        log("ZIDOC token expired — refreshing", debug_bool)
        token = get_new_token()
        headers["Authorization"] = f"Bearer {token}"
        response = requests.get(ZIDOC_DATA_API_URL, headers=headers)

    if not response.ok:
        log("Failed to fetch ZIDOC data", debug_bool)
        raise Exception(f"Failed to fetch ZIDOC data: {response.status_code} {response.text}")        

    return response.json()


def get_flattened_idocs() -> list[dict]:
    raw_data = get_raw_idocs()
    return flatten_idoc_response(raw_data)


def build_zidoc_report(idoc_array: list[dict]) -> str:
    # stats = compute_idoc_statistics(idoc_array)
    # point1 = generate_status_analysis(stats)
    # point2 = generate_traffic_spike_insight(stats)
    # point3 = generate_segment_error_focus(stats)
    # point4 = generate_partner_mismatch_alerts(stats)
    # point5 = generate_delay_summary(stats)
    
    stats = compute_idoc_statistics(idoc_array)
    point1, point2, point3, point4, point5 = generate_all_points_parallel(stats)

    return f"""
    <html>
    <head>
        <style>
        body {{
            font-family: Arial, sans-serif;
            color: #333;
            line-height: 1.6;
            padding: 20px;
        }}
        h2 {{
            color: #2c3e50;
            border-bottom: 2px solid #ccc;
            padding-bottom: 5px;
        }}
        h3 {{
            margin-top: 30px;
            color: #2980b9;
        }}
        ul {{
            margin: 10px 0;
            padding-left: 20px;
        }}
        li {{
            margin: 5px 0;
        }}
        div {{
            background: #f9f9f9;
            border-left: 4px solid #2980b9;
            padding: 10px;
            margin-top: 10px;
        }}
        </style>
    </head>
    <body>
        <h2>ZIDOC Analytics Report</h2>
        {point1}
        <hr/>
        {point2}
        <hr/>
        {point3}
        <hr/>
        {point4}
        <hr/>
        {point5}
    </body>
    </html>
    """
