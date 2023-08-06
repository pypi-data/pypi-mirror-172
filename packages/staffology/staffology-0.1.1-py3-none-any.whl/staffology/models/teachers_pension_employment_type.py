from enum import Enum


class TeachersPensionEmploymentType(str, Enum):
    FULLTIME = "FullTime"
    PARTTIMEREGULAR = "PartTimeRegular"
    IRREGULARPARTTIME = "IrregularPartTime"
    IRREGULARPARTTIME_IN = "IrregularPartTime_In"

    def __str__(self) -> str:
        return str(self.value)
