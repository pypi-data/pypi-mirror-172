from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="RtiEmployeeAddress")


@attr.s(auto_attribs=True)
class RtiEmployeeAddress:
    """
    Attributes:
        line (Union[Unset, None, List[str]]):
        postcode (Union[Unset, None, str]):
        post_code (Union[Unset, None, str]):
        uk_postcode (Union[Unset, None, str]):
        country (Union[Unset, None, str]):
        foreign_country (Union[Unset, None, str]):
    """

    line: Union[Unset, None, List[str]] = UNSET
    postcode: Union[Unset, None, str] = UNSET
    post_code: Union[Unset, None, str] = UNSET
    uk_postcode: Union[Unset, None, str] = UNSET
    country: Union[Unset, None, str] = UNSET
    foreign_country: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        line: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.line, Unset):
            if self.line is None:
                line = None
            else:
                line = self.line

        postcode = self.postcode
        post_code = self.post_code
        uk_postcode = self.uk_postcode
        country = self.country
        foreign_country = self.foreign_country

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if line is not UNSET:
            field_dict["line"] = line
        if postcode is not UNSET:
            field_dict["postcode"] = postcode
        if post_code is not UNSET:
            field_dict["postCode"] = post_code
        if uk_postcode is not UNSET:
            field_dict["ukPostcode"] = uk_postcode
        if country is not UNSET:
            field_dict["country"] = country
        if foreign_country is not UNSET:
            field_dict["foreignCountry"] = foreign_country

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        line = cast(List[str], d.pop("line", UNSET))

        postcode = d.pop("postcode", UNSET)

        post_code = d.pop("postCode", UNSET)

        uk_postcode = d.pop("ukPostcode", UNSET)

        country = d.pop("country", UNSET)

        foreign_country = d.pop("foreignCountry", UNSET)

        rti_employee_address = cls(
            line=line,
            postcode=postcode,
            post_code=post_code,
            uk_postcode=uk_postcode,
            country=country,
            foreign_country=foreign_country,
        )

        return rti_employee_address
