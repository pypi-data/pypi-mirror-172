from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="NationalInsuranceCalculationBase")


@attr.s(auto_attribs=True)
class NationalInsuranceCalculationBase:
    """Included as part of the PayRunEntry model to provide details of how the National Insurance Contribution was
    calculated.
    Unless the PayRunEntry.ManualNi property is set to true then these value will all be read-only and are recalculated
    everytime a payrun is updated.
    This calculation could be made up of one or more calculations made on different NI table letters.
    Where more than NI table letter affects the calculation, the calculation for each NI table letter will be contain in
    the Breakdown.

        Attributes:
            ni_category (Union[Unset, str]): Calculated on NI table letter
            as_director (Union[Unset, bool]): Calculated as a Director
            earnings_upto_including_lel (Union[Unset, float]): Earnings up to and including LEL
            earnings_above_lel_upto_including_pt (Union[Unset, float]): Earnings above LEL up to PT
            earnings_above_pt_upto_including_st (Union[Unset, float]): Earnings above PT up to ST
            earnings_above_pt_upto_including_uel (Union[Unset, float]): Earnings above PT up to UEL
            earnings_above_st_upto_including_uel (Union[Unset, float]): Earnings above ST up to UEL
            earnings_above_st_upto_including_fust (Union[Unset, None, float]): Earnings above ST up to FUST
            earnings_above_fust_upto_including_uel (Union[Unset, None, float]): Earnings above FUST up to UEL
            earnings_above_uel (Union[Unset, float]): Earnings above UEL
            employee_ni_gross (Union[Unset, float]): Employee National Insurance Gross Value
            employee_ni_rebate (Union[Unset, float]): Employee National Insurance Rebate Value
            employer_ni_gross (Union[Unset, float]): Employer National Insurance Gross Value
            employer_ni_rebate (Union[Unset, float]): Employer National Insurance Rebate Value
            employee_ni (Union[Unset, float]): [readonly] Net Employee National Insurance
            employer_ni (Union[Unset, float]): [readonly] Net Employer National Insurance
            net_ni (Union[Unset, float]): [readonly] Net National Insurance (Employer + Employee)
    """

    ni_category: Union[Unset, str] = UNSET
    as_director: Union[Unset, bool] = UNSET
    earnings_upto_including_lel: Union[Unset, float] = UNSET
    earnings_above_lel_upto_including_pt: Union[Unset, float] = UNSET
    earnings_above_pt_upto_including_st: Union[Unset, float] = UNSET
    earnings_above_pt_upto_including_uel: Union[Unset, float] = UNSET
    earnings_above_st_upto_including_uel: Union[Unset, float] = UNSET
    earnings_above_st_upto_including_fust: Union[Unset, None, float] = UNSET
    earnings_above_fust_upto_including_uel: Union[Unset, None, float] = UNSET
    earnings_above_uel: Union[Unset, float] = UNSET
    employee_ni_gross: Union[Unset, float] = UNSET
    employee_ni_rebate: Union[Unset, float] = UNSET
    employer_ni_gross: Union[Unset, float] = UNSET
    employer_ni_rebate: Union[Unset, float] = UNSET
    employee_ni: Union[Unset, float] = UNSET
    employer_ni: Union[Unset, float] = UNSET
    net_ni: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        ni_category = self.ni_category
        as_director = self.as_director
        earnings_upto_including_lel = self.earnings_upto_including_lel
        earnings_above_lel_upto_including_pt = self.earnings_above_lel_upto_including_pt
        earnings_above_pt_upto_including_st = self.earnings_above_pt_upto_including_st
        earnings_above_pt_upto_including_uel = self.earnings_above_pt_upto_including_uel
        earnings_above_st_upto_including_uel = self.earnings_above_st_upto_including_uel
        earnings_above_st_upto_including_fust = (
            self.earnings_above_st_upto_including_fust
        )
        earnings_above_fust_upto_including_uel = (
            self.earnings_above_fust_upto_including_uel
        )
        earnings_above_uel = self.earnings_above_uel
        employee_ni_gross = self.employee_ni_gross
        employee_ni_rebate = self.employee_ni_rebate
        employer_ni_gross = self.employer_ni_gross
        employer_ni_rebate = self.employer_ni_rebate
        employee_ni = self.employee_ni
        employer_ni = self.employer_ni
        net_ni = self.net_ni

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if ni_category is not UNSET:
            field_dict["niCategory"] = ni_category
        if as_director is not UNSET:
            field_dict["asDirector"] = as_director
        if earnings_upto_including_lel is not UNSET:
            field_dict["earningsUptoIncludingLEL"] = earnings_upto_including_lel
        if earnings_above_lel_upto_including_pt is not UNSET:
            field_dict[
                "earningsAboveLELUptoIncludingPT"
            ] = earnings_above_lel_upto_including_pt
        if earnings_above_pt_upto_including_st is not UNSET:
            field_dict[
                "earningsAbovePTUptoIncludingST"
            ] = earnings_above_pt_upto_including_st
        if earnings_above_pt_upto_including_uel is not UNSET:
            field_dict[
                "earningsAbovePTUptoIncludingUEL"
            ] = earnings_above_pt_upto_including_uel
        if earnings_above_st_upto_including_uel is not UNSET:
            field_dict[
                "earningsAboveSTUptoIncludingUEL"
            ] = earnings_above_st_upto_including_uel
        if earnings_above_st_upto_including_fust is not UNSET:
            field_dict[
                "earningsAboveSTUptoIncludingFUST"
            ] = earnings_above_st_upto_including_fust
        if earnings_above_fust_upto_including_uel is not UNSET:
            field_dict[
                "earningsAboveFUSTUptoIncludingUEL"
            ] = earnings_above_fust_upto_including_uel
        if earnings_above_uel is not UNSET:
            field_dict["earningsAboveUEL"] = earnings_above_uel
        if employee_ni_gross is not UNSET:
            field_dict["employeeNiGross"] = employee_ni_gross
        if employee_ni_rebate is not UNSET:
            field_dict["employeeNiRebate"] = employee_ni_rebate
        if employer_ni_gross is not UNSET:
            field_dict["employerNiGross"] = employer_ni_gross
        if employer_ni_rebate is not UNSET:
            field_dict["employerNiRebate"] = employer_ni_rebate
        if employee_ni is not UNSET:
            field_dict["employeeNi"] = employee_ni
        if employer_ni is not UNSET:
            field_dict["employerNi"] = employer_ni
        if net_ni is not UNSET:
            field_dict["netNi"] = net_ni

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        ni_category = d.pop("niCategory", UNSET)

        as_director = d.pop("asDirector", UNSET)

        earnings_upto_including_lel = d.pop("earningsUptoIncludingLEL", UNSET)

        earnings_above_lel_upto_including_pt = d.pop(
            "earningsAboveLELUptoIncludingPT", UNSET
        )

        earnings_above_pt_upto_including_st = d.pop(
            "earningsAbovePTUptoIncludingST", UNSET
        )

        earnings_above_pt_upto_including_uel = d.pop(
            "earningsAbovePTUptoIncludingUEL", UNSET
        )

        earnings_above_st_upto_including_uel = d.pop(
            "earningsAboveSTUptoIncludingUEL", UNSET
        )

        earnings_above_st_upto_including_fust = d.pop(
            "earningsAboveSTUptoIncludingFUST", UNSET
        )

        earnings_above_fust_upto_including_uel = d.pop(
            "earningsAboveFUSTUptoIncludingUEL", UNSET
        )

        earnings_above_uel = d.pop("earningsAboveUEL", UNSET)

        employee_ni_gross = d.pop("employeeNiGross", UNSET)

        employee_ni_rebate = d.pop("employeeNiRebate", UNSET)

        employer_ni_gross = d.pop("employerNiGross", UNSET)

        employer_ni_rebate = d.pop("employerNiRebate", UNSET)

        employee_ni = d.pop("employeeNi", UNSET)

        employer_ni = d.pop("employerNi", UNSET)

        net_ni = d.pop("netNi", UNSET)

        national_insurance_calculation_base = cls(
            ni_category=ni_category,
            as_director=as_director,
            earnings_upto_including_lel=earnings_upto_including_lel,
            earnings_above_lel_upto_including_pt=earnings_above_lel_upto_including_pt,
            earnings_above_pt_upto_including_st=earnings_above_pt_upto_including_st,
            earnings_above_pt_upto_including_uel=earnings_above_pt_upto_including_uel,
            earnings_above_st_upto_including_uel=earnings_above_st_upto_including_uel,
            earnings_above_st_upto_including_fust=earnings_above_st_upto_including_fust,
            earnings_above_fust_upto_including_uel=earnings_above_fust_upto_including_uel,
            earnings_above_uel=earnings_above_uel,
            employee_ni_gross=employee_ni_gross,
            employee_ni_rebate=employee_ni_rebate,
            employer_ni_gross=employer_ni_gross,
            employer_ni_rebate=employer_ni_rebate,
            employee_ni=employee_ni,
            employer_ni=employer_ni,
            net_ni=net_ni,
        )

        return national_insurance_calculation_base
