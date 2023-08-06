import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.right_to_work_document_type import RightToWorkDocumentType
from ..types import UNSET, Unset

T = TypeVar("T", bound="RightToWork")


@attr.s(auto_attribs=True)
class RightToWork:
    """
    Attributes:
        checked (Union[Unset, bool]):
        document_type (Union[Unset, RightToWorkDocumentType]):
        document_ref (Union[Unset, None, str]):
        document_expiry (Union[Unset, None, datetime.date]):
        note (Union[Unset, None, str]):
    """

    checked: Union[Unset, bool] = UNSET
    document_type: Union[Unset, RightToWorkDocumentType] = UNSET
    document_ref: Union[Unset, None, str] = UNSET
    document_expiry: Union[Unset, None, datetime.date] = UNSET
    note: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        checked = self.checked
        document_type: Union[Unset, str] = UNSET
        if not isinstance(self.document_type, Unset):
            document_type = self.document_type.value

        document_ref = self.document_ref
        document_expiry: Union[Unset, None, str] = UNSET
        if not isinstance(self.document_expiry, Unset):
            document_expiry = (
                self.document_expiry.isoformat() if self.document_expiry else None
            )

        note = self.note

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if checked is not UNSET:
            field_dict["checked"] = checked
        if document_type is not UNSET:
            field_dict["documentType"] = document_type
        if document_ref is not UNSET:
            field_dict["documentRef"] = document_ref
        if document_expiry is not UNSET:
            field_dict["documentExpiry"] = document_expiry
        if note is not UNSET:
            field_dict["note"] = note

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        checked = d.pop("checked", UNSET)

        _document_type = d.pop("documentType", UNSET)
        document_type: Union[Unset, RightToWorkDocumentType]
        if isinstance(_document_type, Unset):
            document_type = UNSET
        else:
            document_type = RightToWorkDocumentType(_document_type)

        document_ref = d.pop("documentRef", UNSET)

        _document_expiry = d.pop("documentExpiry", UNSET)
        document_expiry: Union[Unset, None, datetime.date]
        if _document_expiry is None:
            document_expiry = None
        elif isinstance(_document_expiry, Unset):
            document_expiry = UNSET
        else:
            document_expiry = isoparse(_document_expiry).date()

        note = d.pop("note", UNSET)

        right_to_work = cls(
            checked=checked,
            document_type=document_type,
            document_ref=document_ref,
            document_expiry=document_expiry,
            note=note,
        )

        return right_to_work
