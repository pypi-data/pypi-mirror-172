from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.overseas_secondment_status import OverseasSecondmentStatus
from ..types import UNSET, Unset

T = TypeVar("T", bound="OverseasEmployerDetails")


@attr.s(auto_attribs=True)
class OverseasEmployerDetails:
    """
    Attributes:
        overseas_employer (Union[Unset, bool]):
        overseas_secondment_status (Union[Unset, OverseasSecondmentStatus]):
        eea_citizen (Union[Unset, bool]):
        epm_6_scheme (Union[Unset, bool]):
    """

    overseas_employer: Union[Unset, bool] = UNSET
    overseas_secondment_status: Union[Unset, OverseasSecondmentStatus] = UNSET
    eea_citizen: Union[Unset, bool] = UNSET
    epm_6_scheme: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        overseas_employer = self.overseas_employer
        overseas_secondment_status: Union[Unset, str] = UNSET
        if not isinstance(self.overseas_secondment_status, Unset):
            overseas_secondment_status = self.overseas_secondment_status.value

        eea_citizen = self.eea_citizen
        epm_6_scheme = self.epm_6_scheme

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if overseas_employer is not UNSET:
            field_dict["overseasEmployer"] = overseas_employer
        if overseas_secondment_status is not UNSET:
            field_dict["overseasSecondmentStatus"] = overseas_secondment_status
        if eea_citizen is not UNSET:
            field_dict["eeaCitizen"] = eea_citizen
        if epm_6_scheme is not UNSET:
            field_dict["epm6Scheme"] = epm_6_scheme

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        overseas_employer = d.pop("overseasEmployer", UNSET)

        _overseas_secondment_status = d.pop("overseasSecondmentStatus", UNSET)
        overseas_secondment_status: Union[Unset, OverseasSecondmentStatus]
        if isinstance(_overseas_secondment_status, Unset):
            overseas_secondment_status = UNSET
        else:
            overseas_secondment_status = OverseasSecondmentStatus(
                _overseas_secondment_status
            )

        eea_citizen = d.pop("eeaCitizen", UNSET)

        epm_6_scheme = d.pop("epm6Scheme", UNSET)

        overseas_employer_details = cls(
            overseas_employer=overseas_employer,
            overseas_secondment_status=overseas_secondment_status,
            eea_citizen=eea_citizen,
            epm_6_scheme=epm_6_scheme,
        )

        return overseas_employer_details
