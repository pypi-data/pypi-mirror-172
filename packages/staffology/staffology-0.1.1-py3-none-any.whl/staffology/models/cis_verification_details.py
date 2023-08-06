import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.cis_sub_contractor import CisSubContractor
from ..models.cis_tax_status import CISTaxStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="CisVerificationDetails")


@attr.s(auto_attribs=True)
class CisVerificationDetails:
    """
    Attributes:
        manually_entered (Union[Unset, bool]):
        match_instead_of_verify (Union[Unset, bool]):
        number (Union[Unset, None, str]):
        date (Union[Unset, None, datetime.date]):
        tax_status (Union[Unset, CISTaxStatus]):
        verification_request (Union[Unset, None, str]): [readonly] If a Verification request has been made for this
            employee then this will show its ID
        verification_response (Union[Unset, CisSubContractor]):
    """

    manually_entered: Union[Unset, bool] = UNSET
    match_instead_of_verify: Union[Unset, bool] = UNSET
    number: Union[Unset, None, str] = UNSET
    date: Union[Unset, None, datetime.date] = UNSET
    tax_status: Union[Unset, CISTaxStatus] = UNSET
    verification_request: Union[Unset, None, str] = UNSET
    verification_response: Union[Unset, CisSubContractor] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        manually_entered = self.manually_entered
        match_instead_of_verify = self.match_instead_of_verify
        number = self.number
        date: Union[Unset, None, str] = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat() if self.date else None

        tax_status: Union[Unset, str] = UNSET
        if not isinstance(self.tax_status, Unset):
            tax_status = self.tax_status.value

        verification_request = self.verification_request
        verification_response: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.verification_response, Unset):
            verification_response = self.verification_response.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if manually_entered is not UNSET:
            field_dict["manuallyEntered"] = manually_entered
        if match_instead_of_verify is not UNSET:
            field_dict["matchInsteadOfVerify"] = match_instead_of_verify
        if number is not UNSET:
            field_dict["number"] = number
        if date is not UNSET:
            field_dict["date"] = date
        if tax_status is not UNSET:
            field_dict["taxStatus"] = tax_status
        if verification_request is not UNSET:
            field_dict["verificationRequest"] = verification_request
        if verification_response is not UNSET:
            field_dict["verificationResponse"] = verification_response

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        manually_entered = d.pop("manuallyEntered", UNSET)

        match_instead_of_verify = d.pop("matchInsteadOfVerify", UNSET)

        number = d.pop("number", UNSET)

        _date = d.pop("date", UNSET)
        date: Union[Unset, None, datetime.date]
        if _date is None:
            date = None
        elif isinstance(_date, Unset):
            date = UNSET
        else:
            date = isoparse(_date).date()

        _tax_status = d.pop("taxStatus", UNSET)
        tax_status: Union[Unset, CISTaxStatus]
        if isinstance(_tax_status, Unset):
            tax_status = UNSET
        else:
            tax_status = CISTaxStatus(_tax_status)

        verification_request = d.pop("verificationRequest", UNSET)

        _verification_response = d.pop("verificationResponse", UNSET)
        verification_response: Union[Unset, CisSubContractor]
        if isinstance(_verification_response, Unset):
            verification_response = UNSET
        else:
            verification_response = CisSubContractor.from_dict(_verification_response)

        cis_verification_details = cls(
            manually_entered=manually_entered,
            match_instead_of_verify=match_instead_of_verify,
            number=number,
            date=date,
            tax_status=tax_status,
            verification_request=verification_request,
            verification_response=verification_response,
        )

        return cis_verification_details
