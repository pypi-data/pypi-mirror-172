from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="ExternalDataCompany")


@attr.s(auto_attribs=True)
class ExternalDataCompany:
    """When we retrieve data from an ExternalDataProvider we normalise it so that regardless of the provider the models are
    the same.
    This model is used to represent a Company in an ExternalDataProvider

        Attributes:
            id (Union[Unset, None, str]):
            name (Union[Unset, None, str]):
            scheme_name (Union[Unset, None, str]):
    """

    id: Union[Unset, None, str] = UNSET
    name: Union[Unset, None, str] = UNSET
    scheme_name: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        scheme_name = self.scheme_name

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if scheme_name is not UNSET:
            field_dict["schemeName"] = scheme_name

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        scheme_name = d.pop("schemeName", UNSET)

        external_data_company = cls(
            id=id,
            name=name,
            scheme_name=scheme_name,
        )

        return external_data_company
