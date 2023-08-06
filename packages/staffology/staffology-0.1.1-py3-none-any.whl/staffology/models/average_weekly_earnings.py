import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.average_weekly_earnings_result import AverageWeeklyEarningsResult
from ..types import UNSET, Unset

T = TypeVar("T", bound="AverageWeeklyEarnings")


@attr.s(auto_attribs=True)
class AverageWeeklyEarnings:
    """
    Attributes:
        result (Union[Unset, AverageWeeklyEarningsResult]):
        result_description (Union[Unset, None, str]):
        average_earnings (Union[Unset, float]):
        threshold (Union[Unset, float]):
        eligibility_threshold (Union[Unset, float]):
        requested_date (Union[Unset, datetime.date]):
        relevant_period_start (Union[Unset, datetime.date]):
        relevant_period_end (Union[Unset, datetime.date]):
        relevant_period_week_count (Union[Unset, float]):
        relevant_period_earnings (Union[Unset, float]):
    """

    result: Union[Unset, AverageWeeklyEarningsResult] = UNSET
    result_description: Union[Unset, None, str] = UNSET
    average_earnings: Union[Unset, float] = UNSET
    threshold: Union[Unset, float] = UNSET
    eligibility_threshold: Union[Unset, float] = UNSET
    requested_date: Union[Unset, datetime.date] = UNSET
    relevant_period_start: Union[Unset, datetime.date] = UNSET
    relevant_period_end: Union[Unset, datetime.date] = UNSET
    relevant_period_week_count: Union[Unset, float] = UNSET
    relevant_period_earnings: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        result: Union[Unset, str] = UNSET
        if not isinstance(self.result, Unset):
            result = self.result.value

        result_description = self.result_description
        average_earnings = self.average_earnings
        threshold = self.threshold
        eligibility_threshold = self.eligibility_threshold
        requested_date: Union[Unset, str] = UNSET
        if not isinstance(self.requested_date, Unset):
            requested_date = self.requested_date.isoformat()

        relevant_period_start: Union[Unset, str] = UNSET
        if not isinstance(self.relevant_period_start, Unset):
            relevant_period_start = self.relevant_period_start.isoformat()

        relevant_period_end: Union[Unset, str] = UNSET
        if not isinstance(self.relevant_period_end, Unset):
            relevant_period_end = self.relevant_period_end.isoformat()

        relevant_period_week_count = self.relevant_period_week_count
        relevant_period_earnings = self.relevant_period_earnings

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if result is not UNSET:
            field_dict["result"] = result
        if result_description is not UNSET:
            field_dict["resultDescription"] = result_description
        if average_earnings is not UNSET:
            field_dict["averageEarnings"] = average_earnings
        if threshold is not UNSET:
            field_dict["threshold"] = threshold
        if eligibility_threshold is not UNSET:
            field_dict["eligibilityThreshold"] = eligibility_threshold
        if requested_date is not UNSET:
            field_dict["requestedDate"] = requested_date
        if relevant_period_start is not UNSET:
            field_dict["relevantPeriodStart"] = relevant_period_start
        if relevant_period_end is not UNSET:
            field_dict["relevantPeriodEnd"] = relevant_period_end
        if relevant_period_week_count is not UNSET:
            field_dict["relevantPeriodWeekCount"] = relevant_period_week_count
        if relevant_period_earnings is not UNSET:
            field_dict["relevantPeriodEarnings"] = relevant_period_earnings

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _result = d.pop("result", UNSET)
        result: Union[Unset, AverageWeeklyEarningsResult]
        if isinstance(_result, Unset):
            result = UNSET
        else:
            result = AverageWeeklyEarningsResult(_result)

        result_description = d.pop("resultDescription", UNSET)

        average_earnings = d.pop("averageEarnings", UNSET)

        threshold = d.pop("threshold", UNSET)

        eligibility_threshold = d.pop("eligibilityThreshold", UNSET)

        _requested_date = d.pop("requestedDate", UNSET)
        requested_date: Union[Unset, datetime.date]
        if isinstance(_requested_date, Unset):
            requested_date = UNSET
        else:
            requested_date = isoparse(_requested_date).date()

        _relevant_period_start = d.pop("relevantPeriodStart", UNSET)
        relevant_period_start: Union[Unset, datetime.date]
        if isinstance(_relevant_period_start, Unset):
            relevant_period_start = UNSET
        else:
            relevant_period_start = isoparse(_relevant_period_start).date()

        _relevant_period_end = d.pop("relevantPeriodEnd", UNSET)
        relevant_period_end: Union[Unset, datetime.date]
        if isinstance(_relevant_period_end, Unset):
            relevant_period_end = UNSET
        else:
            relevant_period_end = isoparse(_relevant_period_end).date()

        relevant_period_week_count = d.pop("relevantPeriodWeekCount", UNSET)

        relevant_period_earnings = d.pop("relevantPeriodEarnings", UNSET)

        average_weekly_earnings = cls(
            result=result,
            result_description=result_description,
            average_earnings=average_earnings,
            threshold=threshold,
            eligibility_threshold=eligibility_threshold,
            requested_date=requested_date,
            relevant_period_start=relevant_period_start,
            relevant_period_end=relevant_period_end,
            relevant_period_week_count=relevant_period_week_count,
            relevant_period_earnings=relevant_period_earnings,
        )

        return average_weekly_earnings
