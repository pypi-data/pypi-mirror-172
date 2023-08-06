from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="CookiePreference")


@attr.s(auto_attribs=True)
class CookiePreference:
    """
    Attributes:
        gainsight (Union[Unset, None, bool]):
    """

    gainsight: Union[Unset, None, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        gainsight = self.gainsight

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if gainsight is not UNSET:
            field_dict["gainsight"] = gainsight

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        gainsight = d.pop("gainsight", UNSET)

        cookie_preference = cls(
            gainsight=gainsight,
        )

        return cookie_preference
