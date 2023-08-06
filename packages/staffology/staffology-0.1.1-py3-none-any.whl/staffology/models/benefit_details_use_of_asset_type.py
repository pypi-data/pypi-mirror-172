from enum import Enum


class BenefitDetailsUseOfAssetType(str, Enum):
    OTHER = "Other"
    MULTIPLE = "Multiple"
    CORPORATEHOSPITALITY = "CorporateHospitality"
    BOAT = "Boat"
    AIRCRAFT = "Aircraft"
    TIMESHAREACCOMMODATION = "TimeshareAccommodation"
    HOLIDAYACCOMMODATION = "HolidayAccommodation"

    def __str__(self) -> str:
        return str(self.value)
