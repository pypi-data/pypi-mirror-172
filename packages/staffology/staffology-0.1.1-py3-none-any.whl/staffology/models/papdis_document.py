from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.papdis_message_function_code import PapdisMessageFunctionCode
from ..models.papdis_pension_provider import PapdisPensionProvider
from ..models.papdis_version import PapdisVersion
from ..models.report import Report
from ..models.tax_year import TaxYear
from ..types import UNSET, Unset

T = TypeVar("T", bound="PapdisDocument")


@attr.s(auto_attribs=True)
class PapdisDocument:
    """PAPDIS stands for 'Payroll and Pension Data Interface Standard'.
    It is an industry standard for exchanging data between payroll software and pension providers.
    Our system provides an export of data in this standard and these models are used to represent the data.
    Whilst the relevant reporting API endpoint can provide this data as a JSON entity, it is usually represented in CSV
    or XML format which our API also provides.

        Attributes:
            message_function_code (Union[Unset, PapdisMessageFunctionCode]):
            version (Union[Unset, PapdisVersion]):
            message_function_code_int (Union[Unset, int]): [readonly]
            pension_provider (Union[Unset, PapdisPensionProvider]):
            report (Union[Unset, Report]):
            tax_year (Union[Unset, TaxYear]):
    """

    message_function_code: Union[Unset, PapdisMessageFunctionCode] = UNSET
    version: Union[Unset, PapdisVersion] = UNSET
    message_function_code_int: Union[Unset, int] = UNSET
    pension_provider: Union[Unset, PapdisPensionProvider] = UNSET
    report: Union[Unset, Report] = UNSET
    tax_year: Union[Unset, TaxYear] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        message_function_code: Union[Unset, str] = UNSET
        if not isinstance(self.message_function_code, Unset):
            message_function_code = self.message_function_code.value

        version: Union[Unset, str] = UNSET
        if not isinstance(self.version, Unset):
            version = self.version.value

        message_function_code_int = self.message_function_code_int
        pension_provider: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pension_provider, Unset):
            pension_provider = self.pension_provider.to_dict()

        report: Union[Unset, str] = UNSET
        if not isinstance(self.report, Unset):
            report = self.report.value

        tax_year: Union[Unset, str] = UNSET
        if not isinstance(self.tax_year, Unset):
            tax_year = self.tax_year.value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if message_function_code is not UNSET:
            field_dict["messageFunctionCode"] = message_function_code
        if version is not UNSET:
            field_dict["version"] = version
        if message_function_code_int is not UNSET:
            field_dict["messageFunctionCodeInt"] = message_function_code_int
        if pension_provider is not UNSET:
            field_dict["pensionProvider"] = pension_provider
        if report is not UNSET:
            field_dict["report"] = report
        if tax_year is not UNSET:
            field_dict["taxYear"] = tax_year

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _message_function_code = d.pop("messageFunctionCode", UNSET)
        message_function_code: Union[Unset, PapdisMessageFunctionCode]
        if isinstance(_message_function_code, Unset):
            message_function_code = UNSET
        else:
            message_function_code = PapdisMessageFunctionCode(_message_function_code)

        _version = d.pop("version", UNSET)
        version: Union[Unset, PapdisVersion]
        if isinstance(_version, Unset):
            version = UNSET
        else:
            version = PapdisVersion(_version)

        message_function_code_int = d.pop("messageFunctionCodeInt", UNSET)

        _pension_provider = d.pop("pensionProvider", UNSET)
        pension_provider: Union[Unset, PapdisPensionProvider]
        if isinstance(_pension_provider, Unset):
            pension_provider = UNSET
        else:
            pension_provider = PapdisPensionProvider.from_dict(_pension_provider)

        _report = d.pop("report", UNSET)
        report: Union[Unset, Report]
        if isinstance(_report, Unset):
            report = UNSET
        else:
            report = Report(_report)

        _tax_year = d.pop("taxYear", UNSET)
        tax_year: Union[Unset, TaxYear]
        if isinstance(_tax_year, Unset):
            tax_year = UNSET
        else:
            tax_year = TaxYear(_tax_year)

        papdis_document = cls(
            message_function_code=message_function_code,
            version=version,
            message_function_code_int=message_function_code_int,
            pension_provider=pension_provider,
            report=report,
            tax_year=tax_year,
        )

        return papdis_document
