from flask import Blueprint, request, jsonify
from app.mail_api.service.mailer import try_mailersend, try_ses, try_mailersend_sdk
from app.utils.decorators import log_request_response
from app.utils.logger import log, get_log_context

bp = Blueprint("mail_send", __name__)

@bp.route("/send-email", methods=["POST"])
@log_request_response
def send_email():
    data = request.get_json()
    getlogs = data.get("getlogs", False)

    subject = data.get("subject")
    body = data.get("body")
    html_body = data.get("html_body")
    to = data.get("to")
    attachment = data.get("attachment_base64", None)
    attachment_name = data.get("attachment_name", "attachment.pdf")

    if try_mailersend(to, subject, body, html_body, attachment, attachment_name):
        return jsonify({"status": "success", "method": "mailersend", "logs": get_log_context() if getlogs else []}), 200
    elif try_mailersend_sdk(to, subject, body, html_body, attachment, attachment_name):
        return jsonify({"status": "success", "method": "mailersend_sdk", "logs": get_log_context() if getlogs else []}), 200
    elif try_ses(to, subject, body, html_body, attachment, attachment_name):
        return jsonify({"status": "success", "method": "aws_ses", "logs": get_log_context() if getlogs else []}), 200
    else:
        return jsonify({
            "status": "failure",
            "log": "All methods failed",
            "logs": get_log_context() if getlogs else None
        }), 500