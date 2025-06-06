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
from app.zidoc_api.utils.stats2 import generate_idoc_analytics2_html_report, generate_idoc_analytics2_text_report
from app.zidoc_api.hf_service import hf_service
from app.utils.decorators import log_request_response
from app.utils.auth import require_api_key
from app.utils.logger import log, debug_bool
from app.config import ZIDOC_DATA_API_URL
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
        "odata.metadata":  ZIDOC_DATA_API_URL + "$metadata", # "https://example.com/zidoc/$metadata#ZIDOC",
        "value": idocs
    }
    return Response(json.dumps(response), status=200, content_type="application/json")


# @zidoc_bp.route("/zidocstats", methods=["GET"])
# @require_api_key
# @log_request_response
# def get_rawzidoc() -> Response:
#     """Endpoint handler for /zidocstats — only returns zidoc statistics and analytics/statistics string"""
#     log("Handling /zidocstats request")
#     idocs = get_flattened_idocs()
#     response = {}
#     try:
#         html_report = generate_idoc_analytics2_html_report(idoc_data=idocs)
#         text_report = generate_idoc_analytics2_text_report(idoc_data=idocs)
#         response["idocdataplain"] = text_report
#         response["idocdatahtml"] = html_report
#     except Exception as e:
#         # Need to Handle code here
#         pass
#     return Response(json.dumps(response), status=200, content_type="application/json")

@zidoc_bp.route("/zidocstats", methods=["GET"])
@require_api_key
@log_request_response
def get_zidocstats() -> Response:
    """Endpoint handler for /zidocstats — returns zidoc statistics and analytics/statistics string"""
    log("Handling /zidocstats request")
    
    try:
        # Get the iDoc data
        idocs = get_flattened_idocs()
        
        # Validate we have data before processing
        if not idocs:
            raise ValueError("No iDoc data available in the system")
            
        # Generate reports
        html_report = generate_idoc_analytics2_html_report(idoc_data=idocs)
        text_report = generate_idoc_analytics2_text_report(idoc_data=idocs)
        
        # Validate reports were generated properly
        if "No iDoc Data Available" in html_report or "No iDoc Data Available" in text_report:
            raise ValueError("Report generation failed - empty data detected")
        
        # Prepare successful response
        response = {
            "status": "success",
            "data": {
                "idocdataplain": text_report,
                "idocdatahtml": html_report
            }
        }
        return Response(
            json.dumps(response),
            status=200,
            content_type="application/json"
        )
        
    except ValueError as ve:
        # Handle business logic errors (no data, empty reports, etc.)
        error_response = {
            "status": "error",
            "message": str(ve),
            "error_type": "data_validation_error"
        }
        return Response(
            json.dumps(error_response),
            status=404,  # Not Found for no data
            content_type="application/json"
        )
        
    except Exception as e:
        # Handle unexpected errors
        log(f"Unexpected error in /zidocstats: {str(e)}", level="error")
        error_response = {
            "status": "error",
            "message": "An internal server error occurred while processing your request",
            "error_type": "server_error",
            "details": str(e) # if current_app.config.get('DEBUG') else None
        }
        return Response(
            json.dumps(error_response),
            status=500,
            content_type="application/json"
        )


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