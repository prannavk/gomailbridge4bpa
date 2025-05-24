from flask import Blueprint, request, jsonify
from app.mail_api.service.mailer import try_ses, try_mailersend_sdk, try_maileroo
from app.utils.decorators import log_request_response
from app.utils.logger import log, get_log_context

bp = Blueprint("mail_send", __name__)


def handle_input_recipient_list(input_to_list = []):
    verdict = "Ok"
    to_actual = []
    if input_to_list is None or input_to_list is []:
        verdict = "OOPS"
    else:
        to_actual = [input_to_list[0]]
        to_ask_to_try_again = input_to_list[1:]
        if not to_ask_to_try_again:
            verdict += "Sent"
        else:
            verdict += "Sent to the first recipient only. Please try sending again seperately for the rest of the recipients as presently unable to send to multiple recipients (to addresses) at once due to a temporary resource limitation on the backend."
    return (to_actual, verdict)

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

    to_send_to, verdict = handle_input_recipient_list(to)

    # Validation
    if verdict == "OOPS":
        return jsonify({"error":"There is an issue with the recipients list sent, please try again"}), 400
    if subject == "" or body == "" or html_body == "":
        return jsonify({"error":"Please send all the required data to send as there seems to be a missing subject, body or html_body"}), 400    
    
    # Calling service logic
    # if try_mailersend(to_send_to, subject, body, html_body, attachment, attachment_name): -> Commented as its always failing
    #     return jsonify({"status": "success", "method": "mailersend", "logs": get_log_context() if getlogs else [], "comment":verdict}), 200
    if try_mailersend_sdk(to_send_to, subject, body, html_body, attachment, attachment_name):
        return jsonify({"status": "success", "method": "mailersend_sdk", "logs": get_log_context() if getlogs else [], "comment":verdict}), 200
    elif try_maileroo(to_send_to, subject, body, html_body, attachment, attachment_name):
        return jsonify({"status": "success", "method": "maileroo", "logs": get_log_context() if getlogs else [], "comment":verdict}), 200
    # elif try_ses(to_send_to, subject, body, html_body, attachment, attachment_name):
    #     return jsonify({"status": "success", "method": "aws_ses", "logs": get_log_context() if getlogs else [], "comment":verdict}), 200
    else:
        return jsonify({
            "status": "failure",
            "log": "All methods failed",
            "logs": get_log_context() if getlogs else None,
            "comment": "If the Email Payload was correct, but the send has still failed, then please be patient, as the developer(s) will fix it soon and you will not see this again"
        }), 500

    