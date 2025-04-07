from fastapi import BackgroundTasks
import aiosmtplib
from email.message import EmailMessage


SMTP_SERVER = "smtp.gmail.com"  # Replace with your SMTP server
SMTP_PORT = 465  #405 Usually 587 for TLS, 465 for SSL
SMTP_USERNAME = "priyanhari2303@gmail.com"  # Your email
SMTP_PASSWORD = "yivt hrjo owar ylsg"


async def send_email_notification(name:str, email:str):
    subject = "Verify Your Account"
    email_template = f"""
        Hi {name},

        Thank you for signing up! Please verify your email by clicking the link below:

        [Verify Email](https://example.com/verify?token=token)

        If you didn’t sign up, please ignore this email.

        Best regards,  
        Book Inventory app
        """

    message = EmailMessage()
    message["From"] = SMTP_USERNAME
    message["To"] = email
    message["Subject"] = subject
    message.set_content(email_template)

    # Connect to SMTP server and send email
    await aiosmtplib.send(
        message,
        hostname=SMTP_SERVER,
        port=SMTP_PORT,
        username=SMTP_USERNAME,
        password=SMTP_PASSWORD,
        start_tls=True,  # Use True for TLS, False for SSL
    )
    print(f"email sent to {name}")


async def confirm_email_status(name:str, email:str):
    subject = "Confirm email verify"
    email_template = f"""
            Hi {name},

            Please verify your email by clicking the link below:

            [Verify Email](https://example.com/verify?token=token)

            Best regards,  
            Book Inventory app
            """
    message = EmailMessage()
    message["From"] = SMTP_USERNAME
    message["To"] = email
    message["Subject"] = subject
    message.set_content(email_template)

    await aiosmtplib.send(
        message,
        hostname=SMTP_SERVER,
        port=SMTP_PORT,
        username=SMTP_USERNAME,
        password=SMTP_PASSWORD,
        start_tls=True,  # Use True for TLS, False for SSL
    )
    print(f"confirm email notification sent to {name}")
