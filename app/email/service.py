from fastapi_mail import FastMail, MessageSchema, MessageType
from .config import conf


async def send_email(
    recipients: list[str],
    subject: str,
    body: str,
):
    try:
        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            body=body,
            subtype=MessageType.html,
        )

        fm = FastMail(conf)
        await fm.send_message(message)

    except Exception as e:
        print(f"Email sending failed: {e}")