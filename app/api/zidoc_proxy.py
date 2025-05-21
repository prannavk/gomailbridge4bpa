from flask import Blueprint, request, jsonify, Response
from app.service.zidoc_service import call_zidoc_api
from app.utils.decorators import log_request_response
from app.utils.auth import require_api_key
from app.utils.logger import log
import json

bp = Blueprint("zidoc_proxy", __name__)

@bp.route("/zidoc", methods=["GET"])
@require_api_key
@log_request_response
def proxy_zidoc():
    # status, result = call_zidoc_api()
    # return jsonify({"status": status, "result": result}), status
    log("--- zidoc Request Data Received: ---")
    print("Headers:", request.headers)
    print("Query Params:", request.args)
    isflat = request.args.get("isflat", "false").lower() == "true"
    status, result = call_zidoc_api(flat=isflat)
    # return jsonify(result), status
    return Response(
        json.dumps(result, sort_keys=False),
        status=status,
        content_type="application/json"
    )