from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import pkcs7
from zeep import Client
from zeep.helpers import serialize_object
from zeep.exceptions import Fault
from datetime import datetime, timezone, timedelta

DEFAULT_TTL = 24 * 60 * 60
DEFAULT_OFFSET = 5 * 60

LOGIN_TICKET_REQUEST = '''<?xml version="1.0" encoding="UTF-8" ?>
<loginTicketRequest version="1.0">
  <header>
    {source}
    {destination}
    <uniqueId>{unique_id}</uniqueId>
    <generationTime>{created_at}</generationTime>
    <expirationTime>{expires_at}</expirationTime>
  </header>
  <service>{service}</service>
</loginTicketRequest>'''

SOURCE_FIELD = '<source>{}</source>'
DESTINATION_FIELD = '<destination>{}</destination>'


class WSAA():

    def __init__(self, url, cert, key, password=None, source=None, destination=None):

        self.cert = x509.load_pem_x509_certificate(cert.encode())

        self.key = serialization.load_pem_private_key(key.encode(), password)

        self.client = Client(url)

        self.source = source

        self.destination = destination

    def _prepare_tx(self, service, ttl=DEFAULT_TTL, offset=DEFAULT_OFFSET):
        now = datetime.now(timezone.utc)
        timestamp = int(now.timestamp())
        created_at = (now - timedelta(seconds=offset)).astimezone()
        expires_at = (now + timedelta(seconds=ttl)).astimezone()

        source = SOURCE_FIELD.format(self.source) if self.source else ''
        destination = DESTINATION_FIELD.format(
            self.destination) if self.destination else ''

        ticket_options = {
            'unique_id': timestamp,
            'created_at': created_at.isoformat(),
            'expires_at': expires_at.isoformat(),
            'service': service,
            'source': source,
            'destination': destination,
        }

        return LOGIN_TICKET_REQUEST.format(**ticket_options)

    def _sign_tx(self, tx):
        
        options = []

        cms = pkcs7.PKCS7SignatureBuilder().set_data(
            tx.encode()
        ).add_signer(
            self.cert, self.key, hashes.SHA256()
        ).sign(
            serialization.Encoding.PEM, options
        )

        cms = cms.decode().splitlines()
        cms.remove('-----BEGIN PKCS7-----')
        cms.remove('-----END PKCS7-----')
        cms = ''.join(cms)

        return cms

    def authorize(self, service):
        trx = self._prepare_tx(service)
        cms = self._sign_tx(trx)

        try:
            xml = self.client.service['loginCms'](cms)
            obj = serialize_object(xml)
            print(type(obj))
            return obj
        except Fault as e:
            return(e.__dict__)

