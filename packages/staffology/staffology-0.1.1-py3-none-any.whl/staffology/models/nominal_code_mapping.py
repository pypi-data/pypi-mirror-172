from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="NominalCodeMapping")


@attr.s(auto_attribs=True)
class NominalCodeMapping:
    """
    Attributes:
        nominal_code (Union[Unset, None, str]):
        nominal_name (Union[Unset, None, str]):
        external_id (Union[Unset, None, str]): If you will be using the API to post journals to an ExternalDataProvider,
            then this is the Id of the nominal code in the external system.
            If there's no mapping then this will have a value of "0"
        pay_code (Union[Unset, None, str]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    nominal_code: Union[Unset, None, str] = UNSET
    nominal_name: Union[Unset, None, str] = UNSET
    external_id: Union[Unset, None, str] = UNSET
    pay_code: Union[Unset, None, str] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        nominal_code = self.nominal_code
        nominal_name = self.nominal_name
        external_id = self.external_id
        pay_code = self.pay_code
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if nominal_code is not UNSET:
            field_dict["nominalCode"] = nominal_code
        if nominal_name is not UNSET:
            field_dict["nominalName"] = nominal_name
        if external_id is not UNSET:
            field_dict["externalId"] = external_id
        if pay_code is not UNSET:
            field_dict["payCode"] = pay_code
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        nominal_code = d.pop("nominalCode", UNSET)

        nominal_name = d.pop("nominalName", UNSET)

        external_id = d.pop("externalId", UNSET)

        pay_code = d.pop("payCode", UNSET)

        id = d.pop("id", UNSET)

        nominal_code_mapping = cls(
            nominal_code=nominal_code,
            nominal_name=nominal_name,
            external_id=external_id,
            pay_code=pay_code,
            id=id,
        )

        return nominal_code_mapping
