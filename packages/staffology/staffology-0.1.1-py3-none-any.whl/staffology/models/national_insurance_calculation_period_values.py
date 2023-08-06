from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="NationalInsuranceCalculationPeriodValues")


@attr.s(auto_attribs=True)
class NationalInsuranceCalculationPeriodValues:
    """Part of the TaxYearConfig that our engine uses to calculate National Insurance Contributions.
    It is used internally when our engine performs calculations.
    You do not need to do anything with this model, it's provided purely for informational purposes.

        Attributes:
            lel (Union[Unset, float]): [readonly] Lower Earnings Limit
            pt (Union[Unset, float]): [readonly] Primary Threshold
            st (Union[Unset, float]): [readonly] Secondary Threshold
            fust (Union[Unset, float]): [readonly] Freeports Upper Accrual Threshold
            uap (Union[Unset, float]): [readonly] Upper Accrual Point
            ust (Union[Unset, float]): [readonly] Upper Secondary Threshold (under 21)
            aust (Union[Unset, float]): [readonly] Apprentice Upper Secondary Threshold (apprentice under 25)
            uel (Union[Unset, float]): [readonly] Upper Earnings Limit
            vust (Union[Unset, float]): [readonly] Veterian Upper Secondary Threshold
    """

    lel: Union[Unset, float] = UNSET
    pt: Union[Unset, float] = UNSET
    st: Union[Unset, float] = UNSET
    fust: Union[Unset, float] = UNSET
    uap: Union[Unset, float] = UNSET
    ust: Union[Unset, float] = UNSET
    aust: Union[Unset, float] = UNSET
    uel: Union[Unset, float] = UNSET
    vust: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        lel = self.lel
        pt = self.pt
        st = self.st
        fust = self.fust
        uap = self.uap
        ust = self.ust
        aust = self.aust
        uel = self.uel
        vust = self.vust

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if lel is not UNSET:
            field_dict["lel"] = lel
        if pt is not UNSET:
            field_dict["pt"] = pt
        if st is not UNSET:
            field_dict["st"] = st
        if fust is not UNSET:
            field_dict["fust"] = fust
        if uap is not UNSET:
            field_dict["uap"] = uap
        if ust is not UNSET:
            field_dict["ust"] = ust
        if aust is not UNSET:
            field_dict["aust"] = aust
        if uel is not UNSET:
            field_dict["uel"] = uel
        if vust is not UNSET:
            field_dict["vust"] = vust

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        lel = d.pop("lel", UNSET)

        pt = d.pop("pt", UNSET)

        st = d.pop("st", UNSET)

        fust = d.pop("fust", UNSET)

        uap = d.pop("uap", UNSET)

        ust = d.pop("ust", UNSET)

        aust = d.pop("aust", UNSET)

        uel = d.pop("uel", UNSET)

        vust = d.pop("vust", UNSET)

        national_insurance_calculation_period_values = cls(
            lel=lel,
            pt=pt,
            st=st,
            fust=fust,
            uap=uap,
            ust=ust,
            aust=aust,
            uel=uel,
            vust=vust,
        )

        return national_insurance_calculation_period_values
