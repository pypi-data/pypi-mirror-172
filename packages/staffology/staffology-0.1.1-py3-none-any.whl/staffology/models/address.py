from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.country import Country
from ..types import UNSET, Unset

T = TypeVar("T", bound="Address")


@attr.s(auto_attribs=True)
class Address:
    """
    Attributes:
        line1 (Union[Unset, None, str]):
        line2 (Union[Unset, None, str]):
        line3 (Union[Unset, None, str]):
        line4 (Union[Unset, None, str]):
        line5 (Union[Unset, None, str]):
        post_code (Union[Unset, None, str]):
        country (Union[Unset, Country]):
        foreign_country (Union[Unset, None, str]):
    """

    line1: Union[Unset, None, str] = UNSET
    line2: Union[Unset, None, str] = UNSET
    line3: Union[Unset, None, str] = UNSET
    line4: Union[Unset, None, str] = UNSET
    line5: Union[Unset, None, str] = UNSET
    post_code: Union[Unset, None, str] = UNSET
    country: Union[Unset, Country] = UNSET
    foreign_country: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        line1 = self.line1
        line2 = self.line2
        line3 = self.line3
        line4 = self.line4
        line5 = self.line5
        post_code = self.post_code
        country: Union[Unset, str] = UNSET
        if not isinstance(self.country, Unset):
            country = self.country.value

        foreign_country = self.foreign_country

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if line1 is not UNSET:
            field_dict["line1"] = line1
        if line2 is not UNSET:
            field_dict["line2"] = line2
        if line3 is not UNSET:
            field_dict["line3"] = line3
        if line4 is not UNSET:
            field_dict["line4"] = line4
        if line5 is not UNSET:
            field_dict["line5"] = line5
        if post_code is not UNSET:
            field_dict["postCode"] = post_code
        if country is not UNSET:
            field_dict["country"] = country
        if foreign_country is not UNSET:
            field_dict["foreignCountry"] = foreign_country

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        line1 = d.pop("line1", UNSET)

        line2 = d.pop("line2", UNSET)

        line3 = d.pop("line3", UNSET)

        line4 = d.pop("line4", UNSET)

        line5 = d.pop("line5", UNSET)

        post_code = d.pop("postCode", UNSET)

        _country = d.pop("country", UNSET)
        country: Union[Unset, Country]
        if isinstance(_country, Unset):
            country = UNSET
        else:
            country = Country(_country)

        foreign_country = d.pop("foreignCountry", UNSET)

        address = cls(
            line1=line1,
            line2=line2,
            line3=line3,
            line4=line4,
            line5=line5,
            post_code=post_code,
            country=country,
            foreign_country=foreign_country,
        )

        return address
