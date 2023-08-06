from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.pension_scheme import PensionScheme
from ..types import UNSET, Unset

T = TypeVar("T", bound="PensionSelection")


@attr.s(auto_attribs=True)
class PensionSelection:
    """
    Attributes:
        id (Union[Unset, str]): [readonly] The unique id of the object
        pension_scheme_id (Union[Unset, str]):
        pension_scheme (Union[Unset, PensionScheme]):
        worker_group_id (Union[Unset, str]):
    """

    id: Union[Unset, str] = UNSET
    pension_scheme_id: Union[Unset, str] = UNSET
    pension_scheme: Union[Unset, PensionScheme] = UNSET
    worker_group_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        pension_scheme_id = self.pension_scheme_id
        pension_scheme: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pension_scheme, Unset):
            pension_scheme = self.pension_scheme.to_dict()

        worker_group_id = self.worker_group_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if pension_scheme_id is not UNSET:
            field_dict["pensionSchemeId"] = pension_scheme_id
        if pension_scheme is not UNSET:
            field_dict["pensionScheme"] = pension_scheme
        if worker_group_id is not UNSET:
            field_dict["workerGroupId"] = worker_group_id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        pension_scheme_id = d.pop("pensionSchemeId", UNSET)

        _pension_scheme = d.pop("pensionScheme", UNSET)
        pension_scheme: Union[Unset, PensionScheme]
        if isinstance(_pension_scheme, Unset):
            pension_scheme = UNSET
        else:
            pension_scheme = PensionScheme.from_dict(_pension_scheme)

        worker_group_id = d.pop("workerGroupId", UNSET)

        pension_selection = cls(
            id=id,
            pension_scheme_id=pension_scheme_id,
            pension_scheme=pension_scheme,
            worker_group_id=worker_group_id,
        )

        return pension_selection
