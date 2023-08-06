import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.audit_event_action import AuditEventAction
from ..models.entity_type import EntityType
from ..models.field_modification import FieldModification
from ..types import UNSET, Unset

T = TypeVar("T", bound="ChangeSummary")


@attr.s(auto_attribs=True)
class ChangeSummary:
    """
    Attributes:
        id (Union[Unset, str]):
        audit_id (Union[Unset, str]):
        date (Union[Unset, datetime.date]):
        name (Union[Unset, None, str]):
        action_performed (Union[Unset, AuditEventAction]):
        entity_type (Union[Unset, EntityType]): [readonly] Specifies the entity for which audit logs need to retrieved
        entity_id (Union[Unset, str]): Id of the underlying entity
        employee_unique_id (Union[Unset, str]): Unique id of the employee this operation belongs to
        action_performed_by (Union[Unset, None, str]):
        action_performed_on (Union[Unset, None, str]):
        unique_id (Union[Unset, str]): Unique id of the owner this request belongs to
        parent_event_type (Union[Unset, None, str]):
        modifications (Union[Unset, None, List[FieldModification]]):
    """

    id: Union[Unset, str] = UNSET
    audit_id: Union[Unset, str] = UNSET
    date: Union[Unset, datetime.date] = UNSET
    name: Union[Unset, None, str] = UNSET
    action_performed: Union[Unset, AuditEventAction] = UNSET
    entity_type: Union[Unset, EntityType] = UNSET
    entity_id: Union[Unset, str] = UNSET
    employee_unique_id: Union[Unset, str] = UNSET
    action_performed_by: Union[Unset, None, str] = UNSET
    action_performed_on: Union[Unset, None, str] = UNSET
    unique_id: Union[Unset, str] = UNSET
    parent_event_type: Union[Unset, None, str] = UNSET
    modifications: Union[Unset, None, List[FieldModification]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        audit_id = self.audit_id
        date: Union[Unset, str] = UNSET
        if not isinstance(self.date, Unset):
            date = self.date.isoformat()

        name = self.name
        action_performed: Union[Unset, str] = UNSET
        if not isinstance(self.action_performed, Unset):
            action_performed = self.action_performed.value

        entity_type: Union[Unset, str] = UNSET
        if not isinstance(self.entity_type, Unset):
            entity_type = self.entity_type.value

        entity_id = self.entity_id
        employee_unique_id = self.employee_unique_id
        action_performed_by = self.action_performed_by
        action_performed_on = self.action_performed_on
        unique_id = self.unique_id
        parent_event_type = self.parent_event_type
        modifications: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.modifications, Unset):
            if self.modifications is None:
                modifications = None
            else:
                modifications = []
                for modifications_item_data in self.modifications:
                    modifications_item = modifications_item_data.to_dict()

                    modifications.append(modifications_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if audit_id is not UNSET:
            field_dict["auditId"] = audit_id
        if date is not UNSET:
            field_dict["date"] = date
        if name is not UNSET:
            field_dict["name"] = name
        if action_performed is not UNSET:
            field_dict["actionPerformed"] = action_performed
        if entity_type is not UNSET:
            field_dict["entityType"] = entity_type
        if entity_id is not UNSET:
            field_dict["entityId"] = entity_id
        if employee_unique_id is not UNSET:
            field_dict["employeeUniqueId"] = employee_unique_id
        if action_performed_by is not UNSET:
            field_dict["actionPerformedBy"] = action_performed_by
        if action_performed_on is not UNSET:
            field_dict["actionPerformedOn"] = action_performed_on
        if unique_id is not UNSET:
            field_dict["uniqueId"] = unique_id
        if parent_event_type is not UNSET:
            field_dict["parentEventType"] = parent_event_type
        if modifications is not UNSET:
            field_dict["modifications"] = modifications

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        audit_id = d.pop("auditId", UNSET)

        _date = d.pop("date", UNSET)
        date: Union[Unset, datetime.date]
        if isinstance(_date, Unset):
            date = UNSET
        else:
            date = isoparse(_date).date()

        name = d.pop("name", UNSET)

        _action_performed = d.pop("actionPerformed", UNSET)
        action_performed: Union[Unset, AuditEventAction]
        if isinstance(_action_performed, Unset):
            action_performed = UNSET
        else:
            action_performed = AuditEventAction(_action_performed)

        _entity_type = d.pop("entityType", UNSET)
        entity_type: Union[Unset, EntityType]
        if isinstance(_entity_type, Unset):
            entity_type = UNSET
        else:
            entity_type = EntityType(_entity_type)

        entity_id = d.pop("entityId", UNSET)

        employee_unique_id = d.pop("employeeUniqueId", UNSET)

        action_performed_by = d.pop("actionPerformedBy", UNSET)

        action_performed_on = d.pop("actionPerformedOn", UNSET)

        unique_id = d.pop("uniqueId", UNSET)

        parent_event_type = d.pop("parentEventType", UNSET)

        modifications = []
        _modifications = d.pop("modifications", UNSET)
        for modifications_item_data in _modifications or []:
            modifications_item = FieldModification.from_dict(modifications_item_data)

            modifications.append(modifications_item)

        change_summary = cls(
            id=id,
            audit_id=audit_id,
            date=date,
            name=name,
            action_performed=action_performed,
            entity_type=entity_type,
            entity_id=entity_id,
            employee_unique_id=employee_unique_id,
            action_performed_by=action_performed_by,
            action_performed_on=action_performed_on,
            unique_id=unique_id,
            parent_event_type=parent_event_type,
            modifications=modifications,
        )

        return change_summary
