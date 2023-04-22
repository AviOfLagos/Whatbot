import os
from twilio.rest import Client

class WhatsApp:
    def __init__(self):
        self.account_sid = os.environ.get("ACbdd3846b46fa821716d62715c37f1515")
        self.auth_token = os.environ.get("22076a3e03f69fcdef6e393e56f0b6d6")
        self.client = Client(self.account_sid, self.auth_token)

    def send_message(self, message_body, recipient):
        message = self.client.messages.create(
            body=message_body,
            from_=f"whatsapp:{os.environ.get(+15077105339)}",
            to=f"whatsapp:{recipient}"
        )

        return message.sid
