from enum import Enum


class EntityType(str, Enum):
    NONE = "None"
    EMPLOYER = "Employer"
    EMPLOYEE = "Employee"
    PAYRUNENTRY = "PayRunEntry"
    PENSIONSCHEME = "PensionScheme"
    PAYCODE = "PayCode"
    NOTE = "Note"
    LEAVE = "Leave"
    BENEFITS = "Benefits"
    PENSION = "Pension"
    ATTACHMENTORDER = "AttachmentOrder"
    OPENINGBALANCES = "OpeningBalances"
    NICSUMMARY = "NicSummary"
    HMRCPAYMENT = "HmrcPayment"
    DPSNOTICE = "DpsNotice"
    USER = "User"
    SETTINGS = "Settings"
    PAYRUN = "PayRun"
    LOAN = "Loan"

    def __str__(self) -> str:
        return str(self.value)
