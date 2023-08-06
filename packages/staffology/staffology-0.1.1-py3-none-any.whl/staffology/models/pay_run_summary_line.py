from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.pay_code import PayCode
from ..types import UNSET, Unset

T = TypeVar("T", bound="PayRunSummaryLine")


@attr.s(auto_attribs=True)
class PayRunSummaryLine:
    """An array of this model is used to represent a summary of a PayRun.
    This would typically be used for creating accounting entries for the PayRun.

        Attributes:
            nominal_code (Union[Unset, None, str]): [readonly] If you've set up NominalCodeMapping then the relevant Nominal
                code for the PayCode will be shown here.
            department_code (Union[Unset, None, str]): [readonly] If the journal is split by department then the relevant
                department code is shown here.
            nominal_name (Union[Unset, None, str]): [readonly] As above
            description (Union[Unset, None, str]): [readonly] A description of what this line summarises.
            qty (Union[Unset, None, float]): [readonly] If the PayCode is a Multiplier code then this will contain the
                number of days/hours
            value (Union[Unset, float]): [readonly] The total value for this line.
            pay_code (Union[Unset, PayCode]): Each PayLine has a Code. The Code will match the Code property of a PayCode.
                The PayCode that is used determines how the amount is treated with regards to tax, NI and pensions
    """

    nominal_code: Union[Unset, None, str] = UNSET
    department_code: Union[Unset, None, str] = UNSET
    nominal_name: Union[Unset, None, str] = UNSET
    description: Union[Unset, None, str] = UNSET
    qty: Union[Unset, None, float] = UNSET
    value: Union[Unset, float] = UNSET
    pay_code: Union[Unset, PayCode] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        nominal_code = self.nominal_code
        department_code = self.department_code
        nominal_name = self.nominal_name
        description = self.description
        qty = self.qty
        value = self.value
        pay_code: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pay_code, Unset):
            pay_code = self.pay_code.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if nominal_code is not UNSET:
            field_dict["nominalCode"] = nominal_code
        if department_code is not UNSET:
            field_dict["departmentCode"] = department_code
        if nominal_name is not UNSET:
            field_dict["nominalName"] = nominal_name
        if description is not UNSET:
            field_dict["description"] = description
        if qty is not UNSET:
            field_dict["qty"] = qty
        if value is not UNSET:
            field_dict["value"] = value
        if pay_code is not UNSET:
            field_dict["payCode"] = pay_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        nominal_code = d.pop("nominalCode", UNSET)

        department_code = d.pop("departmentCode", UNSET)

        nominal_name = d.pop("nominalName", UNSET)

        description = d.pop("description", UNSET)

        qty = d.pop("qty", UNSET)

        value = d.pop("value", UNSET)

        _pay_code = d.pop("payCode", UNSET)
        pay_code: Union[Unset, PayCode]
        if isinstance(_pay_code, Unset):
            pay_code = UNSET
        else:
            pay_code = PayCode.from_dict(_pay_code)

        pay_run_summary_line = cls(
            nominal_code=nominal_code,
            department_code=department_code,
            nominal_name=nominal_name,
            description=description,
            qty=qty,
            value=value,
            pay_code=pay_code,
        )

        return pay_run_summary_line
