from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="EpsAccount")


@attr.s(auto_attribs=True)
class EpsAccount:
    """Used on an EPS to send bank account information

    Attributes:
        account_holders_name (Union[Unset, None, str]):
        account_no (Union[Unset, None, str]):
        sort_code (Union[Unset, None, str]):
        building_soc_ref (Union[Unset, None, str]):
    """

    account_holders_name: Union[Unset, None, str] = UNSET
    account_no: Union[Unset, None, str] = UNSET
    sort_code: Union[Unset, None, str] = UNSET
    building_soc_ref: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        account_holders_name = self.account_holders_name
        account_no = self.account_no
        sort_code = self.sort_code
        building_soc_ref = self.building_soc_ref

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if account_holders_name is not UNSET:
            field_dict["accountHoldersName"] = account_holders_name
        if account_no is not UNSET:
            field_dict["accountNo"] = account_no
        if sort_code is not UNSET:
            field_dict["sortCode"] = sort_code
        if building_soc_ref is not UNSET:
            field_dict["buildingSocRef"] = building_soc_ref

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        account_holders_name = d.pop("accountHoldersName", UNSET)

        account_no = d.pop("accountNo", UNSET)

        sort_code = d.pop("sortCode", UNSET)

        building_soc_ref = d.pop("buildingSocRef", UNSET)

        eps_account = cls(
            account_holders_name=account_holders_name,
            account_no=account_no,
            sort_code=sort_code,
            building_soc_ref=building_soc_ref,
        )

        return eps_account
