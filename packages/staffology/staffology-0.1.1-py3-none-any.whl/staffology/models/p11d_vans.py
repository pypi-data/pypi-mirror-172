from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="P11DVans")


@attr.s(auto_attribs=True)
class P11DVans:
    """
    Attributes:
        fuel_cash_equiv_or_relevant_amt (Union[Unset, None, str]):
        type_letter (Union[Unset, None, str]):
        taxable_pmt (Union[Unset, None, str]):
        excess (Union[Unset, None, str]):
        taxable_pmt_or_relevant_amt (Union[Unset, None, str]):
        trading_org_ind (Union[Unset, None, str]):
        desc (Union[Unset, None, str]):
        other (Union[Unset, None, str]):
        ann_val_pro_rata (Union[Unset, None, str]):
        gross_or_amt_forgone (Union[Unset, None, str]):
        cost_or_amt_forgone (Union[Unset, None, str]):
        made_good (Union[Unset, None, str]):
        cash_equiv_or_relevant_amt (Union[Unset, None, str]):
    """

    fuel_cash_equiv_or_relevant_amt: Union[Unset, None, str] = UNSET
    type_letter: Union[Unset, None, str] = UNSET
    taxable_pmt: Union[Unset, None, str] = UNSET
    excess: Union[Unset, None, str] = UNSET
    taxable_pmt_or_relevant_amt: Union[Unset, None, str] = UNSET
    trading_org_ind: Union[Unset, None, str] = UNSET
    desc: Union[Unset, None, str] = UNSET
    other: Union[Unset, None, str] = UNSET
    ann_val_pro_rata: Union[Unset, None, str] = UNSET
    gross_or_amt_forgone: Union[Unset, None, str] = UNSET
    cost_or_amt_forgone: Union[Unset, None, str] = UNSET
    made_good: Union[Unset, None, str] = UNSET
    cash_equiv_or_relevant_amt: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        fuel_cash_equiv_or_relevant_amt = self.fuel_cash_equiv_or_relevant_amt
        type_letter = self.type_letter
        taxable_pmt = self.taxable_pmt
        excess = self.excess
        taxable_pmt_or_relevant_amt = self.taxable_pmt_or_relevant_amt
        trading_org_ind = self.trading_org_ind
        desc = self.desc
        other = self.other
        ann_val_pro_rata = self.ann_val_pro_rata
        gross_or_amt_forgone = self.gross_or_amt_forgone
        cost_or_amt_forgone = self.cost_or_amt_forgone
        made_good = self.made_good
        cash_equiv_or_relevant_amt = self.cash_equiv_or_relevant_amt

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if fuel_cash_equiv_or_relevant_amt is not UNSET:
            field_dict["fuelCashEquivOrRelevantAmt"] = fuel_cash_equiv_or_relevant_amt
        if type_letter is not UNSET:
            field_dict["typeLetter"] = type_letter
        if taxable_pmt is not UNSET:
            field_dict["taxablePmt"] = taxable_pmt
        if excess is not UNSET:
            field_dict["excess"] = excess
        if taxable_pmt_or_relevant_amt is not UNSET:
            field_dict["taxablePmtOrRelevantAmt"] = taxable_pmt_or_relevant_amt
        if trading_org_ind is not UNSET:
            field_dict["tradingOrgInd"] = trading_org_ind
        if desc is not UNSET:
            field_dict["desc"] = desc
        if other is not UNSET:
            field_dict["other"] = other
        if ann_val_pro_rata is not UNSET:
            field_dict["annValProRata"] = ann_val_pro_rata
        if gross_or_amt_forgone is not UNSET:
            field_dict["grossOrAmtForgone"] = gross_or_amt_forgone
        if cost_or_amt_forgone is not UNSET:
            field_dict["costOrAmtForgone"] = cost_or_amt_forgone
        if made_good is not UNSET:
            field_dict["madeGood"] = made_good
        if cash_equiv_or_relevant_amt is not UNSET:
            field_dict["cashEquivOrRelevantAmt"] = cash_equiv_or_relevant_amt

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        fuel_cash_equiv_or_relevant_amt = d.pop("fuelCashEquivOrRelevantAmt", UNSET)

        type_letter = d.pop("typeLetter", UNSET)

        taxable_pmt = d.pop("taxablePmt", UNSET)

        excess = d.pop("excess", UNSET)

        taxable_pmt_or_relevant_amt = d.pop("taxablePmtOrRelevantAmt", UNSET)

        trading_org_ind = d.pop("tradingOrgInd", UNSET)

        desc = d.pop("desc", UNSET)

        other = d.pop("other", UNSET)

        ann_val_pro_rata = d.pop("annValProRata", UNSET)

        gross_or_amt_forgone = d.pop("grossOrAmtForgone", UNSET)

        cost_or_amt_forgone = d.pop("costOrAmtForgone", UNSET)

        made_good = d.pop("madeGood", UNSET)

        cash_equiv_or_relevant_amt = d.pop("cashEquivOrRelevantAmt", UNSET)

        p11d_vans = cls(
            fuel_cash_equiv_or_relevant_amt=fuel_cash_equiv_or_relevant_amt,
            type_letter=type_letter,
            taxable_pmt=taxable_pmt,
            excess=excess,
            taxable_pmt_or_relevant_amt=taxable_pmt_or_relevant_amt,
            trading_org_ind=trading_org_ind,
            desc=desc,
            other=other,
            ann_val_pro_rata=ann_val_pro_rata,
            gross_or_amt_forgone=gross_or_amt_forgone,
            cost_or_amt_forgone=cost_or_amt_forgone,
            made_good=made_good,
            cash_equiv_or_relevant_amt=cash_equiv_or_relevant_amt,
        )

        return p11d_vans
