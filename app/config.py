import os
from dotenv import load_dotenv

load_dotenv()

# MAILERSEND
MAILERSEND_BASEURL = "https://api.mailersend.com/v1/"

MAILERSEND_FROM_NAME1 = "PranavWeb1"
MAILERSEND_FROM_NAME2 = "MailSendBotKKP"
MAILERSEND_FROM_NAME = MAILERSEND_FROM_NAME2

MAILERSEND_ACCOUNTS = [
    {
        "acc_mail_id" : os.getenv("MAILERSEND_FROM2", ""),
        "acc_token" : os.getenv("MAILERSEND_API_TOKEN2")
    },
    {
        "acc_mail_id" : os.getenv("MAILERSEND_FROM", ""),
        "acc_token" : os.getenv("MAILERSEND_API_TOKEN")
    }
]

# MAILEROO
MAILEROO_KEY = os.getenv("MAILEROO_API_KEY", "xxxxx")
MAILEROO_FROM_DOMAINMAIL = "mailsendbotkkp@943da8e672c34539.maileroo.org"


# AWS SES
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

SES_FROM_LIST = os.getenv("SES_FROM_LIST", "kkpranav3@outlook.com,703395151@genpact.com,krishnapk808@gmail.com").split(",")

# Port Config
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))

# ZIDOC Proxy Vars
ZIDOC_TOKEN_URL = os.getenv("ZIDOC_TOKEN_URL")
ZIDOC_CLIENT_ID = os.getenv("ZIDOC_CLIENT_ID")
ZIDOC_CLIENT_SECRET = os.getenv("ZIDOC_CLIENT_SECRET")
ZIDOC_SCOPE = os.getenv("ZIDOC_SCOPE", "")  # if required
ZIDOC_DATA_API_URL = os.getenv("ZIDOC_DATA_API_URL")

