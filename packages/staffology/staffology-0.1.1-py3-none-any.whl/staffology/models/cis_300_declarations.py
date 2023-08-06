from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="Cis300Declarations")


@attr.s(auto_attribs=True)
class Cis300Declarations:
    """
    Attributes:
        employment_status (Union[Unset, None, str]):
        verification (Union[Unset, None, str]):
        information_correct (Union[Unset, None, str]):
        inactivity (Union[Unset, None, str]):
    """

    employment_status: Union[Unset, None, str] = UNSET
    verification: Union[Unset, None, str] = UNSET
    information_correct: Union[Unset, None, str] = UNSET
    inactivity: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        employment_status = self.employment_status
        verification = self.verification
        information_correct = self.information_correct
        inactivity = self.inactivity

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if employment_status is not UNSET:
            field_dict["employmentStatus"] = employment_status
        if verification is not UNSET:
            field_dict["verification"] = verification
        if information_correct is not UNSET:
            field_dict["informationCorrect"] = information_correct
        if inactivity is not UNSET:
            field_dict["inactivity"] = inactivity

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        employment_status = d.pop("employmentStatus", UNSET)

        verification = d.pop("verification", UNSET)

        information_correct = d.pop("informationCorrect", UNSET)

        inactivity = d.pop("inactivity", UNSET)

        cis_300_declarations = cls(
            employment_status=employment_status,
            verification=verification,
            information_correct=information_correct,
            inactivity=inactivity,
        )

        return cis_300_declarations
