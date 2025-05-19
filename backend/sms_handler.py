import os
from twilio.rest import Client


class SMSHandler:
    def __init__(self):
        self.acc_sid = os.getenv('ACCOUNT_SID')
        self.auth_token = os.getenv('AUTH_TOKEN')

        if not self.acc_sid or not self.auth_token:
            raise ValueError("Environment variables ACCOUNT_SID and/or AUTH_TOKEN not set.")

        print("Initializing Twilio Client...")
        self.client = Client(self.acc_sid, self.auth_token)
        print("Twilio Client Initialized.")

        # Optional: validate with a test request or flag
        self.sender = "+13022468290"  # From number you registered
        self.recipient = "+251707355385"

    def send_sms(self, message):
        try:
            print("Sending SMS...")
            message = self.client.messages.create(
                to=self.recipient,
                from_=self.sender,
                body=message
            )
            print(f"SMS sent with SID: {message.sid}")
        except Exception as e:
            print(f"❌ Failed to send SMS: {e}")
