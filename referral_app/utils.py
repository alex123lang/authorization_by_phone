import os
from smsaero import SmsAero, SmsAeroException
from dotenv import load_dotenv

load_dotenv()

SMSAERO_EMAIL = os.getenv("SMSAERO_EMAIL")
SMSAERO_API_KEY = os.getenv("SMSAERO_API_KEY")


def send_sms(phone: int, message: str) -> dict:
    """
    Sends an SMS message using SmsAero.

    Parameters:
    phone (int): The phone number to which the SMS message will be sent.
    message (str): The content of the SMS message to be sent.

    Returns:
    dict: A dictionary containing the response from the SmsAero API.
    """
    try:
        api = SmsAero(SMSAERO_EMAIL, SMSAERO_API_KEY)
        response = api.send_sms(phone, message)
        return response
    except SmsAeroException as e:
        # Можно добавить обработку ошибок и логирование
        return {"error": str(e)}
