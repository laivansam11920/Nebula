import resend
from os import getenv

resend.api_key = str(getenv("RESEND_API_KEY"))

