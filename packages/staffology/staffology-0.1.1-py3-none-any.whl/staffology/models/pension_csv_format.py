from enum import Enum


class PensionCsvFormat(str, Enum):
    PAPDIS = "Papdis"
    NEST = "Nest"
    NOWPENSIONS = "NowPensions"
    TEACHERSPENSIONMDC = "TeachersPensionMdc"
    TEACHERSPENSIONMCR = "TeachersPensionMcr"

    def __str__(self) -> str:
        return str(self.value)
