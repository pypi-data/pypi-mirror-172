from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="P11DDescOther")


@attr.s(auto_attribs=True)
class P11DDescOther:
    """
    Attributes:
        desc (Union[Unset, None, str]):
        other (Union[Unset, None, str]):
        ann_val_pro_rata (Union[Unset, None, str]):
        gross_or_amt_forgone (Union[Unset, None, str]):
        cost_or_amt_forgone (Union[Unset, None, str]):
        made_good (Union[Unset, None, str]):
        cash_equiv_or_relevant_amt (Union[Unset, None, str]):
    """

    desc: Union[Unset, None, str] = UNSET
    other: Union[Unset, None, str] = UNSET
    ann_val_pro_rata: Union[Unset, None, str] = UNSET
    gross_or_amt_forgone: Union[Unset, None, str] = UNSET
    cost_or_amt_forgone: Union[Unset, None, str] = UNSET
    made_good: Union[Unset, None, str] = UNSET
    cash_equiv_or_relevant_amt: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        desc = self.desc
        other = self.other
        ann_val_pro_rata = self.ann_val_pro_rata
        gross_or_amt_forgone = self.gross_or_amt_forgone
        cost_or_amt_forgone = self.cost_or_amt_forgone
        made_good = self.made_good
        cash_equiv_or_relevant_amt = self.cash_equiv_or_relevant_amt

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
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
        desc = d.pop("desc", UNSET)

        other = d.pop("other", UNSET)

        ann_val_pro_rata = d.pop("annValProRata", UNSET)

        gross_or_amt_forgone = d.pop("grossOrAmtForgone", UNSET)

        cost_or_amt_forgone = d.pop("costOrAmtForgone", UNSET)

        made_good = d.pop("madeGood", UNSET)

        cash_equiv_or_relevant_amt = d.pop("cashEquivOrRelevantAmt", UNSET)

        p11d_desc_other = cls(
            desc=desc,
            other=other,
            ann_val_pro_rata=ann_val_pro_rata,
            gross_or_amt_forgone=gross_or_amt_forgone,
            cost_or_amt_forgone=cost_or_amt_forgone,
            made_good=made_good,
            cash_equiv_or_relevant_amt=cash_equiv_or_relevant_amt,
        )

        return p11d_desc_other
