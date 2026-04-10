from .gava import send_sms
from .models import Notification

def send_ticket_confirmation(user, ticket):
    """SMS sent after successful ticket booking"""
    message = (
        f"Hello {user.username}! Your ticket has been booked.\n"
        f"Event: {ticket.event.title}\n"
        f"Date: {ticket.event.date.strftime('%d %b %Y %H:%M')}\n"
        f"Venue: {ticket.event.venue}\n"
        f"Ticket ID: {ticket.ticket_id}\n"
        f"Show this SMS or QR code at the gate."
    )
    result = send_sms(user.phone_number, message)
    Notification.objects.create(
        user=user,
        notification_type='ticket_confirmation',
        message=message,
        phone_number=user.phone_number,
        status='sent' if not result.get('error') else 'failed'
    )
    return result


def send_payment_confirmation(user, payment):
    """SMS sent after successful M-Pesa payment"""
    message = (
        f"Hello {user.username}! Payment confirmed.\n"
        f"Amount: KES {payment.amount}\n"
        f"Event: {payment.ticket.event.title}\n"
        f"M-Pesa Receipt: {payment.mpesa_receipt_number}\n"
        f"Thank you!"
    )
    result = send_sms(user.phone_number, message)
    Notification.objects.create(
        user=user,
        notification_type='payment_confirmation',
        message=message,
        phone_number=user.phone_number,
        status='sent' if not result.get('error') else 'failed'
    )
    return result


def send_event_reminder(user, ticket):
    """SMS reminder sent before the event"""
    message = (
        f"Hello {user.username}! Reminder:\n"
        f"'{ticket.event.title}' is tomorrow!\n"
        f"Date: {ticket.event.date.strftime('%d %b %Y %H:%M')}\n"
        f"Venue: {ticket.event.venue}\n"
        f"Ticket ID: {ticket.ticket_id}\n"
        f"See you there!"
    )
    result = send_sms(user.phone_number, message)
    Notification.objects.create(
        user=user,
        notification_type='event_reminder',
        message=message,
        phone_number=user.phone_number,
        status='sent' if not result.get('error') else 'failed'
    )
    return result


def send_event_update(user, event, update_message):
    """SMS sent when event details change"""
    message = (
        f"Hello {user.username}! Update for '{event.title}':\n"
        f"{update_message}\n"
        f"Date: {event.date.strftime('%d %b %Y %H:%M')}\n"
        f"Venue: {event.venue}"
    )
    result = send_sms(user.phone_number, message)
    Notification.objects.create(
        user=user,
        notification_type='event_update',
        message=message,
        phone_number=user.phone_number,
        status='sent' if not result.get('error') else 'failed'
    )
    return result