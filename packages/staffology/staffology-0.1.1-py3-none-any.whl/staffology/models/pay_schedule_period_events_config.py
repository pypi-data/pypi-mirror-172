from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PaySchedulePeriodEventsConfig")


@attr.s(auto_attribs=True)
class PaySchedulePeriodEventsConfig:
    """Only applicable if Bureau functionality is enabled. Defines the number of days each event occurs before the Payment
    Date.

        Attributes:
            submit_for_processing (Union[Unset, int]):
            send_for_approval (Union[Unset, int]):
            approval (Union[Unset, int]):
            finalise (Union[Unset, int]):
            send_pay_slip (Union[Unset, int]):
            submit_rti (Union[Unset, int]):
    """

    submit_for_processing: Union[Unset, int] = UNSET
    send_for_approval: Union[Unset, int] = UNSET
    approval: Union[Unset, int] = UNSET
    finalise: Union[Unset, int] = UNSET
    send_pay_slip: Union[Unset, int] = UNSET
    submit_rti: Union[Unset, int] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        submit_for_processing = self.submit_for_processing
        send_for_approval = self.send_for_approval
        approval = self.approval
        finalise = self.finalise
        send_pay_slip = self.send_pay_slip
        submit_rti = self.submit_rti

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if submit_for_processing is not UNSET:
            field_dict["SubmitForProcessing"] = submit_for_processing
        if send_for_approval is not UNSET:
            field_dict["SendForApproval"] = send_for_approval
        if approval is not UNSET:
            field_dict["Approval"] = approval
        if finalise is not UNSET:
            field_dict["Finalise"] = finalise
        if send_pay_slip is not UNSET:
            field_dict["SendPaySlip"] = send_pay_slip
        if submit_rti is not UNSET:
            field_dict["SubmitRti"] = submit_rti

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        submit_for_processing = d.pop("SubmitForProcessing", UNSET)

        send_for_approval = d.pop("SendForApproval", UNSET)

        approval = d.pop("Approval", UNSET)

        finalise = d.pop("Finalise", UNSET)

        send_pay_slip = d.pop("SendPaySlip", UNSET)

        submit_rti = d.pop("SubmitRti", UNSET)

        pay_schedule_period_events_config = cls(
            submit_for_processing=submit_for_processing,
            send_for_approval=send_for_approval,
            approval=approval,
            finalise=finalise,
            send_pay_slip=send_pay_slip,
            submit_rti=submit_rti,
        )

        return pay_schedule_period_events_config
