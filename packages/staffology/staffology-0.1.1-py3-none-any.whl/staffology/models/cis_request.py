from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.cis_contractor import CisContractor
from ..models.cis_sub_contractor import CisSubContractor
from ..types import UNSET, Unset

T = TypeVar("T", bound="CisRequest")


@attr.s(auto_attribs=True)
class CisRequest:
    """
    Attributes:
        contractor (Union[Unset, CisContractor]): Used to represent details of a CIS SubContractor when communicating
            with the HMRC Gateway
        subcontractor (Union[Unset, None, List[CisSubContractor]]):
        declaration (Union[Unset, None, str]):
    """

    contractor: Union[Unset, CisContractor] = UNSET
    subcontractor: Union[Unset, None, List[CisSubContractor]] = UNSET
    declaration: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        contractor: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.contractor, Unset):
            contractor = self.contractor.to_dict()

        subcontractor: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.subcontractor, Unset):
            if self.subcontractor is None:
                subcontractor = None
            else:
                subcontractor = []
                for subcontractor_item_data in self.subcontractor:
                    subcontractor_item = subcontractor_item_data.to_dict()

                    subcontractor.append(subcontractor_item)

        declaration = self.declaration

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if contractor is not UNSET:
            field_dict["contractor"] = contractor
        if subcontractor is not UNSET:
            field_dict["subcontractor"] = subcontractor
        if declaration is not UNSET:
            field_dict["declaration"] = declaration

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _contractor = d.pop("contractor", UNSET)
        contractor: Union[Unset, CisContractor]
        if isinstance(_contractor, Unset):
            contractor = UNSET
        else:
            contractor = CisContractor.from_dict(_contractor)

        subcontractor = []
        _subcontractor = d.pop("subcontractor", UNSET)
        for subcontractor_item_data in _subcontractor or []:
            subcontractor_item = CisSubContractor.from_dict(subcontractor_item_data)

            subcontractor.append(subcontractor_item)

        declaration = d.pop("declaration", UNSET)

        cis_request = cls(
            contractor=contractor,
            subcontractor=subcontractor,
            declaration=declaration,
        )

        return cis_request
