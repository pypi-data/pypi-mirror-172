from enum import Enum


class UserCategory(str, Enum):
    ACTIVETRIALIST = "ActiveTrialist"
    AGEDACTIVETRIALIST = "AgedActiveTrialist"
    LAPSEDTRIALIST = "LapsedTrialist"
    ACTIVECUSTOMER = "ActiveCustomer"
    LAPSEDCUSTOMER = "LapsedCustomer"
    SUBUSER = "SubUser"
    AGEDACTIVETRIALISTANDSUBUSER = "AgedActiveTrialistAndSubUser"
    INTERNALUSER = "InternalUser"

    def __str__(self) -> str:
        return str(self.value)
