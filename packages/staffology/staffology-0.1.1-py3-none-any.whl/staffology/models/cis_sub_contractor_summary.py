from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..models.cis_sub_contractor_type import CISSubContractorType
from ..models.cis_tax_status import CISTaxStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="CisSubContractorSummary")


@attr.s(auto_attribs=True)
class CisSubContractorSummary:
    """
    Attributes:
        payroll_code (Union[Unset, None, str]):
        trading_name (Union[Unset, None, str]):
        first_name (Union[Unset, None, str]):
        last_name (Union[Unset, None, str]):
        ni_number (Union[Unset, None, str]):
        type (Union[Unset, CISSubContractorType]):
        utr (Union[Unset, None, str]):
        tax_status (Union[Unset, CISTaxStatus]):
        verification_number (Union[Unset, None, str]):
        display_name (Union[Unset, None, str]):
        validation_message (Union[Unset, None, List[str]]):
    """

    payroll_code: Union[Unset, None, str] = UNSET
    trading_name: Union[Unset, None, str] = UNSET
    first_name: Union[Unset, None, str] = UNSET
    last_name: Union[Unset, None, str] = UNSET
    ni_number: Union[Unset, None, str] = UNSET
    type: Union[Unset, CISSubContractorType] = UNSET
    utr: Union[Unset, None, str] = UNSET
    tax_status: Union[Unset, CISTaxStatus] = UNSET
    verification_number: Union[Unset, None, str] = UNSET
    display_name: Union[Unset, None, str] = UNSET
    validation_message: Union[Unset, None, List[str]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        payroll_code = self.payroll_code
        trading_name = self.trading_name
        first_name = self.first_name
        last_name = self.last_name
        ni_number = self.ni_number
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        utr = self.utr
        tax_status: Union[Unset, str] = UNSET
        if not isinstance(self.tax_status, Unset):
            tax_status = self.tax_status.value

        verification_number = self.verification_number
        display_name = self.display_name
        validation_message: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.validation_message, Unset):
            if self.validation_message is None:
                validation_message = None
            else:
                validation_message = self.validation_message

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if payroll_code is not UNSET:
            field_dict["payrollCode"] = payroll_code
        if trading_name is not UNSET:
            field_dict["tradingName"] = trading_name
        if first_name is not UNSET:
            field_dict["firstName"] = first_name
        if last_name is not UNSET:
            field_dict["lastName"] = last_name
        if ni_number is not UNSET:
            field_dict["niNumber"] = ni_number
        if type is not UNSET:
            field_dict["type"] = type
        if utr is not UNSET:
            field_dict["utr"] = utr
        if tax_status is not UNSET:
            field_dict["taxStatus"] = tax_status
        if verification_number is not UNSET:
            field_dict["verificationNumber"] = verification_number
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if validation_message is not UNSET:
            field_dict["validationMessage"] = validation_message

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        payroll_code = d.pop("payrollCode", UNSET)

        trading_name = d.pop("tradingName", UNSET)

        first_name = d.pop("firstName", UNSET)

        last_name = d.pop("lastName", UNSET)

        ni_number = d.pop("niNumber", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, CISSubContractorType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = CISSubContractorType(_type)

        utr = d.pop("utr", UNSET)

        _tax_status = d.pop("taxStatus", UNSET)
        tax_status: Union[Unset, CISTaxStatus]
        if isinstance(_tax_status, Unset):
            tax_status = UNSET
        else:
            tax_status = CISTaxStatus(_tax_status)

        verification_number = d.pop("verificationNumber", UNSET)

        display_name = d.pop("displayName", UNSET)

        validation_message = cast(List[str], d.pop("validationMessage", UNSET))

        cis_sub_contractor_summary = cls(
            payroll_code=payroll_code,
            trading_name=trading_name,
            first_name=first_name,
            last_name=last_name,
            ni_number=ni_number,
            type=type,
            utr=utr,
            tax_status=tax_status,
            verification_number=verification_number,
            display_name=display_name,
            validation_message=validation_message,
        )

        return cis_sub_contractor_summary
