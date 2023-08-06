from enum import Enum


class AutoPilotFinaliseTime(str, Enum):
    JUSTAFTERMIDNIGHT = "JustAfterMidnight"
    NINEAM = "NineAm"
    ONEPM = "OnePm"
    FOURPM = "FourPm"
    SIXPM = "SixPm"
    ELEVENPM = "ElevenPm"

    def __str__(self) -> str:
        return str(self.value)
