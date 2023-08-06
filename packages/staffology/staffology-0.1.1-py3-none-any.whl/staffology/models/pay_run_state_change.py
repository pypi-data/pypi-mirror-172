from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.pay_run_state import PayRunState
from ..models.pay_run_state_change_reason import PayRunStateChangeReason
from ..types import UNSET, Unset

T = TypeVar("T", bound="PayRunStateChange")


@attr.s(auto_attribs=True)
class PayRunStateChange:
    """
    Attributes:
        state (Union[Unset, PayRunState]): The state of the payrun. You would set this value when updating a payrun to
            finalise or re-open it.
            Other states are used with Bureau functionality which isn't currently generally available.
        reason (Union[Unset, PayRunStateChangeReason]):
        reason_text (Union[Unset, None, str]): A free-form text field for a reason for the change of state.
    """

    state: Union[Unset, PayRunState] = UNSET
    reason: Union[Unset, PayRunStateChangeReason] = UNSET
    reason_text: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        state: Union[Unset, str] = UNSET
        if not isinstance(self.state, Unset):
            state = self.state.value

        reason: Union[Unset, str] = UNSET
        if not isinstance(self.reason, Unset):
            reason = self.reason.value

        reason_text = self.reason_text

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if state is not UNSET:
            field_dict["state"] = state
        if reason is not UNSET:
            field_dict["reason"] = reason
        if reason_text is not UNSET:
            field_dict["reasonText"] = reason_text

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _state = d.pop("state", UNSET)
        state: Union[Unset, PayRunState]
        if isinstance(_state, Unset):
            state = UNSET
        else:
            state = PayRunState(_state)

        _reason = d.pop("reason", UNSET)
        reason: Union[Unset, PayRunStateChangeReason]
        if isinstance(_reason, Unset):
            reason = UNSET
        else:
            reason = PayRunStateChangeReason(_reason)

        reason_text = d.pop("reasonText", UNSET)

        pay_run_state_change = cls(
            state=state,
            reason=reason,
            reason_text=reason_text,
        )

        return pay_run_state_change
