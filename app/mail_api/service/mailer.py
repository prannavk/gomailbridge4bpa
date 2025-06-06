import requests
import boto3
from botocore.exceptions import ClientError
# from app.config import MAILERSEND_API_TOKEN, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
import io
import mimetypes
from mailersend import emails
import base64
from app.utils.logger import log
import json
from app.config import *
from app.utils.logger import log
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import tempfile
import os


@staticmethod
def build_attachment(base64_content, filename="attachment.pdf"):
    import base64
    part = MIMEApplication(base64.b64decode(base64_content))
    part.add_header('Content-Disposition', f'attachment; filename=\"{filename}\"')
    return part


# def try_mailersend(to_list, subject, body, html_body=None, attachment_base64=None, attachment_name="attachment.pdf"):
#     log("Attempting MailerSend HTTP API fallback with multiple accounts")
#     for i, acc in enumerate(MAILERSEND_ACCOUNTS, 1):
#         acc_token = acc["acc_token"]
#         acc_mail_id = acc["acc_mail_id"]
#         log(f"[{i}] Trying MailerSend account: {acc_mail_id}")
#         headers = {
#             "Authorization": f"Bearer {acc_token}",
#             "Content-Type": "application/json"
#         }
#         payload = {
#             "from": {"email": acc_mail_id, "name": "MAILSENDBOTPW1"},
#             "to": [{"email": email} for email in to_list],
#             "subject": subject,
#             "text": body
#         }
#         if html_body:
#             payload["html"] = html_body
#         if attachment_base64:
#             payload["attachments"] = [{
#                 "filename": attachment_name,
#                 "content": attachment_base64,
#                 "disposition": "attachment"
#             }]
#         try:
#             res = requests.post(MAILERSEND_BASEURL, json=payload, headers=headers)
#             res.raise_for_status()

#             if res.status_code == 202:
#                 log(f"[{i}] MailerSend email sent successfully with account: {acc_mail_id}")
#                 return True
#             else:
#                 log(f"[{i}] MailerSend failed: {res.status_code} {res.text}")

#         except requests.exceptions.RequestException as e:
#             log(f"[{i}] RequestException with account {acc_mail_id}: {e}")
#         except json.decoder.JSONDecodeError as e:
#             log(f"[{i}] JSONDecodeError with account {acc_mail_id}: {e}")
#         except Exception as e:
#             log(f"[{i}] Unexpected error with account {acc_mail_id}: {e}")

#     log("MailerSend failed to send email using all accounts")
#     return False

def get_mime_type_from_filename(filename: str) -> str:
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type if mime_type else "application/octet-stream"

def try_maileroo(to_list, subject, body, html_body=None, attachment_base64=None, attachment_name="attachment.pdf"):
    log("Attempting to send with Maileroo API........")
    url = "https://smtp.maileroo.com/send"
    headers = {
        "X-API-Key": MAILEROO_KEY
    }
    data = {
        "from": MAILEROO_FROM_DOMAINMAIL,
        "to": to_list,
        "subject": subject,
        "text": body,
        "html": body if html_body is None else html_body
    }
    
    temp_path = None

    try:
        files={}
        if attachment_base64 is not None and attachment_name:
            # Decode the base64 string into binary data
            attachment_data = base64.b64decode(attachment_base64)
            # Create a file-like object from the binary data
            # att_file = io.BytesIO(attachment_data)
            # att_file.name = attachment_name  # Set the filename attribute
            # Tempfile approach as above approach maynot work
            with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
                tmp_file.write(attachment_data)
                tmp_file.flush()
                temp_path = tmp_file.name

            files = {
                "attachments": (attachment_name, open(temp_path, "rb"), get_mime_type_from_filename(attachment_name))
            }
        
        response = requests.post(url, headers=headers, data=data, files=files if attachment_base64 is not None else None)
        response.raise_for_status()
        log("Email sent successfully.")        
        return True        
                    
    except requests.exceptions.HTTPError as http_err:
        log(f"HTTP error occurred: {http_err} - Response: {response.text}")        
        return False
    except Exception as err:
        log(f"An error occurred: {err}")        
        return False
    finally:
        # att_file.close()
        if files and "attachments" in files:
            files["attachments"][1].close()
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)  # Clean up temp file    


def try_mailersend_sdk(to_list, subject, body, html_body=None, attachment_base64=None, attachment_name="attachment.txt"):
    log("Attempting MailerSend SDK with multiple accounts........")

    for i, acc in enumerate(MAILERSEND_ACCOUNTS, 1):
        acc_token = acc["acc_token"]
        acc_mail_id = acc["acc_mail_id"]

        log(f"[{i}] Trying MailerSend account: {acc_mail_id}")

        try:
            mailer = emails.NewEmail(acc_token)
            mail_body = {}

            mailer.set_mail_from({
                "email": acc_mail_id,
                "name": "PranavWeb"
            }, mail_body)

            mailer.set_mail_to([{"email": email} for email in to_list], mail_body)
            mailer.set_subject(subject, mail_body)
            mailer.set_plaintext_content(body, mail_body)

            if html_body:
                mailer.set_html_content(html_body, mail_body)

            if attachment_base64:
                attachments = [{
                    "filename": attachment_name,
                    "content": attachment_base64,
                    "disposition": "attachment"
                }]
                mailer.set_attachments(attachments, mail_body)

            response = mailer.send(mail_body)

            if isinstance(response, str):
                try:
                    parsed = json.loads(response)
                    log(f"[{i}] SDK Response JSON: {parsed}")
                except Exception:
                    log(f"[{i}] SDK Raw Response: {response}")

            if str(response).startswith("2"):
                log(f"[{i}] MailerSend SDK email sent successfully with account: {acc_mail_id}")
                return True

            log(f"[{i}] MailerSend SDK returned unexpected response: {response}")

        except Exception as e:
            log(f"[{i}] SDK ERROR with account {acc_mail_id}: Exception: {e}")

    log("MailerSend SDK failed to send email using all accounts")
    return False



def try_ses(to_list, subject, body, html_body=None, attachment_base64=None, attachment_name="attachment.pdf"):
    log("Attempting to send email using AWS SES........")

    # Try with primary sender
    sender_ids = SES_FROM_LIST # ["primary@yourdomain.com", "fallback@yourdomain.com"]

    client = boto3.client(
        'ses',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )

    for sender_email in sender_ids:
        try:
            log(f"Trying with SES sender: {sender_email}")
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = sender_email
            msg['To'] = ", ".join(to_list)

            msg.attach(MIMEText(body, 'plain'))
            if html_body:
                msg.attach(MIMEText(html_body, 'html'))
            if attachment_base64:
                msg.attach(build_attachment(attachment_base64, attachment_name))

            client.send_raw_email(
                Source=sender_email,
                Destinations=to_list,
                RawMessage={'Data': msg.as_string()}
            )
            log(f"SES email sent successfully using {sender_email}")
            return True

        except ClientError as e:
            log(f"(ClientError) SES failed with {sender_email}: {e.response['Error']['Message']}")
            continue
        except Exception as e:
            log(f"(Unexpected Exception) SES failed: {e}")
            continue

    return False

