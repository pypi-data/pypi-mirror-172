from enum import Enum


class ExternalDataProviderId(str, Enum):
    SMARTPENSION_EMPLOYER = "SmartPension_Employer"
    SMARTPENSION_ADVISER = "SmartPension_Adviser"
    PEOPLESPENSION = "PeoplesPension"
    XERO = "Xero"
    QBO = "Qbo"
    SAGE = "Sage"
    NEST = "Nest"
    CASHPLUS = "Cashplus"
    BREATHEHR = "BreatheHr"
    KASHFLOW = "KashFlow"
    RECKON = "Reckon"
    FREEAGENT = "FreeAgent"
    FREEAGENTPM = "FreeAgentPm"
    MODULR = "Modulr"
    SQUARE = "Square"
    CEZANNE = "Cezanne"
    CIPHR = "Ciphr"
    TELLEROO = "Telleroo"
    WEWORKED = "WeWorked"
    ROTACLOUD = "RotaCloud"
    QUINYX = "Quinyx"
    CSOD = "Csod"
    PLANDAY = "Planday"
    STARLING = "Starling"
    DEPUTY = "Deputy"
    BOTTOMLINE = "Bottomline"
    TWINFIELD = "Twinfield"
    MYEPAYWINDOW = "MyePayWindow"
    IFINANCE = "IFinance"
    ACCOUNTSIQ = "AccountsIQ"

    def __str__(self) -> str:
        return str(self.value)
