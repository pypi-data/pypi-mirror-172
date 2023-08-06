from enum import Enum


class EmployerTemplateType(str, Enum):
    PAYSLIPEMAIL = "PayslipEmail"
    AUTOENROLMENT_ENROLLED = "AutoEnrolment_Enrolled"
    AUTOENROLMENT_ENROLLED_NETPAY = "AutoEnrolment_Enrolled_NetPay"
    AUTOENROLMENT_NOTENROLLED = "AutoEnrolment_NotEnrolled"
    AUTOENROLMENT_INSERT = "AutoEnrolment_Insert"
    CISSTATEMENTEMAIL = "CisStatementEmail"
    PAYRUNSUMMARY = "PayrunSummary"
    PAYSLIPSUNEMAILED = "PayslipsUnemailed"
    PAYRUNAUTOEMAIL = "PayrunAutoEmail"
    P60EMAIL = "P60Email"
    ANNUALCISSTATEMENTEMAIL = "AnnualCisStatementEmail"
    P45EMAIL = "P45Email"
    AUTOENROLMENT_POSTPONED = "AutoEnrolment_Postponed"
    AUTOENROLMENT_REENROLLED = "AutoEnrolment_ReEnrolled"

    def __str__(self) -> str:
        return str(self.value)
