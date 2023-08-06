from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExbDeclarations")


@attr.s(auto_attribs=True)
class ExbDeclarations:
    """
    Attributes:
        p_11_dincluded (Union[Unset, None, str]):
        p_46_car_declaration (Union[Unset, None, str]):
    """

    p_11_dincluded: Union[Unset, None, str] = UNSET
    p_46_car_declaration: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        p_11_dincluded = self.p_11_dincluded
        p_46_car_declaration = self.p_46_car_declaration

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if p_11_dincluded is not UNSET:
            field_dict["p11Dincluded"] = p_11_dincluded
        if p_46_car_declaration is not UNSET:
            field_dict["p46CarDeclaration"] = p_46_car_declaration

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        p_11_dincluded = d.pop("p11Dincluded", UNSET)

        p_46_car_declaration = d.pop("p46CarDeclaration", UNSET)

        exb_declarations = cls(
            p_11_dincluded=p_11_dincluded,
            p_46_car_declaration=p_46_car_declaration,
        )

        return exb_declarations
