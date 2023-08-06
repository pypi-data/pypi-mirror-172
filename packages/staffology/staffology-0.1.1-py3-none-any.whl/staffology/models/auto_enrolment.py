import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.ae_assessment import AeAssessment
from ..models.ae_employee_state import AeEmployeeState
from ..models.ae_exclusion_code import AeExclusionCode
from ..models.ae_uk_worker import AeUKWorker
from ..types import UNSET, Unset

T = TypeVar("T", bound="AutoEnrolment")


@attr.s(auto_attribs=True)
class AutoEnrolment:
    """
    Attributes:
        state (Union[Unset, AeEmployeeState]):
        state_date (Union[Unset, None, datetime.date]): [readonly]
        uk_worker (Union[Unset, AeUKWorker]):
        days_to_defer_assessment (Union[Unset, int]): The number of days, if any, to defer assessment of this employee.
            You're allowed to defer assessment of new employees by up to 3 months.
        postponement_date (Union[Unset, None, datetime.date]): [readonly] If a value is present, then employee wont be
            enrolled on an AE Pension until after this date.
            This is automatically set to a date if the employee is deemed to be an EligibleJobHolder, but the employer has
            set a Postponement period and this value is currently null
            This is automatically set to null if it already has a value and the employee is deemed NOT to be an
            EligibleJobHolder - ie, they previously qualified but now do not.
        defer_by_months_not_days (Union[Unset, bool]): If set to true then the value in DaysToDeferAssessment will be
            treated as a number of months, not a number of days
        exempt (Union[Unset, bool]):
        ae_exclusion_code (Union[Unset, AeExclusionCode]):
        ae_postponement_letter_sent (Union[Unset, bool]):
        last_assessment (Union[Unset, AeAssessment]): As part of AutoEnrolment we assess your Employees to see if they
            need to be auto-enroled in a Pension.
            This model shows the result of an assessment.
    """

    state: Union[Unset, AeEmployeeState] = UNSET
    state_date: Union[Unset, None, datetime.date] = UNSET
    uk_worker: Union[Unset, AeUKWorker] = UNSET
    days_to_defer_assessment: Union[Unset, int] = UNSET
    postponement_date: Union[Unset, None, datetime.date] = UNSET
    defer_by_months_not_days: Union[Unset, bool] = UNSET
    exempt: Union[Unset, bool] = UNSET
    ae_exclusion_code: Union[Unset, AeExclusionCode] = UNSET
    ae_postponement_letter_sent: Union[Unset, bool] = UNSET
    last_assessment: Union[Unset, AeAssessment] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        state_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.state_date, Unset):
            state_date = self.state_date.isoformat() if self.state_date else None

        uk_worker: Union[Unset, str] = UNSET
        if not isinstance(self.uk_worker, Unset):
            uk_worker = self.uk_worker.value

        days_to_defer_assessment = self.days_to_defer_assessment
        postponement_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.postponement_date, Unset):
            postponement_date = (
                self.postponement_date.isoformat() if self.postponement_date else None
            )

        defer_by_months_not_days = self.defer_by_months_not_days
        exempt = self.exempt
        ae_exclusion_code: Union[Unset, str] = UNSET
        if not isinstance(self.ae_exclusion_code, Unset):
            ae_exclusion_code = self.ae_exclusion_code.value

        ae_postponement_letter_sent = self.ae_postponement_letter_sent
        last_assessment: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.last_assessment, Unset):
            last_assessment = self.last_assessment.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if state is not UNSET:
            field_dict["state"] = state
        if state_date is not UNSET:
            field_dict["stateDate"] = state_date
        if uk_worker is not UNSET:
            field_dict["ukWorker"] = uk_worker
        if days_to_defer_assessment is not UNSET:
            field_dict["daysToDeferAssessment"] = days_to_defer_assessment
        if postponement_date is not UNSET:
            field_dict["postponementDate"] = postponement_date
        if defer_by_months_not_days is not UNSET:
            field_dict["deferByMonthsNotDays"] = defer_by_months_not_days
        if exempt is not UNSET:
            field_dict["exempt"] = exempt
        if ae_exclusion_code is not UNSET:
            field_dict["aeExclusionCode"] = ae_exclusion_code
        if ae_postponement_letter_sent is not UNSET:
            field_dict["aePostponementLetterSent"] = ae_postponement_letter_sent
        if last_assessment is not UNSET:
            field_dict["lastAssessment"] = last_assessment

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _state = d.pop("state", UNSET)
        state: Union[Unset, AeEmployeeState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = AeEmployeeState(_state)

        _state_date = d.pop("stateDate", UNSET)
        state_date: Union[Unset, None, datetime.date]
        if _state_date is None:
            state_date = None
        elif isinstance(_state_date, Unset):
            state_date = UNSET
        else:
            state_date = isoparse(_state_date).date()

        _uk_worker = d.pop("ukWorker", UNSET)
        uk_worker: Union[Unset, AeUKWorker]
        if isinstance(_uk_worker, Unset):
            uk_worker = UNSET
        else:
            uk_worker = AeUKWorker(_uk_worker)

        days_to_defer_assessment = d.pop("daysToDeferAssessment", UNSET)

        _postponement_date = d.pop("postponementDate", UNSET)
        postponement_date: Union[Unset, None, datetime.date]
        if _postponement_date is None:
            postponement_date = None
        elif isinstance(_postponement_date, Unset):
            postponement_date = UNSET
        else:
            postponement_date = isoparse(_postponement_date).date()

        defer_by_months_not_days = d.pop("deferByMonthsNotDays", UNSET)

        exempt = d.pop("exempt", UNSET)

        _ae_exclusion_code = d.pop("aeExclusionCode", UNSET)
        ae_exclusion_code: Union[Unset, AeExclusionCode]
        if isinstance(_ae_exclusion_code, Unset):
            ae_exclusion_code = UNSET
        else:
            ae_exclusion_code = AeExclusionCode(_ae_exclusion_code)

        ae_postponement_letter_sent = d.pop("aePostponementLetterSent", UNSET)

        _last_assessment = d.pop("lastAssessment", UNSET)
        last_assessment: Union[Unset, AeAssessment]
        if isinstance(_last_assessment, Unset):
            last_assessment = UNSET
        else:
            last_assessment = AeAssessment.from_dict(_last_assessment)

        auto_enrolment = cls(
            state=state,
            state_date=state_date,
            uk_worker=uk_worker,
            days_to_defer_assessment=days_to_defer_assessment,
            postponement_date=postponement_date,
            defer_by_months_not_days=defer_by_months_not_days,
            exempt=exempt,
            ae_exclusion_code=ae_exclusion_code,
            ae_postponement_letter_sent=ae_postponement_letter_sent,
            last_assessment=last_assessment,
        )

        return auto_enrolment
