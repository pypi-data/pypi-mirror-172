from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.payslip_line_type import PayslipLineType
from ..types import UNSET, Unset

T = TypeVar("T", bound="PayslipLine")


@attr.s(auto_attribs=True)
class PayslipLine:
    """
    Attributes:
        type (Union[Unset, PayslipLineType]):
        code (Union[Unset, None, str]):
        description (Union[Unset, None, str]):
        secondary_description (Union[Unset, None, str]):
        value (Union[Unset, float]):
        multiplier (Union[Unset, None, float]): [readonly] If the Code is a multiplier code then this is the multiplier.
            Value has already been calculated so this is just for reference
        attachment_order_id (Union[Unset, None, str]): [readonly] The Id of the associated AttachmentOrder. Only
            included if the Code is AEO
        pension_id (Union[Unset, None, str]): [readonly] The Id of the associated Pension. Only included if the Code is
            PENSION, PENSIONSS or PENSIONRAS
        loan_id (Union[Unset, None, str]): [readonly] The Id of the associated Loan, if any.
        currency_symbol (Union[Unset, None, str]):
        formatted_value (Union[Unset, None, str]):
        is_net_to_gross (Union[Unset, bool]): If the PayLine is a fixed ammount addition without multiplier then this
            property may be set to true so that the amount of the addition to be considered a take home pay target.
        target_net_to_gross_value (Union[Unset, None, float]): The orginal net fixed addition amount that is considered
            to be a take home pay target.
        has_secondary_description (Union[Unset, bool]):
    """

    type: Union[Unset, PayslipLineType] = UNSET
    code: Union[Unset, None, str] = UNSET
    description: Union[Unset, None, str] = UNSET
    secondary_description: Union[Unset, None, str] = UNSET
    value: Union[Unset, float] = UNSET
    multiplier: Union[Unset, None, float] = UNSET
    attachment_order_id: Union[Unset, None, str] = UNSET
    pension_id: Union[Unset, None, str] = UNSET
    loan_id: Union[Unset, None, str] = UNSET
    currency_symbol: Union[Unset, None, str] = UNSET
    formatted_value: Union[Unset, None, str] = UNSET
    is_net_to_gross: Union[Unset, bool] = UNSET
    target_net_to_gross_value: Union[Unset, None, float] = UNSET
    has_secondary_description: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        code = self.code
        description = self.description
        secondary_description = self.secondary_description
        value = self.value
        multiplier = self.multiplier
        attachment_order_id = self.attachment_order_id
        pension_id = self.pension_id
        loan_id = self.loan_id
        currency_symbol = self.currency_symbol
        formatted_value = self.formatted_value
        is_net_to_gross = self.is_net_to_gross
        target_net_to_gross_value = self.target_net_to_gross_value
        has_secondary_description = self.has_secondary_description

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if code is not UNSET:
            field_dict["code"] = code
        if description is not UNSET:
            field_dict["description"] = description
        if secondary_description is not UNSET:
            field_dict["secondaryDescription"] = secondary_description
        if value is not UNSET:
            field_dict["value"] = value
        if multiplier is not UNSET:
            field_dict["multiplier"] = multiplier
        if attachment_order_id is not UNSET:
            field_dict["attachmentOrderId"] = attachment_order_id
        if pension_id is not UNSET:
            field_dict["pensionId"] = pension_id
        if loan_id is not UNSET:
            field_dict["loanId"] = loan_id
        if currency_symbol is not UNSET:
            field_dict["currencySymbol"] = currency_symbol
        if formatted_value is not UNSET:
            field_dict["formattedValue"] = formatted_value
        if is_net_to_gross is not UNSET:
            field_dict["isNetToGross"] = is_net_to_gross
        if target_net_to_gross_value is not UNSET:
            field_dict["targetNetToGrossValue"] = target_net_to_gross_value
        if has_secondary_description is not UNSET:
            field_dict["hasSecondaryDescription"] = has_secondary_description

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _type = d.pop("type", UNSET)
        type: Union[Unset, PayslipLineType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = PayslipLineType(_type)

        code = d.pop("code", UNSET)

        description = d.pop("description", UNSET)

        secondary_description = d.pop("secondaryDescription", UNSET)

        value = d.pop("value", UNSET)

        multiplier = d.pop("multiplier", UNSET)

        attachment_order_id = d.pop("attachmentOrderId", UNSET)

        pension_id = d.pop("pensionId", UNSET)

        loan_id = d.pop("loanId", UNSET)

        currency_symbol = d.pop("currencySymbol", UNSET)

        formatted_value = d.pop("formattedValue", UNSET)

        is_net_to_gross = d.pop("isNetToGross", UNSET)

        target_net_to_gross_value = d.pop("targetNetToGrossValue", UNSET)

        has_secondary_description = d.pop("hasSecondaryDescription", UNSET)

        payslip_line = cls(
            type=type,
            code=code,
            description=description,
            secondary_description=secondary_description,
            value=value,
            multiplier=multiplier,
            attachment_order_id=attachment_order_id,
            pension_id=pension_id,
            loan_id=loan_id,
            currency_symbol=currency_symbol,
            formatted_value=formatted_value,
            is_net_to_gross=is_net_to_gross,
            target_net_to_gross_value=target_net_to_gross_value,
            has_secondary_description=has_secondary_description,
        )

        return payslip_line
