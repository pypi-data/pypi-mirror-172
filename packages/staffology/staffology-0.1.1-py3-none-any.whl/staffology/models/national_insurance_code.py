from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="NationalInsuranceCode")


@attr.s(auto_attribs=True)
class NationalInsuranceCode:
    """Part of the TaxYearConfig that our engine uses to calculate National Insurance Contributions.
    It is used internally when our engine performs calculations.
    You do not need to do anything with this model, it's provided purely for informational purposes.

        Attributes:
            code (Union[Unset, str]): [readonly] NI Table Letter
            description (Union[Unset, None, str]): [readonly] Description of Employees that would use this NI Letter
            ee_b (Union[Unset, float]): [readonly] Earnings at or above LEL up to and including PT (Employee Contribution)
            ee_c (Union[Unset, float]): [readonly] Earnings above the PT up to and including UEL (Employee Contribution)
            ee_d (Union[Unset, float]): [readonly] Balance of earnings above UEL (Employee Contribution)
            ee_e (Union[Unset, float]): [readonly]
            ee_f (Union[Unset, float]): [readonly]
            er_b (Union[Unset, float]): [readonly] Earnings at or above LEL up to and including PT (Employer Contribution)
            er_c (Union[Unset, float]): [readonly]  Earnings above the PT up to and including UEL (Employer Contribution)
            er_d (Union[Unset, float]): [readonly] Balance of earnings above UEL (Employer Contribution)
            er_e (Union[Unset, float]): [readonly]
            er_f (Union[Unset, float]): [readonly]
    """

    code: Union[Unset, str] = UNSET
    description: Union[Unset, None, str] = UNSET
    ee_b: Union[Unset, float] = UNSET
    ee_c: Union[Unset, float] = UNSET
    ee_d: Union[Unset, float] = UNSET
    ee_e: Union[Unset, float] = UNSET
    ee_f: Union[Unset, float] = UNSET
    er_b: Union[Unset, float] = UNSET
    er_c: Union[Unset, float] = UNSET
    er_d: Union[Unset, float] = UNSET
    er_e: Union[Unset, float] = UNSET
    er_f: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        code = self.code
        description = self.description
        ee_b = self.ee_b
        ee_c = self.ee_c
        ee_d = self.ee_d
        ee_e = self.ee_e
        ee_f = self.ee_f
        er_b = self.er_b
        er_c = self.er_c
        er_d = self.er_d
        er_e = self.er_e
        er_f = self.er_f

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if code is not UNSET:
            field_dict["code"] = code
        if description is not UNSET:
            field_dict["description"] = description
        if ee_b is not UNSET:
            field_dict["eeB"] = ee_b
        if ee_c is not UNSET:
            field_dict["eeC"] = ee_c
        if ee_d is not UNSET:
            field_dict["eeD"] = ee_d
        if ee_e is not UNSET:
            field_dict["eeE"] = ee_e
        if ee_f is not UNSET:
            field_dict["eeF"] = ee_f
        if er_b is not UNSET:
            field_dict["erB"] = er_b
        if er_c is not UNSET:
            field_dict["erC"] = er_c
        if er_d is not UNSET:
            field_dict["erD"] = er_d
        if er_e is not UNSET:
            field_dict["erE"] = er_e
        if er_f is not UNSET:
            field_dict["erF"] = er_f

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        code = d.pop("code", UNSET)

        description = d.pop("description", UNSET)

        ee_b = d.pop("eeB", UNSET)

        ee_c = d.pop("eeC", UNSET)

        ee_d = d.pop("eeD", UNSET)

        ee_e = d.pop("eeE", UNSET)

        ee_f = d.pop("eeF", UNSET)

        er_b = d.pop("erB", UNSET)

        er_c = d.pop("erC", UNSET)

        er_d = d.pop("erD", UNSET)

        er_e = d.pop("erE", UNSET)

        er_f = d.pop("erF", UNSET)

        national_insurance_code = cls(
            code=code,
            description=description,
            ee_b=ee_b,
            ee_c=ee_c,
            ee_d=ee_d,
            ee_e=ee_e,
            ee_f=ee_f,
            er_b=er_b,
            er_c=er_c,
            er_d=er_d,
            er_e=er_e,
            er_f=er_f,
        )

        return national_insurance_code
