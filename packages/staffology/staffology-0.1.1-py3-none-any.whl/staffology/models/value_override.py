from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.payroll_value_type import PayrollValueType
from ..types import UNSET, Unset

T = TypeVar("T", bound="ValueOverride")


@attr.s(auto_attribs=True)
class ValueOverride:
    """
    Attributes:
        type (Union[Unset, PayrollValueType]):
        value (Union[Unset, float]): The value to use in place of the original value
        original_value (Union[Unset, float]): [readonly] The original value
        note (Union[Unset, None, str]): The reason given for the overrride
        attachment_order_id (Union[Unset, None, str]): The Id of the AttachmentOrder. Only relevant if the Type is set
            to AttachmentOrderDeductions
        pension_id (Union[Unset, None, str]): The Id of the associated Pension. Only included if the Code is PENSION,
            PENSIONSS or PENSIONRAS
    """

    type: Union[Unset, PayrollValueType] = UNSET
    value: Union[Unset, float] = UNSET
    original_value: Union[Unset, float] = UNSET
    note: Union[Unset, None, str] = UNSET
    attachment_order_id: Union[Unset, None, str] = UNSET
    pension_id: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        value = self.value
        original_value = self.original_value
        note = self.note
        attachment_order_id = self.attachment_order_id
        pension_id = self.pension_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if type is not UNSET:
            field_dict["type"] = type
        if value is not UNSET:
            field_dict["value"] = value
        if original_value is not UNSET:
            field_dict["originalValue"] = original_value
        if note is not UNSET:
            field_dict["note"] = note
        if attachment_order_id is not UNSET:
            field_dict["attachmentOrderId"] = attachment_order_id
        if pension_id is not UNSET:
            field_dict["pensionId"] = pension_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _type = d.pop("type", UNSET)
        type: Union[Unset, PayrollValueType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = PayrollValueType(_type)

        value = d.pop("value", UNSET)

        original_value = d.pop("originalValue", UNSET)

        note = d.pop("note", UNSET)

        attachment_order_id = d.pop("attachmentOrderId", UNSET)

        pension_id = d.pop("pensionId", UNSET)

        value_override = cls(
            type=type,
            value=value,
            original_value=original_value,
            note=note,
            attachment_order_id=attachment_order_id,
            pension_id=pension_id,
        )

        return value_override
