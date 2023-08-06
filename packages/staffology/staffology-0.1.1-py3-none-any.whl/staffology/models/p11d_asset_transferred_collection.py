from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.p11d_desc_other import P11DDescOther
from ..types import UNSET, Unset

T = TypeVar("T", bound="P11DAssetTransferredCollection")


@attr.s(auto_attribs=True)
class P11DAssetTransferredCollection:
    """
    Attributes:
        asset (Union[Unset, None, List[P11DDescOther]]):
        type_letter (Union[Unset, None, str]):
    """

    asset: Union[Unset, None, List[P11DDescOther]] = UNSET
    type_letter: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        asset: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.asset, Unset):
            if self.asset is None:
                asset = None
            else:
                asset = []
                for asset_item_data in self.asset:
                    asset_item = asset_item_data.to_dict()

                    asset.append(asset_item)

        type_letter = self.type_letter

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if asset is not UNSET:
            field_dict["asset"] = asset
        if type_letter is not UNSET:
            field_dict["typeLetter"] = type_letter

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        asset = []
        _asset = d.pop("asset", UNSET)
        for asset_item_data in _asset or []:
            asset_item = P11DDescOther.from_dict(asset_item_data)

            asset.append(asset_item)

        type_letter = d.pop("typeLetter", UNSET)

        p11d_asset_transferred_collection = cls(
            asset=asset,
            type_letter=type_letter,
        )

        return p11d_asset_transferred_collection
