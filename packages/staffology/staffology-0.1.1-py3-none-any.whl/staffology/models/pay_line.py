from typing import Any, Dict, List, Type, TypeVar, Union, cast

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PayLine")


@attr.s(auto_attribs=True)
class PayLine:
    """As well as the basic pay amount for an employee there are often additions and deductions such as bonuses.
    These additions and deductions are represented using this model.

        Attributes:
            value (Union[Unset, float]): The amount to add or deduct (whether it is a deduction or addition depends on the
                PayCode used).
                If the PayCode has a CalculationType other than FixedAmount then this field will be a percentage.
                If the PayCode has a MultiplierType other than None then this field will be readonly and automatically
                calculated.
            rate (Union[Unset, None, float]): If the related  PayCode has a MultiplierType other than None then this field
                will be used as the rate per day or hour. Otherwise it isn't used
            multiplier (Union[Unset, None, float]): If the related PayCode has a MultiplierType other than None then this
                field will be used as number of days or hours
            description (Union[Unset, None, str]): A freeform description to accompany this line. It will be displayed on
                the payslip.
            attachment_order_id (Union[Unset, None, str]): [readonly] The Id of the associated AttachmentOrder. Only
                included if the Code is AEO
            pension_id (Union[Unset, None, str]): [readonly] The Id of the associated Pension. Only included if the Code is
                PENSION, PENSIONSS or PENSIONRAS
            leave_id (Union[Unset, None, str]): [readonly] The Id of the associated Leave. Only included if the PayLine is a
                result of a Leave with Statutory pay
            loan_id (Union[Unset, None, str]): [readonly] The Id of the associated Loan, if any.
            leave_statutory_days_paid (Union[Unset, None, float]): [readonly] If the PayLine is a result of a Leave with
                Statutory Pay then this property tells you how many days they've been paid for (based on their Working Pattern).
            leave_statutory_weeks_paid (Union[Unset, None, float]): [readonly] If the PayLine is a result of a Leave with
                Statutory Pay then this property tells you how many weeks they've been paid for (based on their Working
                Pattern).
            code (Union[Unset, None, str]): The Code of the PayCode this line is assigned to. The PayCode determines the
                treatment of this line when it comes to NI, Tax and Pensions as well as whether it's a deduction or addition.
            tags (Union[Unset, None, List[str]]):
            child_id (Union[Unset, str]): This is nothing but the UniqueId of the model.
            is_net_to_gross (Union[Unset, bool]): If the PayLine is a fixed ammount addition without multiplier then this
                property may be set to true so that the amount of the addition to be considered a take home pay target.
            target_net_to_gross_value (Union[Unset, None, float]): The orginal net fixed addition amount that is considered
                to be a take home pay target.
            net_to_gross_discrepancy (Union[Unset, None, float]): The discrepancy between the targeted and the calculated
                grossed up value durig a net to gross calculation.
    """

    value: Union[Unset, float] = UNSET
    rate: Union[Unset, None, float] = UNSET
    multiplier: Union[Unset, None, float] = UNSET
    description: Union[Unset, None, str] = UNSET
    attachment_order_id: Union[Unset, None, str] = UNSET
    pension_id: Union[Unset, None, str] = UNSET
    leave_id: Union[Unset, None, str] = UNSET
    loan_id: Union[Unset, None, str] = UNSET
    leave_statutory_days_paid: Union[Unset, None, float] = UNSET
    leave_statutory_weeks_paid: Union[Unset, None, float] = UNSET
    code: Union[Unset, None, str] = UNSET
    tags: Union[Unset, None, List[str]] = UNSET
    child_id: Union[Unset, str] = UNSET
    is_net_to_gross: Union[Unset, bool] = UNSET
    target_net_to_gross_value: Union[Unset, None, float] = UNSET
    net_to_gross_discrepancy: Union[Unset, None, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        value = self.value
        rate = self.rate
        multiplier = self.multiplier
        description = self.description
        attachment_order_id = self.attachment_order_id
        pension_id = self.pension_id
        leave_id = self.leave_id
        loan_id = self.loan_id
        leave_statutory_days_paid = self.leave_statutory_days_paid
        leave_statutory_weeks_paid = self.leave_statutory_weeks_paid
        code = self.code
        tags: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.tags, Unset):
            if self.tags is None:
                tags = None
            else:
                tags = self.tags

        child_id = self.child_id
        is_net_to_gross = self.is_net_to_gross
        target_net_to_gross_value = self.target_net_to_gross_value
        net_to_gross_discrepancy = self.net_to_gross_discrepancy

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if value is not UNSET:
            field_dict["value"] = value
        if rate is not UNSET:
            field_dict["rate"] = rate
        if multiplier is not UNSET:
            field_dict["multiplier"] = multiplier
        if description is not UNSET:
            field_dict["description"] = description
        if attachment_order_id is not UNSET:
            field_dict["attachmentOrderId"] = attachment_order_id
        if pension_id is not UNSET:
            field_dict["pensionId"] = pension_id
        if leave_id is not UNSET:
            field_dict["leaveId"] = leave_id
        if loan_id is not UNSET:
            field_dict["loanId"] = loan_id
        if leave_statutory_days_paid is not UNSET:
            field_dict["leaveStatutoryDaysPaid"] = leave_statutory_days_paid
        if leave_statutory_weeks_paid is not UNSET:
            field_dict["leaveStatutoryWeeksPaid"] = leave_statutory_weeks_paid
        if code is not UNSET:
            field_dict["code"] = code
        if tags is not UNSET:
            field_dict["tags"] = tags
        if child_id is not UNSET:
            field_dict["childId"] = child_id
        if is_net_to_gross is not UNSET:
            field_dict["isNetToGross"] = is_net_to_gross
        if target_net_to_gross_value is not UNSET:
            field_dict["targetNetToGrossValue"] = target_net_to_gross_value
        if net_to_gross_discrepancy is not UNSET:
            field_dict["netToGrossDiscrepancy"] = net_to_gross_discrepancy

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        value = d.pop("value", UNSET)

        rate = d.pop("rate", UNSET)

        multiplier = d.pop("multiplier", UNSET)

        description = d.pop("description", UNSET)

        attachment_order_id = d.pop("attachmentOrderId", UNSET)

        pension_id = d.pop("pensionId", UNSET)

        leave_id = d.pop("leaveId", UNSET)

        loan_id = d.pop("loanId", UNSET)

        leave_statutory_days_paid = d.pop("leaveStatutoryDaysPaid", UNSET)

        leave_statutory_weeks_paid = d.pop("leaveStatutoryWeeksPaid", UNSET)

        code = d.pop("code", UNSET)

        tags = cast(List[str], d.pop("tags", UNSET))

        child_id = d.pop("childId", UNSET)

        is_net_to_gross = d.pop("isNetToGross", UNSET)

        target_net_to_gross_value = d.pop("targetNetToGrossValue", UNSET)

        net_to_gross_discrepancy = d.pop("netToGrossDiscrepancy", UNSET)

        pay_line = cls(
            value=value,
            rate=rate,
            multiplier=multiplier,
            description=description,
            attachment_order_id=attachment_order_id,
            pension_id=pension_id,
            leave_id=leave_id,
            loan_id=loan_id,
            leave_statutory_days_paid=leave_statutory_days_paid,
            leave_statutory_weeks_paid=leave_statutory_weeks_paid,
            code=code,
            tags=tags,
            child_id=child_id,
            is_net_to_gross=is_net_to_gross,
            target_net_to_gross_value=target_net_to_gross_value,
            net_to_gross_discrepancy=net_to_gross_discrepancy,
        )

        return pay_line
