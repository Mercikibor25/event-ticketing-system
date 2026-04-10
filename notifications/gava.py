import requests
from django.conf import settings

def send_sms(phone_number, message):
    """Send SMS via GAVA API"""

    # Format phone number — must start with 254
    if phone_number.startswith('0'):
        phone_number = '254' + phone_number[1:]
    elif phone_number.startswith('+'):
        phone_number = phone_number[1:]

    url = 'https://api.gavaconnect.com/v1/sms/send'

    payload = {
        'api_key': settings.GAVA_API_KEY,
        'sender_id': settings.GAVA_SENDER_ID,
        'phone': phone_number,
        'message': message,
    }

    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        return {'error': str(e)}