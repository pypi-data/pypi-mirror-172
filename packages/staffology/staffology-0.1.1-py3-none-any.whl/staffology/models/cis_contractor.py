from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CisContractor")


@attr.s(auto_attribs=True)
class CisContractor:
    """Used to represent details of a CIS SubContractor when communicating with the HMRC Gateway

    Attributes:
        utr (Union[Unset, None, str]):
        a_oref (Union[Unset, None, str]):
    """

    utr: Union[Unset, None, str] = UNSET
    a_oref: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        utr = self.utr
        a_oref = self.a_oref

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if utr is not UNSET:
            field_dict["utr"] = utr
        if a_oref is not UNSET:
            field_dict["aOref"] = a_oref

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        utr = d.pop("utr", UNSET)

        a_oref = d.pop("aOref", UNSET)

        cis_contractor = cls(
            utr=utr,
            a_oref=a_oref,
        )

        return cis_contractor
