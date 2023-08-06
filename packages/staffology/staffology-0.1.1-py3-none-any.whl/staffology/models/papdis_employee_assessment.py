import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="PapdisEmployeeAssessment")


@attr.s(auto_attribs=True)
class PapdisEmployeeAssessment:
    """
    Attributes:
        assessment_code (Union[Unset, int]): [readonly]
        event_code (Union[Unset, int]): [readonly]
        event_date (Union[Unset, None, datetime.date]): [readonly]
        statutory_letter_code (Union[Unset, None, str]): [readonly]
        is_individual_already_member_of_qps (Union[Unset, bool]): [readonly]
        deferral_date (Union[Unset, None, datetime.date]): [readonly]
        enrolment_communications_issued_date (Union[Unset, None, datetime.date]): [readonly]
        worker_exclusion_code (Union[Unset, None, str]): [readonly]
        reenrolment_indicator (Union[Unset, bool]): [readonly]
        opt_out_window_end_date (Union[Unset, None, datetime.date]): [readonly]
    """

    assessment_code: Union[Unset, int] = UNSET
    event_code: Union[Unset, int] = UNSET
    event_date: Union[Unset, None, datetime.date] = UNSET
    statutory_letter_code: Union[Unset, None, str] = UNSET
    is_individual_already_member_of_qps: Union[Unset, bool] = UNSET
    deferral_date: Union[Unset, None, datetime.date] = UNSET
    enrolment_communications_issued_date: Union[Unset, None, datetime.date] = UNSET
    worker_exclusion_code: Union[Unset, None, str] = UNSET
    reenrolment_indicator: Union[Unset, bool] = UNSET
    opt_out_window_end_date: Union[Unset, None, datetime.date] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        assessment_code = self.assessment_code
        event_code = self.event_code
        event_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.event_date, Unset):
            event_date = self.event_date.isoformat() if self.event_date else None

        statutory_letter_code = self.statutory_letter_code
        is_individual_already_member_of_qps = self.is_individual_already_member_of_qps
        deferral_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.deferral_date, Unset):
            deferral_date = (
                self.deferral_date.isoformat() if self.deferral_date else None
            )

        enrolment_communications_issued_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.enrolment_communications_issued_date, Unset):
            enrolment_communications_issued_date = (
                self.enrolment_communications_issued_date.isoformat()
                if self.enrolment_communications_issued_date
                else None
            )

        worker_exclusion_code = self.worker_exclusion_code
        reenrolment_indicator = self.reenrolment_indicator
        opt_out_window_end_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.opt_out_window_end_date, Unset):
            opt_out_window_end_date = (
                self.opt_out_window_end_date.isoformat()
                if self.opt_out_window_end_date
                else None
            )

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if assessment_code is not UNSET:
            field_dict["assessmentCode"] = assessment_code
        if event_code is not UNSET:
            field_dict["eventCode"] = event_code
        if event_date is not UNSET:
            field_dict["eventDate"] = event_date
        if statutory_letter_code is not UNSET:
            field_dict["statutoryLetterCode"] = statutory_letter_code
        if is_individual_already_member_of_qps is not UNSET:
            field_dict[
                "isIndividualAlreadyMemberOfQPS"
            ] = is_individual_already_member_of_qps
        if deferral_date is not UNSET:
            field_dict["deferralDate"] = deferral_date
        if enrolment_communications_issued_date is not UNSET:
            field_dict[
                "enrolmentCommunicationsIssuedDate"
            ] = enrolment_communications_issued_date
        if worker_exclusion_code is not UNSET:
            field_dict["workerExclusionCode"] = worker_exclusion_code
        if reenrolment_indicator is not UNSET:
            field_dict["reenrolmentIndicator"] = reenrolment_indicator
        if opt_out_window_end_date is not UNSET:
            field_dict["optOutWindowEndDate"] = opt_out_window_end_date

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        assessment_code = d.pop("assessmentCode", UNSET)

        event_code = d.pop("eventCode", UNSET)

        _event_date = d.pop("eventDate", UNSET)
        event_date: Union[Unset, None, datetime.date]
        if _event_date is None:
            event_date = None
        elif isinstance(_event_date, Unset):
            event_date = UNSET
        else:
            event_date = isoparse(_event_date).date()

        statutory_letter_code = d.pop("statutoryLetterCode", UNSET)

        is_individual_already_member_of_qps = d.pop(
            "isIndividualAlreadyMemberOfQPS", UNSET
        )

        _deferral_date = d.pop("deferralDate", UNSET)
        deferral_date: Union[Unset, None, datetime.date]
        if _deferral_date is None:
            deferral_date = None
        elif isinstance(_deferral_date, Unset):
            deferral_date = UNSET
        else:
            deferral_date = isoparse(_deferral_date).date()

        _enrolment_communications_issued_date = d.pop(
            "enrolmentCommunicationsIssuedDate", UNSET
        )
        enrolment_communications_issued_date: Union[Unset, None, datetime.date]
        if _enrolment_communications_issued_date is None:
            enrolment_communications_issued_date = None
        elif isinstance(_enrolment_communications_issued_date, Unset):
            enrolment_communications_issued_date = UNSET
        else:
            enrolment_communications_issued_date = isoparse(
                _enrolment_communications_issued_date
            ).date()

        worker_exclusion_code = d.pop("workerExclusionCode", UNSET)

        reenrolment_indicator = d.pop("reenrolmentIndicator", UNSET)

        _opt_out_window_end_date = d.pop("optOutWindowEndDate", UNSET)
        opt_out_window_end_date: Union[Unset, None, datetime.date]
        if _opt_out_window_end_date is None:
            opt_out_window_end_date = None
        elif isinstance(_opt_out_window_end_date, Unset):
            opt_out_window_end_date = UNSET
        else:
            opt_out_window_end_date = isoparse(_opt_out_window_end_date).date()

        papdis_employee_assessment = cls(
            assessment_code=assessment_code,
            event_code=event_code,
            event_date=event_date,
            statutory_letter_code=statutory_letter_code,
            is_individual_already_member_of_qps=is_individual_already_member_of_qps,
            deferral_date=deferral_date,
            enrolment_communications_issued_date=enrolment_communications_issued_date,
            worker_exclusion_code=worker_exclusion_code,
            reenrolment_indicator=reenrolment_indicator,
            opt_out_window_end_date=opt_out_window_end_date,
        )

        return papdis_employee_assessment
