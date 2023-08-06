from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="EmpRefs")


@attr.s(auto_attribs=True)
class EmpRefs:
    """
    Attributes:
        office_no (Union[Unset, None, str]):
        paye_ref (Union[Unset, None, str]):
        ao_ref (Union[Unset, None, str]):
        econ (Union[Unset, None, str]):
        cotax_ref (Union[Unset, None, str]):
        sautr (Union[Unset, None, str]):
    """

    office_no: Union[Unset, None, str] = UNSET
    paye_ref: Union[Unset, None, str] = UNSET
    ao_ref: Union[Unset, None, str] = UNSET
    econ: Union[Unset, None, str] = UNSET
    cotax_ref: Union[Unset, None, str] = UNSET
    sautr: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        office_no = self.office_no
        paye_ref = self.paye_ref
        ao_ref = self.ao_ref
        econ = self.econ
        cotax_ref = self.cotax_ref
        sautr = self.sautr

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if office_no is not UNSET:
            field_dict["officeNo"] = office_no
        if paye_ref is not UNSET:
            field_dict["payeRef"] = paye_ref
        if ao_ref is not UNSET:
            field_dict["aoRef"] = ao_ref
        if econ is not UNSET:
            field_dict["econ"] = econ
        if cotax_ref is not UNSET:
            field_dict["cotaxRef"] = cotax_ref
        if sautr is not UNSET:
            field_dict["sautr"] = sautr

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        office_no = d.pop("officeNo", UNSET)

        paye_ref = d.pop("payeRef", UNSET)

        ao_ref = d.pop("aoRef", UNSET)

        econ = d.pop("econ", UNSET)

        cotax_ref = d.pop("cotaxRef", UNSET)

        sautr = d.pop("sautr", UNSET)

        emp_refs = cls(
            office_no=office_no,
            paye_ref=paye_ref,
            ao_ref=ao_ref,
            econ=econ,
            cotax_ref=cotax_ref,
            sautr=sautr,
        )

        return emp_refs
