from .models import Notification

def send_ticket_confirmation(user, ticket):
    """Log ticket confirmation notification"""
    message = (
        f"Hello {user.username}! Your ticket has been booked.\n"
        f"Event: {ticket.event.title}\n"
        f"Date: {ticket.event.date.strftime('%d %b %Y %H:%M')}\n"
        f"Venue: {ticket.event.venue}\n"
        f"Ticket ID: {ticket.ticket_id}\n"
        f"Show this SMS or QR code at the gate."
    )
    Notification.objects.create(
        user=user,
        notification_type='ticket_confirmation',
        message=message,
        phone_number=user.phone_number,
        status='pending'
    )
    return {'message': 'Notification logged'}


def send_payment_confirmation(user, payment):
    """Log payment confirmation notification"""
    message = (
        f"Hello {user.username}! Payment confirmed.\n"
        f"Amount: KES {payment.amount}\n"
        f"Event: {payment.ticket.event.title}\n"
        f"M-Pesa Receipt: {payment.mpesa_receipt_number}\n"
        f"Thank you!"
    )
    Notification.objects.create(
        user=user,
        notification_type='payment_confirmation',
        message=message,
        phone_number=user.phone_number,
        status='pending'
    )
    return {'message': 'Notification logged'}


def send_event_reminder(user, ticket):
    """Log event reminder notification"""
    message = (
        f"Hello {user.username}! Reminder:\n"
        f"'{ticket.event.title}' is tomorrow!\n"
        f"Date: {ticket.event.date.strftime('%d %b %Y %H:%M')}\n"
        f"Venue: {ticket.event.venue}\n"
        f"Ticket ID: {ticket.ticket_id}\n"
        f"See you there!"
    )
    Notification.objects.create(
        user=user,
        notification_type='event_reminder',
        message=message,
        phone_number=user.phone_number,
        status='pending'
    )
    return {'message': 'Notification logged'}


def send_event_update(user, event, update_message):
    """Log event update notification"""
    message = (
        f"Hello {user.username}! Update for '{event.title}':\n"
        f"{update_message}\n"
        f"Date: {event.date.strftime('%d %b %Y %H:%M')}\n"
        f"Venue: {event.venue}"
    )
    Notification.objects.create(
        user=user,
        notification_type='event_update',
        message=message,
        phone_number=user.phone_number,
        status='pending'
    )
    return {'message': 'Notification logged'}