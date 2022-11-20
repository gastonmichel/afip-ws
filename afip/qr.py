from base64 import b64encode
import json
import qrcode
import datetime


class QR:
    def __init__(
        self,
        url: str = "https://www.afip.gob.ar/fe/qr/ ",
        ver: int = 1,
    ) -> None:
        self.url = url
        self.ver = ver

    def generate(
        self,
        fecha: str = "2020-10-13",
        cuit: int = 30000000007,
        ptoVenta: int = 10,
        tipoCmp: int = 1,
        nroCmp: int = 94,
        importe: float = 12100,
        moneda: str = "DOL",
        ctz: float = 130,
        tipoDocRec: int = None,
        nroDocRec: int = None,
        tipoCodAut: str = "E",
        codAut: int = 70417054367476,
        **kwargs,
    ):
        cmp_base_64 = b64encode(json.dumps(kwargs))
        qr_url = f"{self.url}?p={cmp_base_64}"
        code = qrcode.QRCode()
        code.add_data(qr_url)