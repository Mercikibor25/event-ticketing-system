import requests
import base64
from django.conf import settings

def get_gava_token(consumer_key, secret_key):
    """Generate access token from GAVA/KRA API"""
    url = "https://sbx.kra.go.ke/v1/token/generate?grant_type=client_credentials"
    
    credentials = f"{consumer_key}:{secret_key}"
    encoded = base64.b64encode(credentials.encode()).decode('utf-8')
    
    response = requests.get(
        url,
        headers={'Authorization': f'Basic {encoded}'}
    )
    return response.json().get('access_token')


def verify_kra_pin_by_id(national_id, taxpayer_type='KE'):
    """Verify KRA PIN using National ID"""
    try:
        token = get_gava_token(
            settings.GAVA_PIN_CONSUMER_KEY,
            settings.GAVA_PIN_SECRET_KEY
        )

        url = "https://sbx.kra.go.ke/checker/v1/pin"

        response = requests.post(
            url,
            json={
                'TaxpayerType': taxpayer_type,
                'TaxpayerID': national_id
            },
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }
        )

        data = response.json()

        if 'TaxpayerPIN' in data:
            return {
                'valid': True,
                'kra_pin': data.get('TaxpayerPIN'),
                'taxpayer_name': data.get('TaxpayerName')
            }
        else:
            return {
                'valid': False,
                'error': data.get('ErrorMessage', 'Invalid National ID')
            }

    except Exception as e:
        return {
            'valid': False,
            'error': str(e)
        }


def verify_tax_compliance(kra_pin):
    """Verify Tax Compliance Certificate using KRA PIN"""
    try:
        token = get_gava_token(
            settings.GAVA_TCC_CONSUMER_KEY,
            settings.GAVA_TCC_SECRET_KEY
        )

        url = "https://sbx.kra.go.ke/checker/v1/tcc"

        response = requests.post(
            url,
            json={'TaxpayerPIN': kra_pin},
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }
        )

        data = response.json()

        if response.status_code == 200:
            return {
                'valid': True,
                'data': data
            }
        else:
            return {
                'valid': False,
                'error': data.get('ErrorMessage', 'Verification failed')
            }

    except Exception as e:
        return {
            'valid': False,
            'error': str(e)
        }