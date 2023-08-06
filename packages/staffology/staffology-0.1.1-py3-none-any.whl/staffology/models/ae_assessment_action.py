from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.ae_action import AeAction
from ..models.ae_employee_state import AeEmployeeState
from ..models.ae_statutory_letter import AeStatutoryLetter
from ..types import UNSET, Unset

T = TypeVar("T", bound="AeAssessmentAction")


@attr.s(auto_attribs=True)
class AeAssessmentAction:
    """
    Attributes:
        action (Union[Unset, AeAction]):
        employee_state (Union[Unset, AeEmployeeState]):
        action_completed (Union[Unset, bool]): [readonly] Indicates whether or not the required action was successfully
            completed
        action_completed_message (Union[Unset, None, str]): [readonly] Gives further information about the action taken
            or the reason if wasn't successfully completed
        required_letter (Union[Unset, AeStatutoryLetter]):
        pension_scheme_id (Union[Unset, str]): [readonly] The PensionSchemeId that a completed action relates to
        worker_group_id (Union[Unset, str]): [readonly] The WorkerGroupId that a completed action relates to
        letter_not_yet_sent (Union[Unset, bool]): [readonly] Indicates whether or not any required letter has been sent
    """

    action: Union[Unset, AeAction] = UNSET
    employee_state: Union[Unset, AeEmployeeState] = UNSET
    action_completed: Union[Unset, bool] = UNSET
    action_completed_message: Union[Unset, None, str] = UNSET
    required_letter: Union[Unset, AeStatutoryLetter] = UNSET
    pension_scheme_id: Union[Unset, str] = UNSET
    worker_group_id: Union[Unset, str] = UNSET
    letter_not_yet_sent: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        action: Union[Unset, str] = UNSET
        if not isinstance(self.action, Unset):
            action = self.action.value

        employee_state: Union[Unset, str] = UNSET
        if not isinstance(self.employee_state, Unset):
            employee_state = self.employee_state.value

        action_completed = self.action_completed
        action_completed_message = self.action_completed_message
        required_letter: Union[Unset, str] = UNSET
        if not isinstance(self.required_letter, Unset):
            required_letter = self.required_letter.value

        pension_scheme_id = self.pension_scheme_id
        worker_group_id = self.worker_group_id
        letter_not_yet_sent = self.letter_not_yet_sent

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if action is not UNSET:
            field_dict["action"] = action
        if employee_state is not UNSET:
            field_dict["employeeState"] = employee_state
        if action_completed is not UNSET:
            field_dict["actionCompleted"] = action_completed
        if action_completed_message is not UNSET:
            field_dict["actionCompletedMessage"] = action_completed_message
        if required_letter is not UNSET:
            field_dict["requiredLetter"] = required_letter
        if pension_scheme_id is not UNSET:
            field_dict["pensionSchemeId"] = pension_scheme_id
        if worker_group_id is not UNSET:
            field_dict["workerGroupId"] = worker_group_id
        if letter_not_yet_sent is not UNSET:
            field_dict["letterNotYetSent"] = letter_not_yet_sent

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _action = d.pop("action", UNSET)
        action: Union[Unset, AeAction]
        if isinstance(_action, Unset):
            action = UNSET
        else:
            action = AeAction(_action)

        _employee_state = d.pop("employeeState", UNSET)
        employee_state: Union[Unset, AeEmployeeState]
        if isinstance(_employee_state, Unset):
            employee_state = UNSET
        else:
            employee_state = AeEmployeeState(_employee_state)

        action_completed = d.pop("actionCompleted", UNSET)

        action_completed_message = d.pop("actionCompletedMessage", UNSET)

        _required_letter = d.pop("requiredLetter", UNSET)
        required_letter: Union[Unset, AeStatutoryLetter]
        if isinstance(_required_letter, Unset):
            required_letter = UNSET
        else:
            required_letter = AeStatutoryLetter(_required_letter)

        pension_scheme_id = d.pop("pensionSchemeId", UNSET)

        worker_group_id = d.pop("workerGroupId", UNSET)

        letter_not_yet_sent = d.pop("letterNotYetSent", UNSET)

        ae_assessment_action = cls(
            action=action,
            employee_state=employee_state,
            action_completed=action_completed,
            action_completed_message=action_completed_message,
            required_letter=required_letter,
            pension_scheme_id=pension_scheme_id,
            worker_group_id=worker_group_id,
            letter_not_yet_sent=letter_not_yet_sent,
        )

        return ae_assessment_action
