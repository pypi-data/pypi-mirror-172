from enum import Enum


class AeExclusionCode(str, Enum):
    NOTKNOWN = "NotKnown"
    NOTAWORKER = "NotAWorker"
    NOTWORKINGINUK = "NotWorkingInUk"
    NOORDINARILYWORKINGINUK = "NoOrdinarilyWorkingInUk"
    OUTSIDEOFAGERANGE = "OutsideOfAgeRange"
    SINGLEEMPLOYEE = "SingleEmployee"
    CEASEDACTIVEMEMBERSHIPINPAST12MO = "CeasedActiveMembershipInPast12Mo"
    CEASEDACTIVEMEMBERSHIP = "CeasedActiveMembership"
    RECEIVEDWULSINPAST12MO = "ReceivedWulsInPast12Mo"
    RECEIVEDWULS = "ReceivedWuls"
    LEAVING = "Leaving"
    TAXPROTECTION = "TaxProtection"
    CISSUBCONTRACTOR = "CisSubContractor"

    def __str__(self) -> str:
        return str(self.value)
