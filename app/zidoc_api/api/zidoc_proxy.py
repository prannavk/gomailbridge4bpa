# from flask import Blueprint, request, jsonify, Response
# from app.zidoc_api.service.zidoc_service import call_zidoc_api
# from app.utils.decorators import log_request_response
# from app.utils.auth import require_api_key
# from app.utils.logger import log
# import json

# bp = Blueprint("zidoc_proxy", __name__)

# @bp.route("/zidoc", methods=["GET"])
# @require_api_key
# @log_request_response
# def proxy_zidoc():
#     # status, result = call_zidoc_api()
#     # return jsonify({"status": status, "result": result}), status
#     log("--- zidoc Request Data Received: ---")
#     print("Headers:", request.headers)
#     print("Query Params:", request.args)
#     isflat = request.args.get("isflat", "false").lower() == "true"
#     status, result = call_zidoc_api(flat=isflat)
#     # return jsonify(result), status
#     return Response(
#         json.dumps(result, sort_keys=False),
#         status=status,
#         content_type="application/json"
#     )

from flask import Blueprint, request, jsonify, Response
from app.zidoc_api.service.zidoc_service import get_flattened_idocs, get_raw_idocs, build_zidoc_report
from app.zidoc_api.hf_service import hf_service
from app.utils.decorators import log_request_response
from app.utils.auth import require_api_key
from app.utils.logger import log, debug_bool
import json

zidoc_bp = Blueprint('zidoc', __name__)

@zidoc_bp.route("/pzidoc", methods=["GET"])
@require_api_key
@log_request_response
def get_pzidoc() -> Response:
    """Endpoint handler for /pzidoc — returns report + flattened value"""
    log("Handling /pzidoc request")
    idocs = get_flattened_idocs()
    report = build_zidoc_report(idocs)
    response = {
        "report": report,
        "value": idocs
    }
    return Response(json.dumps(response), status=200, content_type="application/json")


@zidoc_bp.route("/rawzidoc", methods=["GET"])
@require_api_key
@log_request_response
def get_rawzidoc() -> Response:
    """Endpoint handler for /rawzidoc — returns mock OData metadata + flattened value"""
    log("Handling /rawzidoc request")
    idocs = get_flattened_idocs()
    response = {
        "odata.metadata": "https://example.com/zidoc/$metadata#ZIDOC",
        "value": idocs
    }
    return Response(json.dumps(response), status=200, content_type="application/json")


# @zidoc_bp.route("/hfchat", methods=["POST"])
# @require_api_key
# @log_request_response
# def hf_inference_chat() -> Response:
#     """Vanilla HuggingFace endpoint for general chat input"""
#     data = request.get_json()
#     prompt = data.get("prompt")
#     if not prompt:
#         return jsonify({"error": "Prompt not provided"}), 400

#     try:
#         response = hf_service.generate_text(prompt)
#         return jsonify({"response": response})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500