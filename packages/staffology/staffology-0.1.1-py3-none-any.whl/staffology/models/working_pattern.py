import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.bank_holiday_collection import BankHolidayCollection
from ..models.pro_rata_rule import ProRataRule
from ..types import UNSET, Unset

T = TypeVar("T", bound="WorkingPattern")


@attr.s(auto_attribs=True)
class WorkingPattern:
    """
    Attributes:
        title (str):
        mon (Union[Unset, float]):
        tue (Union[Unset, float]):
        wed (Union[Unset, float]):
        thu (Union[Unset, float]):
        fri (Union[Unset, float]):
        sat (Union[Unset, float]):
        sun (Union[Unset, float]):
        bank_holidays (Union[Unset, BankHolidayCollection]):
        pro_rata_rule (Union[Unset, ProRataRule]):
        bank_holiday_dates (Union[Unset, None, List[datetime.datetime]]): [readonly] The dates that are classed as Bank
            Holidays for this Working Pattern
        is_default (Union[Unset, bool]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    title: str
    mon: Union[Unset, float] = UNSET
    tue: Union[Unset, float] = UNSET
    wed: Union[Unset, float] = UNSET
    thu: Union[Unset, float] = UNSET
    fri: Union[Unset, float] = UNSET
    sat: Union[Unset, float] = UNSET
    sun: Union[Unset, float] = UNSET
    bank_holidays: Union[Unset, BankHolidayCollection] = UNSET
    pro_rata_rule: Union[Unset, ProRataRule] = UNSET
    bank_holiday_dates: Union[Unset, None, List[datetime.datetime]] = UNSET
    is_default: Union[Unset, bool] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        title = self.title
        mon = self.mon
        tue = self.tue
        wed = self.wed
        thu = self.thu
        fri = self.fri
        sat = self.sat
        sun = self.sun
        bank_holidays: Union[Unset, str] = UNSET
        if not isinstance(self.bank_holidays, Unset):
            bank_holidays = self.bank_holidays.value

        pro_rata_rule: Union[Unset, str] = UNSET
        if not isinstance(self.pro_rata_rule, Unset):
            pro_rata_rule = self.pro_rata_rule.value

        bank_holiday_dates: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.bank_holiday_dates, Unset):
            if self.bank_holiday_dates is None:
                bank_holiday_dates = None
            else:
                bank_holiday_dates = []
                for bank_holiday_dates_item_data in self.bank_holiday_dates:
                    bank_holiday_dates_item = bank_holiday_dates_item_data.isoformat()

                    bank_holiday_dates.append(bank_holiday_dates_item)

        is_default = self.is_default
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "title": title,
            }
        )
        if mon is not UNSET:
            field_dict["mon"] = mon
        if tue is not UNSET:
            field_dict["tue"] = tue
        if wed is not UNSET:
            field_dict["wed"] = wed
        if thu is not UNSET:
            field_dict["thu"] = thu
        if fri is not UNSET:
            field_dict["fri"] = fri
        if sat is not UNSET:
            field_dict["sat"] = sat
        if sun is not UNSET:
            field_dict["sun"] = sun
        if bank_holidays is not UNSET:
            field_dict["bankHolidays"] = bank_holidays
        if pro_rata_rule is not UNSET:
            field_dict["proRataRule"] = pro_rata_rule
        if bank_holiday_dates is not UNSET:
            field_dict["bankHolidayDates"] = bank_holiday_dates
        if is_default is not UNSET:
            field_dict["isDefault"] = is_default
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        title = d.pop("title")

        mon = d.pop("mon", UNSET)

        tue = d.pop("tue", UNSET)

        wed = d.pop("wed", UNSET)

        thu = d.pop("thu", UNSET)

        fri = d.pop("fri", UNSET)

        sat = d.pop("sat", UNSET)

        sun = d.pop("sun", UNSET)

        _bank_holidays = d.pop("bankHolidays", UNSET)
        bank_holidays: Union[Unset, BankHolidayCollection]
        if isinstance(_bank_holidays, Unset):
            bank_holidays = UNSET
        else:
            bank_holidays = BankHolidayCollection(_bank_holidays)

        _pro_rata_rule = d.pop("proRataRule", UNSET)
        pro_rata_rule: Union[Unset, ProRataRule]
        if isinstance(_pro_rata_rule, Unset):
            pro_rata_rule = UNSET
        else:
            pro_rata_rule = ProRataRule(_pro_rata_rule)

        bank_holiday_dates = []
        _bank_holiday_dates = d.pop("bankHolidayDates", UNSET)
        for bank_holiday_dates_item_data in _bank_holiday_dates or []:
            bank_holiday_dates_item = isoparse(bank_holiday_dates_item_data)

            bank_holiday_dates.append(bank_holiday_dates_item)

        is_default = d.pop("isDefault", UNSET)

        id = d.pop("id", UNSET)

        working_pattern = cls(
            title=title,
            mon=mon,
            tue=tue,
            wed=wed,
            thu=thu,
            fri=fri,
            sat=sat,
            sun=sun,
            bank_holidays=bank_holidays,
            pro_rata_rule=pro_rata_rule,
            bank_holiday_dates=bank_holiday_dates,
            is_default=is_default,
            id=id,
        )

        return working_pattern
