import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.emp_refs import EmpRefs
from ..models.fps_late_reason import FpsLateReason
from ..models.full_payment_submission import FullPaymentSubmission
from ..models.gov_talk_submission import GovTalkSubmission
from ..models.rti_validation_warning import RtiValidationWarning
from ..models.tax_year import TaxYear
from ..types import UNSET, Unset

T = TypeVar("T", bound="Fps")


@attr.s(auto_attribs=True)
class Fps:
    """
    Attributes:
        late_reason (Union[Unset, FpsLateReason]):
        payment_date (Union[Unset, datetime.date]):
        employee_count (Union[Unset, int]):
        is_correction (Union[Unset, bool]):
        full_payment_submission (Union[Unset, FullPaymentSubmission]):
        validation_warnings (Union[Unset, None, List[RtiValidationWarning]]):
        i_rmark (Union[Unset, None, str]):
        xml (Union[Unset, None, str]):
        tax_year (Union[Unset, TaxYear]):
        employer_references (Union[Unset, EmpRefs]):
        gov_talk_submission (Union[Unset, GovTalkSubmission]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    late_reason: Union[Unset, FpsLateReason] = UNSET
    payment_date: Union[Unset, datetime.date] = UNSET
    employee_count: Union[Unset, int] = UNSET
    is_correction: Union[Unset, bool] = UNSET
    full_payment_submission: Union[Unset, FullPaymentSubmission] = UNSET
    validation_warnings: Union[Unset, None, List[RtiValidationWarning]] = UNSET
    i_rmark: Union[Unset, None, str] = UNSET
    xml: Union[Unset, None, str] = UNSET
    tax_year: Union[Unset, TaxYear] = UNSET
    employer_references: Union[Unset, EmpRefs] = UNSET
    gov_talk_submission: Union[Unset, GovTalkSubmission] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        late_reason: Union[Unset, str] = UNSET
        if not isinstance(self.late_reason, Unset):
            late_reason = self.late_reason.value

        payment_date: Union[Unset, str] = UNSET
        if not isinstance(self.payment_date, Unset):
            payment_date = self.payment_date.isoformat()

        employee_count = self.employee_count
        is_correction = self.is_correction
        full_payment_submission: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.full_payment_submission, Unset):
            full_payment_submission = self.full_payment_submission.to_dict()

        validation_warnings: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.validation_warnings, Unset):
            if self.validation_warnings is None:
                validation_warnings = None
            else:
                validation_warnings = []
                for validation_warnings_item_data in self.validation_warnings:
                    validation_warnings_item = validation_warnings_item_data.to_dict()

                    validation_warnings.append(validation_warnings_item)

        i_rmark = self.i_rmark
        xml = self.xml
        tax_year: Union[Unset, str] = UNSET
        if not isinstance(self.tax_year, Unset):
            tax_year = self.tax_year.value

        employer_references: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employer_references, Unset):
            employer_references = self.employer_references.to_dict()

        gov_talk_submission: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.gov_talk_submission, Unset):
            gov_talk_submission = self.gov_talk_submission.to_dict()

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if late_reason is not UNSET:
            field_dict["lateReason"] = late_reason
        if payment_date is not UNSET:
            field_dict["paymentDate"] = payment_date
        if employee_count is not UNSET:
            field_dict["employeeCount"] = employee_count
        if is_correction is not UNSET:
            field_dict["isCorrection"] = is_correction
        if full_payment_submission is not UNSET:
            field_dict["fullPaymentSubmission"] = full_payment_submission
        if validation_warnings is not UNSET:
            field_dict["validationWarnings"] = validation_warnings
        if i_rmark is not UNSET:
            field_dict["iRmark"] = i_rmark
        if xml is not UNSET:
            field_dict["xml"] = xml
        if tax_year is not UNSET:
            field_dict["taxYear"] = tax_year
        if employer_references is not UNSET:
            field_dict["employerReferences"] = employer_references
        if gov_talk_submission is not UNSET:
            field_dict["govTalkSubmission"] = gov_talk_submission
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _late_reason = d.pop("lateReason", UNSET)
        late_reason: Union[Unset, FpsLateReason]
        if isinstance(_late_reason, Unset):
            late_reason = UNSET
        else:
            late_reason = FpsLateReason(_late_reason)

        _payment_date = d.pop("paymentDate", UNSET)
        payment_date: Union[Unset, datetime.date]
        if isinstance(_payment_date, Unset):
            payment_date = UNSET
        else:
            payment_date = isoparse(_payment_date).date()

        employee_count = d.pop("employeeCount", UNSET)

        is_correction = d.pop("isCorrection", UNSET)

        _full_payment_submission = d.pop("fullPaymentSubmission", UNSET)
        full_payment_submission: Union[Unset, FullPaymentSubmission]
        if isinstance(_full_payment_submission, Unset):
            full_payment_submission = UNSET
        else:
            full_payment_submission = FullPaymentSubmission.from_dict(
                _full_payment_submission
            )

        validation_warnings = []
        _validation_warnings = d.pop("validationWarnings", UNSET)
        for validation_warnings_item_data in _validation_warnings or []:
            validation_warnings_item = RtiValidationWarning.from_dict(
                validation_warnings_item_data
            )

            validation_warnings.append(validation_warnings_item)

        i_rmark = d.pop("iRmark", UNSET)

        xml = d.pop("xml", UNSET)

        _tax_year = d.pop("taxYear", UNSET)
        tax_year: Union[Unset, TaxYear]
        if isinstance(_tax_year, Unset):
            tax_year = UNSET
        else:
            tax_year = TaxYear(_tax_year)

        _employer_references = d.pop("employerReferences", UNSET)
        employer_references: Union[Unset, EmpRefs]
        if isinstance(_employer_references, Unset):
            employer_references = UNSET
        else:
            employer_references = EmpRefs.from_dict(_employer_references)

        _gov_talk_submission = d.pop("govTalkSubmission", UNSET)
        gov_talk_submission: Union[Unset, GovTalkSubmission]
        if isinstance(_gov_talk_submission, Unset):
            gov_talk_submission = UNSET
        else:
            gov_talk_submission = GovTalkSubmission.from_dict(_gov_talk_submission)

        id = d.pop("id", UNSET)

        fps = cls(
            late_reason=late_reason,
            payment_date=payment_date,
            employee_count=employee_count,
            is_correction=is_correction,
            full_payment_submission=full_payment_submission,
            validation_warnings=validation_warnings,
            i_rmark=i_rmark,
            xml=xml,
            tax_year=tax_year,
            employer_references=employer_references,
            gov_talk_submission=gov_talk_submission,
            id=id,
        )

        return fps
