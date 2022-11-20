from afip import WSN
from pprint import pprint as print
import pytest
import json

WSDL_WSFEV1 = "https://wswhomo.afip.gov.ar/wsfev1/service.asmx?WSDL"
NAME_WSFEV1 = "wsfe"

STATUS = "FEDummy"
COMPROBANTES = "FEParamGetTiposCbte"


@pytest.fixture
def wsfev1():
    return WSN(WSDL_WSFEV1, NAME_WSFEV1)


def test_status(wsfev1):
    wsfev1.service[STATUS]()


def test_comprobante(wsaa, wsfev1):
    ticket = wsaa.authorize(wsfev1.name)
    with open("ticket.json", "w+") as f:
        json.dump(ticket, f)
    wsfev1.login(ticket)
    wsfev1.service[COMPROBANTES](
        **{
            "Auth": {
                "Token": wsfev1.token,
                "Sign": wsfev1.sign,
                "Cuit": "20350482696",
            }
        }
    )


