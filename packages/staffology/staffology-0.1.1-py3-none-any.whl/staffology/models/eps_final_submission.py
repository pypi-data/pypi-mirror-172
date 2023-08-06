import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="EpsFinalSubmission")


@attr.s(auto_attribs=True)
class EpsFinalSubmission:
    """Used on an EPS to declare a Final Submission

    Attributes:
        is_final_submission (Union[Unset, bool]):
        because_scheme_ceased (Union[Unset, bool]):
        date_ceased (Union[Unset, None, datetime.date]):
    """

    is_final_submission: Union[Unset, bool] = UNSET
    because_scheme_ceased: Union[Unset, bool] = UNSET
    date_ceased: Union[Unset, None, datetime.date] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        is_final_submission = self.is_final_submission
        because_scheme_ceased = self.because_scheme_ceased
        date_ceased: Union[Unset, None, str] = UNSET
        if not isinstance(self.date_ceased, Unset):
            date_ceased = self.date_ceased.isoformat() if self.date_ceased else None

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if is_final_submission is not UNSET:
            field_dict["isFinalSubmission"] = is_final_submission
        if because_scheme_ceased is not UNSET:
            field_dict["becauseSchemeCeased"] = because_scheme_ceased
        if date_ceased is not UNSET:
            field_dict["dateCeased"] = date_ceased

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        is_final_submission = d.pop("isFinalSubmission", UNSET)

        because_scheme_ceased = d.pop("becauseSchemeCeased", UNSET)

        _date_ceased = d.pop("dateCeased", UNSET)
        date_ceased: Union[Unset, None, datetime.date]
        if _date_ceased is None:
            date_ceased = None
        elif isinstance(_date_ceased, Unset):
            date_ceased = UNSET
        else:
            date_ceased = isoparse(_date_ceased).date()

        eps_final_submission = cls(
            is_final_submission=is_final_submission,
            because_scheme_ceased=because_scheme_ceased,
            date_ceased=date_ceased,
        )

        return eps_final_submission
