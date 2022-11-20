from datetime import datetime, timedelta, timezone
import xmltodict
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import pkcs7
from zeep import Client

DEFAULT_TTL = 24 * 60 * 60
DEFAULT_OFFSET = 5 * 60


class WSAA(Client):
    def __init__(
        self,
        wsdl: str,
        cert: bytes,
        key: bytes,
        password: bytes = None,
        source: str = None,
        destination: str = None,
        **kwargs
    ):

        self.cert = x509.load_pem_x509_certificate(cert)

        self.key = serialization.load_pem_private_key(
            key, password
        )

        self.source = source

        self.destination = destination

        super().__init__(wsdl, **kwargs)

    def _prepare_tx(self, service, ttl, offset):
        now = datetime.now(timezone.utc)
        timestamp = int(now.timestamp())
        created_at = (now - timedelta(seconds=offset)).astimezone()
        expires_at = (now + timedelta(seconds=ttl)).astimezone()

        header = {
            "uniqueId": timestamp,
            "generationTime": created_at.isoformat(),
            "expirationTime": expires_at.isoformat(),
        }

        if self.source and self.destination:
            header["source"] = self.source
            header["destination"] = self.destination

        ticket = {
            "loginTicketRequest": {
                "header": header,
                "service": service,
            }
        }
        return xmltodict.unparse(ticket)

    def _sign_tx(self, tx):

        options = []

        cms = (
            pkcs7.PKCS7SignatureBuilder()
            .set_data(tx.encode())
            .add_signer(self.cert, self.key, hashes.SHA256())
            .sign(serialization.Encoding.PEM, options)
        )

        cms = cms.decode().splitlines()
        cms.remove("-----BEGIN PKCS7-----")
        cms.remove("-----END PKCS7-----")
        cms = "".join(cms)

        return cms

    def authorize(
        self, service: str, ttl: int = DEFAULT_TTL, offset: str = DEFAULT_OFFSET
    ):
        trx = self._prepare_tx(service, ttl, offset)
        cms = self._sign_tx(trx)
        r = self.service["loginCms"](cms)
        return xmltodict.parse(r)
