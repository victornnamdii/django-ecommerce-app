import sys
from os import getenv

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment

client_id = getenv("CLIENT_ID")
client_secret = getenv("PP_SECRET_ID")


class PayPalClient:
    def __init__(self):
        self.client_id = client_id
        self.client_secret = client_secret
        self.environment = SandboxEnvironment(
            client_id=self.client_id, client_secret=self.client_secret
        )
        self.client = PayPalHttpClient(self.environment)
