import os
from email.message import EmailMessage

import aiosmtplib

SMTP_SERVER_ADDRESS = os.getenv('SMTP_SERVER_ADDRESS', 'smtp.gmail.com')
SMTP_SERVER_PORT = os.getenv('SMTP_SERVER_PORT', 587)
SMTP_SERVER_EMAIL = os.getenv('SMTP_SERVER_EMAIL')
SMTP_SERVER_PASSWORD = os.getenv('SMTP_SERVER_PASSWORD')

#TODO: Use a queueing system like RabbitMQ or Redis to send emails in the background
class EmailService:
    def __init__(self):
        self.server = aiosmtplib.SMTP(
            hostname=SMTP_SERVER_ADDRESS,
            port=SMTP_SERVER_PORT,
            username=SMTP_SERVER_EMAIL,
            password=SMTP_SERVER_PASSWORD,
        )

    async def send_email(
        self,
        recipient_email,
        subject,
        body,
        sender_email=SMTP_SERVER_EMAIL,
    ):
        await self.server.connect()

        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg.set_content(body)

        await self.server.send_message(msg)
        await self.server.quit()
