import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="DpsSettings")


@attr.s(auto_attribs=True)
class DpsSettings:
    """This model is used to set an employers settings for HMRCs Data Provisioning Service

    Attributes:
        enabled (Union[Unset, bool]): If enabled, we'll automatically retrieve DPS notices from HMRC for you
        retrieve_from (Union[Unset, datetime.date]): The date from which notices should be retrieved
        auto_apply (Union[Unset, bool]): If enabled, we'll automatically apply DPSNotices before starting a payrun that
            covers the EffectiveDate
        last_checked (Union[Unset, None, datetime.date]): [readonly] The time we last checked for notices
        error (Union[Unset, None, str]): [readonly] If we received an error from HMRC when checking for notices, it'll
            be displayed here
    """

    enabled: Union[Unset, bool] = UNSET
    retrieve_from: Union[Unset, datetime.date] = UNSET
    auto_apply: Union[Unset, bool] = UNSET
    last_checked: Union[Unset, None, datetime.date] = UNSET
    error: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        enabled = self.enabled
        retrieve_from: Union[Unset, str] = UNSET
        if not isinstance(self.retrieve_from, Unset):
            retrieve_from = self.retrieve_from.isoformat()

        auto_apply = self.auto_apply
        last_checked: Union[Unset, None, str] = UNSET
        if not isinstance(self.last_checked, Unset):
            last_checked = self.last_checked.isoformat() if self.last_checked else None

        error = self.error

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if enabled is not UNSET:
            field_dict["enabled"] = enabled
        if retrieve_from is not UNSET:
            field_dict["retrieveFrom"] = retrieve_from
        if auto_apply is not UNSET:
            field_dict["autoApply"] = auto_apply
        if last_checked is not UNSET:
            field_dict["lastChecked"] = last_checked
        if error is not UNSET:
            field_dict["error"] = error

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        enabled = d.pop("enabled", UNSET)

        _retrieve_from = d.pop("retrieveFrom", UNSET)
        retrieve_from: Union[Unset, datetime.date]
        if isinstance(_retrieve_from, Unset):
            retrieve_from = UNSET
        else:
            retrieve_from = isoparse(_retrieve_from).date()

        auto_apply = d.pop("autoApply", UNSET)

        _last_checked = d.pop("lastChecked", UNSET)
        last_checked: Union[Unset, None, datetime.date]
        if _last_checked is None:
            last_checked = None
        elif isinstance(_last_checked, Unset):
            last_checked = UNSET
        else:
            last_checked = isoparse(_last_checked).date()

        error = d.pop("error", UNSET)

        dps_settings = cls(
            enabled=enabled,
            retrieve_from=retrieve_from,
            auto_apply=auto_apply,
            last_checked=last_checked,
            error=error,
        )

        return dps_settings
