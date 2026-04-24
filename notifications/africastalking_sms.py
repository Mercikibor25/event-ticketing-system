import africastalking
from django.conf import settings

def initialize_africastalking():
    africastalking.initialize(
        settings.AFRICASTALKING_USERNAME,
        settings.AFRICASTALKING_API_KEY
    )
    return africastalking.SMS

def send_sms(phone_number, message):
    """Send SMS via Africa's Talking"""
    try:
        # Format phone number
        if phone_number.startswith('0'):
            phone_number = '+254' + phone_number[1:]
        elif phone_number.startswith('254'):
            phone_number = '+' + phone_number
        elif not phone_number.startswith('+'):
            phone_number = '+254' + phone_number

        sms = initialize_africastalking()
        response = sms.send(message, [phone_number])
        return {'success': True, 'response': response}

    except Exception as e:
        return {'success': False, 'error': str(e)}