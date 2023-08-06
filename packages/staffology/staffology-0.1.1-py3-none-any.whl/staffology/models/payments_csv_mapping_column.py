from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="PaymentsCsvMappingColumn")


@attr.s(auto_attribs=True)
class PaymentsCsvMappingColumn:
    """
    Attributes:
        title (str):
        code (Union[Unset, None, str]):
        is_reference_only (Union[Unset, bool]): If set to true then no PayCode is mapped and this column is just for on-
            screen refernece only
        col_index (Union[Unset, int]):
        is_multiplier (Union[Unset, bool]):
        rate_col_index (Union[Unset, None, int]): If the mapping IsMultiplier, then this optionally specifies another
            column from which to get the value
        should_serialize_rate_col_index (Union[Unset, bool]):
    """

    title: str
    code: Union[Unset, None, str] = UNSET
    is_reference_only: Union[Unset, bool] = UNSET
    col_index: Union[Unset, int] = UNSET
    is_multiplier: Union[Unset, bool] = UNSET
    rate_col_index: Union[Unset, None, int] = UNSET
    should_serialize_rate_col_index: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        title = self.title
        code = self.code
        is_reference_only = self.is_reference_only
        col_index = self.col_index
        is_multiplier = self.is_multiplier
        rate_col_index = self.rate_col_index
        should_serialize_rate_col_index = self.should_serialize_rate_col_index

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "title": title,
            }
        )
        if code is not UNSET:
            field_dict["code"] = code
        if is_reference_only is not UNSET:
            field_dict["isReferenceOnly"] = is_reference_only
        if col_index is not UNSET:
            field_dict["colIndex"] = col_index
        if is_multiplier is not UNSET:
            field_dict["isMultiplier"] = is_multiplier
        if rate_col_index is not UNSET:
            field_dict["rateColIndex"] = rate_col_index
        if should_serialize_rate_col_index is not UNSET:
            field_dict["shouldSerializeRateColIndex"] = should_serialize_rate_col_index

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        title = d.pop("title")

        code = d.pop("code", UNSET)

        is_reference_only = d.pop("isReferenceOnly", UNSET)

        col_index = d.pop("colIndex", UNSET)

        is_multiplier = d.pop("isMultiplier", UNSET)

        rate_col_index = d.pop("rateColIndex", UNSET)

        should_serialize_rate_col_index = d.pop("shouldSerializeRateColIndex", UNSET)

        payments_csv_mapping_column = cls(
            title=title,
            code=code,
            is_reference_only=is_reference_only,
            col_index=col_index,
            is_multiplier=is_multiplier,
            rate_col_index=rate_col_index,
            should_serialize_rate_col_index=should_serialize_rate_col_index,
        )

        return payments_csv_mapping_column
