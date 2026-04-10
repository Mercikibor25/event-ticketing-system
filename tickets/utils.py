import qrcode
import os
from django.conf import settings
from io import BytesIO
from django.core.files import File

def generate_qr_code(ticket):
    qr_data = (
        f"Ticket ID: {ticket.ticket_id}\n"
        f"Event: {ticket.event.title}\n"
        f"Date: {ticket.event.date.strftime('%Y-%m-%d %H:%M')}\n"
        f"Venue: {ticket.event.venue}\n"
        f"Attendee: {ticket.user.username}"
    )

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)

    filename = f"ticket_{ticket.ticket_id}.png"
    ticket.qr_code.save(filename, File(buffer), save=True)