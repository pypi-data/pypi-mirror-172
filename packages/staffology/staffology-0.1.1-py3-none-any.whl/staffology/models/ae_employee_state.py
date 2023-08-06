from enum import Enum


class AeEmployeeState(str, Enum):
    AUTOMATIC = "Automatic"
    OPTOUT = "OptOut"
    OPTIN = "OptIn"
    VOLUNTARYJOINER = "VoluntaryJoiner"
    CONTRACTUALPENSION = "ContractualPension"
    CEASEDMEMBERSHIP = "CeasedMembership"
    LEAVER = "Leaver"
    EXCLUDED = "Excluded"
    ENROL = "Enrol"

    def __str__(self) -> str:
        return str(self.value)
