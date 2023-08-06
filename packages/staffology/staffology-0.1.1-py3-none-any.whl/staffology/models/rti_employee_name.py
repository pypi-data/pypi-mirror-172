from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="RtiEmployeeName")


@attr.s(auto_attribs=True)
class RtiEmployeeName:
    """
    Attributes:
        ttl (Union[Unset, None, str]):
        fore (Union[Unset, None, List[str]]):
        initials (Union[Unset, None, str]):
        sur (Union[Unset, None, str]):
    """

    ttl: Union[Unset, None, str] = UNSET
    fore: Union[Unset, None, List[str]] = UNSET
    initials: Union[Unset, None, str] = UNSET
    sur: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        ttl = self.ttl
        fore: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.fore, Unset):
            if self.fore is None:
                fore = None
            else:
                fore = self.fore

        initials = self.initials
        sur = self.sur

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if ttl is not UNSET:
            field_dict["ttl"] = ttl
        if fore is not UNSET:
            field_dict["fore"] = fore
        if initials is not UNSET:
            field_dict["initials"] = initials
        if sur is not UNSET:
            field_dict["sur"] = sur

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        ttl = d.pop("ttl", UNSET)

        fore = cast(List[str], d.pop("fore", UNSET))

        initials = d.pop("initials", UNSET)

        sur = d.pop("sur", UNSET)

        rti_employee_name = cls(
            ttl=ttl,
            fore=fore,
            initials=initials,
            sur=sur,
        )

        return rti_employee_name
