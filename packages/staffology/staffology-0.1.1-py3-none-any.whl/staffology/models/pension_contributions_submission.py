from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.background_task_status import BackgroundTaskStatus
from ..models.pay_periods import PayPeriods
from ..models.tax_year import TaxYear
from ..types import UNSET, Unset

T = TypeVar("T", bound="PensionContributionsSubmission")


@attr.s(auto_attribs=True)
class PensionContributionsSubmission:
    """This model is used to track submission of Pension Contributions to an external data provider.

    Attributes:
        employer_id (Union[Unset, int]):
        pay_run_id (Union[Unset, int]):
        pay_period (Union[Unset, PayPeriods]):
        ordinal (Union[Unset, int]):
        period (Union[Unset, int]):
        tax_year (Union[Unset, TaxYear]):
        scheme_id (Union[Unset, int]):
        status (Union[Unset, BackgroundTaskStatus]):
        external_id (Union[Unset, None, str]):
        status_message (Union[Unset, None, str]):
        submission_data (Union[Unset, Any]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    employer_id: Union[Unset, int] = UNSET
    pay_run_id: Union[Unset, int] = UNSET
    pay_period: Union[Unset, PayPeriods] = UNSET
    ordinal: Union[Unset, int] = UNSET
    period: Union[Unset, int] = UNSET
    tax_year: Union[Unset, TaxYear] = UNSET
    scheme_id: Union[Unset, int] = UNSET
    status: Union[Unset, BackgroundTaskStatus] = UNSET
    external_id: Union[Unset, None, str] = UNSET
    status_message: Union[Unset, None, str] = UNSET
    submission_data: Union[Unset, Any] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        employer_id = self.employer_id
        pay_run_id = self.pay_run_id
        pay_period: Union[Unset, str] = UNSET
        if not isinstance(self.pay_period, Unset):
            pay_period = self.pay_period.value

        ordinal = self.ordinal
        period = self.period
        tax_year: Union[Unset, str] = UNSET
        if not isinstance(self.tax_year, Unset):
            tax_year = self.tax_year.value

        scheme_id = self.scheme_id
        status: Union[Unset, str] = UNSET
        if not isinstance(self.status, Unset):
            status = self.status.value

        external_id = self.external_id
        status_message = self.status_message
        submission_data = self.submission_data
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if employer_id is not UNSET:
            field_dict["employerId"] = employer_id
        if pay_run_id is not UNSET:
            field_dict["payRunId"] = pay_run_id
        if pay_period is not UNSET:
            field_dict["payPeriod"] = pay_period
        if ordinal is not UNSET:
            field_dict["ordinal"] = ordinal
        if period is not UNSET:
            field_dict["period"] = period
        if tax_year is not UNSET:
            field_dict["taxYear"] = tax_year
        if scheme_id is not UNSET:
            field_dict["schemeId"] = scheme_id
        if status is not UNSET:
            field_dict["status"] = status
        if external_id is not UNSET:
            field_dict["externalId"] = external_id
        if status_message is not UNSET:
            field_dict["statusMessage"] = status_message
        if submission_data is not UNSET:
            field_dict["submissionData"] = submission_data
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        employer_id = d.pop("employerId", UNSET)

        pay_run_id = d.pop("payRunId", UNSET)

        _pay_period = d.pop("payPeriod", UNSET)
        pay_period: Union[Unset, PayPeriods]
        if isinstance(_pay_period, Unset):
            pay_period = UNSET
        else:
            pay_period = PayPeriods(_pay_period)

        ordinal = d.pop("ordinal", UNSET)

        period = d.pop("period", UNSET)

        _tax_year = d.pop("taxYear", UNSET)
        tax_year: Union[Unset, TaxYear]
        if isinstance(_tax_year, Unset):
            tax_year = UNSET
        else:
            tax_year = TaxYear(_tax_year)

        scheme_id = d.pop("schemeId", UNSET)

        _status = d.pop("status", UNSET)
        status: Union[Unset, BackgroundTaskStatus]
        if isinstance(_status, Unset):
            status = UNSET
        else:
            status = BackgroundTaskStatus(_status)

        external_id = d.pop("externalId", UNSET)

        status_message = d.pop("statusMessage", UNSET)

        submission_data = d.pop("submissionData", UNSET)

        id = d.pop("id", UNSET)

        pension_contributions_submission = cls(
            employer_id=employer_id,
            pay_run_id=pay_run_id,
            pay_period=pay_period,
            ordinal=ordinal,
            period=period,
            tax_year=tax_year,
            scheme_id=scheme_id,
            status=status,
            external_id=external_id,
            status_message=status_message,
            submission_data=submission_data,
            id=id,
        )

        return pension_contributions_submission
