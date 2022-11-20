import pytest
from afip import WSAA
from base64 import b64decode
from decouple import config

WSDL_WSAA_HOMO = "https://wsaahomo.afip.gov.ar/ws/services/LoginCms?WSDL"
AFIP_CERT = config("AFIP_CERT", cast=b64decode)
AFIP_PKEY = config("AFIP_PKEY", cast=b64decode)


@pytest.fixture
def wsaa():
    return WSAA(
        WSDL_WSAA_HOMO,
        AFIP_CERT,
        AFIP_PKEY,
    )
