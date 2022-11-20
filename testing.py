from afip import WSN
import json
import datetime

WSDL_WSFEV1 = "https://wswhomo.afip.gov.ar/wsfev1/service.asmx?WSDL"
NAME_WSFEV1 = "wsfe"

wsfev1 = WSN(WSDL_WSFEV1, NAME_WSFEV1)

with open("ticket.json", "r") as f:
    ticket = json.load(f)
wsfev1.login(ticket)

today = datetime.date.today().strftime("%Y%m%d")

Auth = dict(
    Token=wsfev1.token,
    Sign=wsfev1.sign,
    Cuit="20350482696",
)


def FECompUltimoAutorizado():
    return wsfev1.service.FECompUltimoAutorizado(
        Auth=Auth,
        PtoVta=1,
        CbteTipo=11,
    )


def FEParamGetTiposCbte():
    print(wsfev1.service.FEParamGetTiposCbte(Auth=Auth))


def FEParamGetTiposMonedas():
    print(wsfev1.service.FEParamGetTiposMonedas(Auth=Auth))


def FEParamGetPtosVenta():
    print(wsfev1.service.FEParamGetPtosVenta(Auth=Auth))


def FEParamGetTiposConcepto():
    print(wsfev1.service.FEParamGetTiposConcepto(Auth=Auth))


def FEParamGetTiposDoc():
    print(wsfev1.service.FEParamGetTiposDoc(Auth=Auth))


def FEParamGetTiposPaises():
    print(wsfev1.service.FEParamGetTiposPaises(Auth=Auth))


comprobante = FECompUltimoAutorizado()["CbteNro"] + 1


def FECAESolicitar():
    r = wsfev1.service.FECAESolicitar(
        Auth=Auth,
        FeCAEReq=dict(
            FeCabReq=dict(
                CantReg=1,
                PtoVta=1,
                CbteTipo=11,
            ),
            FeDetReq=dict(
                FECAEDetRequest=dict(
                    Concepto=2,
                    DocTipo=99,
                    DocNro=0,
                    CbteDesde=comprobante,
                    CbteHasta=comprobante,
                    CbteFch=today,
                    ImpTotal=0,
                    ImpTotConc=0,
                    ImpNeto=0,
                    ImpOpEx=0,
                    ImpIVA=0,
                    ImpTrib=0,
                    FchServDesde="20220901",
                    FchServHasta="20220930",
                    FchVtoPago="20221010",
                    MonId="PES",
                    MonCotiz=1,
                ),
            ),
        ),
    )
    print(r)


# FEParamGetTiposDoc()
FECAESolicitar()
# FEParamGetTiposCbte()
# FECAESolicitar()
