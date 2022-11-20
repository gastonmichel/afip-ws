from zeep import Client
from datetime import datetime


class WSN(Client):
    def __init__(self, wsdl: str, name: str, **kwargs):
        self.name = name
        super().__init__(wsdl, **kwargs)

    def login(self, ticket):
        self.expires_at = datetime.fromisoformat(
            ticket["loginTicketResponse"]["header"]["expirationTime"]
        )
        self.token = ticket["loginTicketResponse"]["credentials"]["token"]
        self.sign = ticket["loginTicketResponse"]["credentials"]["sign"]
