from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="FpsEmployeeTaxCode")


@attr.s(auto_attribs=True)
class FpsEmployeeTaxCode:
    """
    Attributes:
        basis_non_cumulative (Union[Unset, None, str]):
        tax_regime (Union[Unset, None, str]):
        tax_code (Union[Unset, None, str]):
    """

    basis_non_cumulative: Union[Unset, None, str] = UNSET
    tax_regime: Union[Unset, None, str] = UNSET
    tax_code: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        basis_non_cumulative = self.basis_non_cumulative
        tax_regime = self.tax_regime
        tax_code = self.tax_code

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if basis_non_cumulative is not UNSET:
            field_dict["basisNonCumulative"] = basis_non_cumulative
        if tax_regime is not UNSET:
            field_dict["taxRegime"] = tax_regime
        if tax_code is not UNSET:
            field_dict["taxCode"] = tax_code

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        basis_non_cumulative = d.pop("basisNonCumulative", UNSET)

        tax_regime = d.pop("taxRegime", UNSET)

        tax_code = d.pop("taxCode", UNSET)

        fps_employee_tax_code = cls(
            basis_non_cumulative=basis_non_cumulative,
            tax_regime=tax_regime,
            tax_code=tax_code,
        )

        return fps_employee_tax_code
