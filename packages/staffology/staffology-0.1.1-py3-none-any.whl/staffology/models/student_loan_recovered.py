from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="StudentLoanRecovered")


@attr.s(auto_attribs=True)
class StudentLoanRecovered:
    """
    Attributes:
        plan_type (Union[Unset, None, str]):
        value (Union[Unset, None, str]):
    """

    plan_type: Union[Unset, None, str] = UNSET
    value: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        plan_type = self.plan_type
        value = self.value

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if plan_type is not UNSET:
            field_dict["planType"] = plan_type
        if value is not UNSET:
            field_dict["value"] = value

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        plan_type = d.pop("planType", UNSET)

        value = d.pop("value", UNSET)

        student_loan_recovered = cls(
            plan_type=plan_type,
            value=value,
        )

        return student_loan_recovered
