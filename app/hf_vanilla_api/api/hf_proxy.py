# FILE: app/hf_vanilla_api/api/hf_proxy.py

from flask import Blueprint, request, jsonify
from app.zidoc_api.hf_service import hf_service
from app.utils.auth import require_api_key
from app.utils.decorators import log_request_response
from app.utils.logger import log

hf_bp = Blueprint("hf_proxy", __name__)

@hf_bp.route("/hfchat", methods=["POST"])
@require_api_key
@log_request_response
def hf_inference_chat():
    data = request.get_json()
    prompt = data.get("prompt")
    log(f"prompt received : {prompt}")
    if not prompt:
        return jsonify({"error": "Prompt not provided"}), 400

    try:
        response = hf_service.freestyle_text_gen(prompt)
        log(f"hf prompt response: {response}")
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
