from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.background_task_status import BackgroundTaskStatus
from ..models.item import Item
from ..models.role import Role
from ..types import UNSET, Unset

T = TypeVar("T", bound="Invitation")


@attr.s(auto_attribs=True)
class Invitation:
    """Invitations are used to invite other users to access an existing Employer

    Attributes:
        email_address (str): The email address of the user that is being invited to access the Employer
        employer (Union[Unset, Item]):
        message (Union[Unset, None, str]): An optional message to include in the email sent to the EmailAddress
        role (Union[Unset, Role]):
        email_id (Union[Unset, None, str]):
        email_status (Union[Unset, BackgroundTaskStatus]):
        invited_by (Union[Unset, Item]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    email_address: str
    employer: Union[Unset, Item] = UNSET
    message: Union[Unset, None, str] = UNSET
    role: Union[Unset, Role] = UNSET
    email_id: Union[Unset, None, str] = UNSET
    email_status: Union[Unset, BackgroundTaskStatus] = UNSET
    invited_by: Union[Unset, Item] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        email_address = self.email_address
        employer: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employer, Unset):
            employer = self.employer.to_dict()

        message = self.message
        role: Union[Unset, str] = UNSET
        if not isinstance(self.role, Unset):
            role = self.role.value

        email_id = self.email_id
        email_status: Union[Unset, str] = UNSET
        if not isinstance(self.email_status, Unset):
            email_status = self.email_status.value

        invited_by: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.invited_by, Unset):
            invited_by = self.invited_by.to_dict()

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "emailAddress": email_address,
            }
        )
        if employer is not UNSET:
            field_dict["employer"] = employer
        if message is not UNSET:
            field_dict["message"] = message
        if role is not UNSET:
            field_dict["role"] = role
        if email_id is not UNSET:
            field_dict["emailId"] = email_id
        if email_status is not UNSET:
            field_dict["emailStatus"] = email_status
        if invited_by is not UNSET:
            field_dict["invitedBy"] = invited_by
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        email_address = d.pop("emailAddress")

        _employer = d.pop("employer", UNSET)
        employer: Union[Unset, Item]
        if isinstance(_employer, Unset):
            employer = UNSET
        else:
            employer = Item.from_dict(_employer)

        message = d.pop("message", UNSET)

        _role = d.pop("role", UNSET)
        role: Union[Unset, Role]
        if isinstance(_role, Unset):
            role = UNSET
        else:
            role = Role(_role)

        email_id = d.pop("emailId", UNSET)

        _email_status = d.pop("emailStatus", UNSET)
        email_status: Union[Unset, BackgroundTaskStatus]
        if isinstance(_email_status, Unset):
            email_status = UNSET
        else:
            email_status = BackgroundTaskStatus(_email_status)

        _invited_by = d.pop("invitedBy", UNSET)
        invited_by: Union[Unset, Item]
        if isinstance(_invited_by, Unset):
            invited_by = UNSET
        else:
            invited_by = Item.from_dict(_invited_by)

        id = d.pop("id", UNSET)

        invitation = cls(
            email_address=email_address,
            employer=employer,
            message=message,
            role=role,
            email_id=email_id,
            email_status=email_status,
            invited_by=invited_by,
            id=id,
        )

        return invitation
