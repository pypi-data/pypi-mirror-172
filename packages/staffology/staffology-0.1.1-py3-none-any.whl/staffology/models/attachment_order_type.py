from enum import Enum


class AttachmentOrderType(str, Enum):
    AEOP = "AeoP"
    AEO = "Aeo"
    CSA = "Csa"
    CSA2012 = "Csa2012"
    DEO = "Deo"
    AEONP = "AeoNp"
    CCPRE92 = "CcPre92"
    CCPOST92 = "CcPost92"
    CTAEO = "Ctaeo"
    MCAEO = "Mcaeo"
    EA = "Ea"
    CMA = "Cma"
    CAO = "Cao"
    ISD = "Isd"
    EA2006 = "Ea2006"
    CAPS = "Caps"
    DEA = "Dea"
    DEAHIGHER = "DeaHigher"
    DEAFIXED = "DeaFixed"
    CTAEOWALES = "CtaeoWales"

    def __str__(self) -> str:
        return str(self.value)
