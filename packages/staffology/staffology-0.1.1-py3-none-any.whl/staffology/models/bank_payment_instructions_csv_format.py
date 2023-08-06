from enum import Enum


class BankPaymentInstructionsCsvFormat(str, Enum):
    STANDARDCSV = "StandardCsv"
    TELLEROO = "Telleroo"
    BARCLAYSBACS = "BarclaysBacs"
    SANTANDERBACS = "SantanderBacs"
    SIF = "Sif"
    REVOLUT = "Revolut"
    STANDARD18FASTERPAYMENTS = "Standard18FasterPayments"
    STANDARD18BACS = "Standard18Bacs"
    BANKLINE = "Bankline"
    BANKLINEBULK = "BanklineBulk"
    STANDARDCSVBACS = "StandardCsvBacs"
    LLOYDSMULTIPLESTANDARDCSVBACS = "LloydsMultipleStandardCsvBacs"
    LLOYDSV11CSVBACS = "LloydsV11CsvBacs"
    COOPBULKCSVBACS = "CoOpBulkCsvBacs"
    COOPFASTERPAYMENTSCSV = "CoOpFasterPaymentsCsv"

    def __str__(self) -> str:
        return str(self.value)
