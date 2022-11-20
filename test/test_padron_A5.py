from afip import WSN
from pprint import pprint as print
import pytest

WSDL_PADRON_A5 = (
    "https://awshomo.afip.gov.ar/sr-padron/webservices/personaServiceA5?WSDL"
)
NAME_PADRON_A5 = "ws_sr_padron_a5"


STATUS = "dummy"
GET_PERSONA = "getPersona"

@pytest.fixture
def padronA5():
    return WSN(WSDL_PADRON_A5, NAME_PADRON_A5)


def test_status(padronA5):
    padronA5.service[STATUS]()


def test_getPersona(wsaa, padronA5):
    ticket = wsaa.authorize(padronA5.name)
    padronA5.login(ticket)
    print(ticket)
    padronA5.service[GET_PERSONA](
        **{
            "token": padronA5.token,
            "sign": padronA5.sign,
            "cuitRepresentada": "20350482696",
            "idPersona": "27255820422",
        }
    )
