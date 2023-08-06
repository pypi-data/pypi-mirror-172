from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.p11d_car_free_fuel_withdrawn import P11DCarFreeFuelWithdrawn
from ..types import UNSET, Unset

T = TypeVar("T", bound="P11DCar")


@attr.s(auto_attribs=True)
class P11DCar:
    """
    Attributes:
        make (Union[Unset, None, str]):
        registered (Union[Unset, None, str]):
        avail_from (Union[Unset, None, str]):
        avail_to (Union[Unset, None, str]):
        cc (Union[Unset, None, str]):
        fuel (Union[Unset, None, str]):
        c_o2 (Union[Unset, None, str]):
        zero_emission_mileage (Union[Unset, None, str]):
        no_app_co2_fig (Union[Unset, None, str]):
        list_ (Union[Unset, None, str]):
        accs (Union[Unset, None, str]):
        cap_cont (Union[Unset, None, str]):
        priv_use_pmt (Union[Unset, None, str]):
        fuel_withdrawn (Union[Unset, P11DCarFreeFuelWithdrawn]):
        cash_equiv_or_relevant_amt (Union[Unset, None, str]):
        fuel_cash_equiv_or_relevant_amt (Union[Unset, None, str]):
    """

    make: Union[Unset, None, str] = UNSET
    registered: Union[Unset, None, str] = UNSET
    avail_from: Union[Unset, None, str] = UNSET
    avail_to: Union[Unset, None, str] = UNSET
    cc: Union[Unset, None, str] = UNSET
    fuel: Union[Unset, None, str] = UNSET
    c_o2: Union[Unset, None, str] = UNSET
    zero_emission_mileage: Union[Unset, None, str] = UNSET
    no_app_co2_fig: Union[Unset, None, str] = UNSET
    list_: Union[Unset, None, str] = UNSET
    accs: Union[Unset, None, str] = UNSET
    cap_cont: Union[Unset, None, str] = UNSET
    priv_use_pmt: Union[Unset, None, str] = UNSET
    fuel_withdrawn: Union[Unset, P11DCarFreeFuelWithdrawn] = UNSET
    cash_equiv_or_relevant_amt: Union[Unset, None, str] = UNSET
    fuel_cash_equiv_or_relevant_amt: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        make = self.make
        registered = self.registered
        avail_from = self.avail_from
        avail_to = self.avail_to
        cc = self.cc
        fuel = self.fuel
        c_o2 = self.c_o2
        zero_emission_mileage = self.zero_emission_mileage
        no_app_co2_fig = self.no_app_co2_fig
        list_ = self.list_
        accs = self.accs
        cap_cont = self.cap_cont
        priv_use_pmt = self.priv_use_pmt
        fuel_withdrawn: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fuel_withdrawn, Unset):
            fuel_withdrawn = self.fuel_withdrawn.to_dict()

        cash_equiv_or_relevant_amt = self.cash_equiv_or_relevant_amt
        fuel_cash_equiv_or_relevant_amt = self.fuel_cash_equiv_or_relevant_amt

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if make is not UNSET:
            field_dict["make"] = make
        if registered is not UNSET:
            field_dict["registered"] = registered
        if avail_from is not UNSET:
            field_dict["availFrom"] = avail_from
        if avail_to is not UNSET:
            field_dict["availTo"] = avail_to
        if cc is not UNSET:
            field_dict["cc"] = cc
        if fuel is not UNSET:
            field_dict["fuel"] = fuel
        if c_o2 is not UNSET:
            field_dict["cO2"] = c_o2
        if zero_emission_mileage is not UNSET:
            field_dict["zeroEmissionMileage"] = zero_emission_mileage
        if no_app_co2_fig is not UNSET:
            field_dict["noAppCO2Fig"] = no_app_co2_fig
        if list_ is not UNSET:
            field_dict["list"] = list_
        if accs is not UNSET:
            field_dict["accs"] = accs
        if cap_cont is not UNSET:
            field_dict["capCont"] = cap_cont
        if priv_use_pmt is not UNSET:
            field_dict["privUsePmt"] = priv_use_pmt
        if fuel_withdrawn is not UNSET:
            field_dict["fuelWithdrawn"] = fuel_withdrawn
        if cash_equiv_or_relevant_amt is not UNSET:
            field_dict["cashEquivOrRelevantAmt"] = cash_equiv_or_relevant_amt
        if fuel_cash_equiv_or_relevant_amt is not UNSET:
            field_dict["fuelCashEquivOrRelevantAmt"] = fuel_cash_equiv_or_relevant_amt

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        make = d.pop("make", UNSET)

        registered = d.pop("registered", UNSET)

        avail_from = d.pop("availFrom", UNSET)

        avail_to = d.pop("availTo", UNSET)

        cc = d.pop("cc", UNSET)

        fuel = d.pop("fuel", UNSET)

        c_o2 = d.pop("cO2", UNSET)

        zero_emission_mileage = d.pop("zeroEmissionMileage", UNSET)

        no_app_co2_fig = d.pop("noAppCO2Fig", UNSET)

        list_ = d.pop("list", UNSET)

        accs = d.pop("accs", UNSET)

        cap_cont = d.pop("capCont", UNSET)

        priv_use_pmt = d.pop("privUsePmt", UNSET)

        _fuel_withdrawn = d.pop("fuelWithdrawn", UNSET)
        fuel_withdrawn: Union[Unset, P11DCarFreeFuelWithdrawn]
        if isinstance(_fuel_withdrawn, Unset):
            fuel_withdrawn = UNSET
        else:
            fuel_withdrawn = P11DCarFreeFuelWithdrawn.from_dict(_fuel_withdrawn)

        cash_equiv_or_relevant_amt = d.pop("cashEquivOrRelevantAmt", UNSET)

        fuel_cash_equiv_or_relevant_amt = d.pop("fuelCashEquivOrRelevantAmt", UNSET)

        p11d_car = cls(
            make=make,
            registered=registered,
            avail_from=avail_from,
            avail_to=avail_to,
            cc=cc,
            fuel=fuel,
            c_o2=c_o2,
            zero_emission_mileage=zero_emission_mileage,
            no_app_co2_fig=no_app_co2_fig,
            list_=list_,
            accs=accs,
            cap_cont=cap_cont,
            priv_use_pmt=priv_use_pmt,
            fuel_withdrawn=fuel_withdrawn,
            cash_equiv_or_relevant_amt=cash_equiv_or_relevant_amt,
            fuel_cash_equiv_or_relevant_amt=fuel_cash_equiv_or_relevant_amt,
        )

        return p11d_car
