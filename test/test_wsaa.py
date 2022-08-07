from afip import WSAA
from decouple import config
from base64 import b64decode

TESTING_URL = "https://wsaahomo.afip.gov.ar/ws/services/LoginCms?WSDL"
AFIP_CERT = config('AFIP_CERT', cast=b64decode).decode()
AFIP_PKEY = config('AFIP_PKEY', cast=b64decode).decode()


def test_login():
    wsaa = WSAA(
        TESTING_URL,
        AFIP_CERT,
        AFIP_PKEY,
    )

    ticket = wsaa.authorize("ws_sr_padron_a5", 30)

    print(ticket, flush=True)

test_login()