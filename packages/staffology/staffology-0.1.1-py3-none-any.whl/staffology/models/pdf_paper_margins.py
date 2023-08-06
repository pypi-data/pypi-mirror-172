from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PdfPaperMargins")


@attr.s(auto_attribs=True)
class PdfPaperMargins:
    """
    Attributes:
        top (Union[Unset, float]):
        right (Union[Unset, float]):
        bottom (Union[Unset, float]):
        left (Union[Unset, float]):
    """

    top: Union[Unset, float] = UNSET
    right: Union[Unset, float] = UNSET
    bottom: Union[Unset, float] = UNSET
    left: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        top = self.top
        right = self.right
        bottom = self.bottom
        left = self.left

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if top is not UNSET:
            field_dict["top"] = top
        if right is not UNSET:
            field_dict["right"] = right
        if bottom is not UNSET:
            field_dict["bottom"] = bottom
        if left is not UNSET:
            field_dict["left"] = left

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        top = d.pop("top", UNSET)

        right = d.pop("right", UNSET)

        bottom = d.pop("bottom", UNSET)

        left = d.pop("left", UNSET)

        pdf_paper_margins = cls(
            top=top,
            right=right,
            bottom=bottom,
            left=left,
        )

        return pdf_paper_margins
