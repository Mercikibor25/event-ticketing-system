import requests
import base64
from datetime import datetime
from django.conf import settings

def get_mpesa_token():
    """Get OAuth access token from Daraja"""
    if settings.MPESA_ENV == 'sandbox':
        url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    else:
        url = 'https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    credentials = f"{settings.MPESA_CONSUMER_KEY}:{settings.MPESA_CONSUMER_SECRET}"
    encoded = base64.b64encode(credentials.encode()).decode('utf-8')

    response = requests.get(
        url,
        headers={'Authorization': f'Basic {encoded}'}
    )
    return response.json().get('access_token')


def generate_password():
    """Generate base64 encoded password for STK push"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    raw = f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}"
    encoded = base64.b64encode(raw.encode()).decode('utf-8')
    return encoded, timestamp


def stk_push(phone_number, amount, account_reference, description):
    """Initiate STK Push payment request"""
    if settings.MPESA_ENV == 'sandbox':
        url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    else:
        url = 'https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest'

    token = get_mpesa_token()
    password, timestamp = generate_password()

    # Format phone number — must start with 254
    if phone_number.startswith('0'):
        phone_number = '254' + phone_number[1:]
    elif phone_number.startswith('+'):
        phone_number = phone_number[1:]

    payload = {
        'BusinessShortCode': settings.MPESA_SHORTCODE,
        'Password': password,
        'Timestamp': timestamp,
        'TransactionType': 'CustomerPayBillOnline',
        'Amount': int(amount),
        'PartyA': phone_number,
        'PartyB': settings.MPESA_SHORTCODE,
        'PhoneNumber': phone_number,
        'CallBackURL': settings.MPESA_CALLBACK_URL,
        'AccountReference': account_reference,
        'TransactionDesc': description,
    }

    response = requests.post(
        url,
        json=payload,
        headers={'Authorization': f'Bearer {token}'}
    )
    return response.json()