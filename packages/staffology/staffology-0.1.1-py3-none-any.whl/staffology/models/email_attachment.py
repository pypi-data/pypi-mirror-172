from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.pdf_password_type import PdfPasswordType
from ..types import UNSET, Unset

T = TypeVar("T", bound="EmailAttachment")


@attr.s(auto_attribs=True)
class EmailAttachment:
    """
    Attributes:
        url (str):
        filename (str):
        pdf_password_type (Union[Unset, PdfPasswordType]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    url: str
    filename: str
    pdf_password_type: Union[Unset, PdfPasswordType] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        url = self.url
        filename = self.filename
        pdf_password_type: Union[Unset, str] = UNSET
        if not isinstance(self.pdf_password_type, Unset):
            pdf_password_type = self.pdf_password_type.value

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "url": url,
                "filename": filename,
            }
        )
        if pdf_password_type is not UNSET:
            field_dict["pdfPasswordType"] = pdf_password_type
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        url = d.pop("url")

        filename = d.pop("filename")

        _pdf_password_type = d.pop("pdfPasswordType", UNSET)
        pdf_password_type: Union[Unset, PdfPasswordType]
        if isinstance(_pdf_password_type, Unset):
            pdf_password_type = UNSET
        else:
            pdf_password_type = PdfPasswordType(_pdf_password_type)

        id = d.pop("id", UNSET)

        email_attachment = cls(
            url=url,
            filename=filename,
            pdf_password_type=pdf_password_type,
            id=id,
        )

        return email_attachment
