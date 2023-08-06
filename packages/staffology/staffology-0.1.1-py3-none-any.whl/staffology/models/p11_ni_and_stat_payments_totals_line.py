from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="P11NiAndStatPaymentsTotalsLine")


@attr.s(auto_attribs=True)
class P11NiAndStatPaymentsTotalsLine:
    """Summary line for the NI Contributions and Statutory Payments table in the P11 Detailed report

    Attributes:
        to_lel (Union[Unset, float]): [readonly]
        lel_to_pt (Union[Unset, float]): [readonly]
        pt_to_uel (Union[Unset, float]): [readonly]
        ees_and_ers (Union[Unset, float]): [readonly]
        ees (Union[Unset, float]): [readonly]
        class_1a (Union[Unset, float]): [readonly]
        ssp (Union[Unset, float]): [readonly]
        smp (Union[Unset, float]): [readonly]
        spp (Union[Unset, float]): [readonly]
        shpp (Union[Unset, float]): [readonly]
        sap (Union[Unset, float]): [readonly]
        spbp (Union[Unset, float]): [readonly]
    """

    to_lel: Union[Unset, float] = UNSET
    lel_to_pt: Union[Unset, float] = UNSET
    pt_to_uel: Union[Unset, float] = UNSET
    ees_and_ers: Union[Unset, float] = UNSET
    ees: Union[Unset, float] = UNSET
    class_1a: Union[Unset, float] = UNSET
    ssp: Union[Unset, float] = UNSET
    smp: Union[Unset, float] = UNSET
    spp: Union[Unset, float] = UNSET
    shpp: Union[Unset, float] = UNSET
    sap: Union[Unset, float] = UNSET
    spbp: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        to_lel = self.to_lel
        lel_to_pt = self.lel_to_pt
        pt_to_uel = self.pt_to_uel
        ees_and_ers = self.ees_and_ers
        ees = self.ees
        class_1a = self.class_1a
        ssp = self.ssp
        smp = self.smp
        spp = self.spp
        shpp = self.shpp
        sap = self.sap
        spbp = self.spbp

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if to_lel is not UNSET:
            field_dict["toLel"] = to_lel
        if lel_to_pt is not UNSET:
            field_dict["lelToPt"] = lel_to_pt
        if pt_to_uel is not UNSET:
            field_dict["ptToUel"] = pt_to_uel
        if ees_and_ers is not UNSET:
            field_dict["eesAndErs"] = ees_and_ers
        if ees is not UNSET:
            field_dict["ees"] = ees
        if class_1a is not UNSET:
            field_dict["class1A"] = class_1a
        if ssp is not UNSET:
            field_dict["ssp"] = ssp
        if smp is not UNSET:
            field_dict["smp"] = smp
        if spp is not UNSET:
            field_dict["spp"] = spp
        if shpp is not UNSET:
            field_dict["shpp"] = shpp
        if sap is not UNSET:
            field_dict["sap"] = sap
        if spbp is not UNSET:
            field_dict["spbp"] = spbp

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        to_lel = d.pop("toLel", UNSET)

        lel_to_pt = d.pop("lelToPt", UNSET)

        pt_to_uel = d.pop("ptToUel", UNSET)

        ees_and_ers = d.pop("eesAndErs", UNSET)

        ees = d.pop("ees", UNSET)

        class_1a = d.pop("class1A", UNSET)

        ssp = d.pop("ssp", UNSET)

        smp = d.pop("smp", UNSET)

        spp = d.pop("spp", UNSET)

        shpp = d.pop("shpp", UNSET)

        sap = d.pop("sap", UNSET)

        spbp = d.pop("spbp", UNSET)

        p11_ni_and_stat_payments_totals_line = cls(
            to_lel=to_lel,
            lel_to_pt=lel_to_pt,
            pt_to_uel=pt_to_uel,
            ees_and_ers=ees_and_ers,
            ees=ees,
            class_1a=class_1a,
            ssp=ssp,
            smp=smp,
            spp=spp,
            shpp=shpp,
            sap=sap,
            spbp=spbp,
        )

        return p11_ni_and_stat_payments_totals_line
