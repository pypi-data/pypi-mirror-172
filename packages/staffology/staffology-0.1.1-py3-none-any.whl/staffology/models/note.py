import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.item import Item
from ..models.note_type import NoteType
from ..types import UNSET, Unset

T = TypeVar("T", bound="Note")


@attr.s(auto_attribs=True)
class Note:
    """Used to represent a Note for an Employee

    Attributes:
        note_date (Union[Unset, datetime.date]): The date of the note
        note_text (Union[Unset, None, str]): Note text
        created_by (Union[Unset, None, str]): [readonly] The email address of the user that create the Note
        updated_by (Union[Unset, None, str]): [readonly] The email address of the user that last updated the Note
        type (Union[Unset, NoteType]):
        document_count (Union[Unset, int]): [readonly] The number of attachments associated with this model
        documents (Union[Unset, None, List[Item]]): [readonly] The attachments associated with this model
        employee (Union[Unset, Item]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    note_date: Union[Unset, datetime.date] = UNSET
    note_text: Union[Unset, None, str] = UNSET
    created_by: Union[Unset, None, str] = UNSET
    updated_by: Union[Unset, None, str] = UNSET
    type: Union[Unset, NoteType] = UNSET
    document_count: Union[Unset, int] = UNSET
    documents: Union[Unset, None, List[Item]] = UNSET
    employee: Union[Unset, Item] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        note_date: Union[Unset, str] = UNSET
        if not isinstance(self.note_date, Unset):
            note_date = self.note_date.isoformat()

        note_text = self.note_text
        created_by = self.created_by
        updated_by = self.updated_by
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        document_count = self.document_count
        documents: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.documents, Unset):
            if self.documents is None:
                documents = None
            else:
                documents = []
                for documents_item_data in self.documents:
                    documents_item = documents_item_data.to_dict()

                    documents.append(documents_item)

        employee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employee, Unset):
            employee = self.employee.to_dict()

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if note_date is not UNSET:
            field_dict["noteDate"] = note_date
        if note_text is not UNSET:
            field_dict["noteText"] = note_text
        if created_by is not UNSET:
            field_dict["createdBy"] = created_by
        if updated_by is not UNSET:
            field_dict["updatedBy"] = updated_by
        if type is not UNSET:
            field_dict["type"] = type
        if document_count is not UNSET:
            field_dict["documentCount"] = document_count
        if documents is not UNSET:
            field_dict["documents"] = documents
        if employee is not UNSET:
            field_dict["employee"] = employee
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _note_date = d.pop("noteDate", UNSET)
        note_date: Union[Unset, datetime.date]
        if isinstance(_note_date, Unset):
            note_date = UNSET
        else:
            note_date = isoparse(_note_date).date()

        note_text = d.pop("noteText", UNSET)

        created_by = d.pop("createdBy", UNSET)

        updated_by = d.pop("updatedBy", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, NoteType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = NoteType(_type)

        document_count = d.pop("documentCount", UNSET)

        documents = []
        _documents = d.pop("documents", UNSET)
        for documents_item_data in _documents or []:
            documents_item = Item.from_dict(documents_item_data)

            documents.append(documents_item)

        _employee = d.pop("employee", UNSET)
        employee: Union[Unset, Item]
        if isinstance(_employee, Unset):
            employee = UNSET
        else:
            employee = Item.from_dict(_employee)

        id = d.pop("id", UNSET)

        note = cls(
            note_date=note_date,
            note_text=note_text,
            created_by=created_by,
            updated_by=updated_by,
            type=type,
            document_count=document_count,
            documents=documents,
            employee=employee,
            id=id,
        )

        return note
