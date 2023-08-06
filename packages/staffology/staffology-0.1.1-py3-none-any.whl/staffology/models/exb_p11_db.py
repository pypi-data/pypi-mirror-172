from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.exb_p11_db_class_1a import ExbP11DbClass1A
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExbP11Db")


@attr.s(auto_attribs=True)
class ExbP11Db:
    """
    Attributes:
        class_1_acontributions_due (Union[Unset, ExbP11DbClass1A]):
    """

    class_1_acontributions_due: Union[Unset, ExbP11DbClass1A] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        class_1_acontributions_due: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.class_1_acontributions_due, Unset):
            class_1_acontributions_due = self.class_1_acontributions_due.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if class_1_acontributions_due is not UNSET:
            field_dict["class1AcontributionsDue"] = class_1_acontributions_due

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _class_1_acontributions_due = d.pop("class1AcontributionsDue", UNSET)
        class_1_acontributions_due: Union[Unset, ExbP11DbClass1A]
        if isinstance(_class_1_acontributions_due, Unset):
            class_1_acontributions_due = UNSET
        else:
            class_1_acontributions_due = ExbP11DbClass1A.from_dict(
                _class_1_acontributions_due
            )

        exb_p11_db = cls(
            class_1_acontributions_due=class_1_acontributions_due,
        )

        return exb_p11_db
