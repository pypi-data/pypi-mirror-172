from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.exb_declarations import ExbDeclarations
from ..models.exb_employer import ExbEmployer
from ..models.exb_p11_db import ExbP11Db
from ..models.exb_p11d import ExbP11D
from ..types import UNSET, Unset

T = TypeVar("T", bound="ExpensesAndBenefits")


@attr.s(auto_attribs=True)
class ExpensesAndBenefits:
    """
    Attributes:
        employer (Union[Unset, ExbEmployer]):
        declarations (Union[Unset, ExbDeclarations]):
        p_11_db (Union[Unset, ExbP11Db]):
        p_11_drecord_count (Union[Unset, int]):
        p_46_car_record_count (Union[Unset, int]):
        p_11d (Union[Unset, None, List[ExbP11D]]):
        related_tax_year (Union[Unset, None, str]):
    """

    employer: Union[Unset, ExbEmployer] = UNSET
    declarations: Union[Unset, ExbDeclarations] = UNSET
    p_11_db: Union[Unset, ExbP11Db] = UNSET
    p_11_drecord_count: Union[Unset, int] = UNSET
    p_46_car_record_count: Union[Unset, int] = UNSET
    p_11d: Union[Unset, None, List[ExbP11D]] = UNSET
    related_tax_year: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        employer: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employer, Unset):
            employer = self.employer.to_dict()

        declarations: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.declarations, Unset):
            declarations = self.declarations.to_dict()

        p_11_db: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.p_11_db, Unset):
            p_11_db = self.p_11_db.to_dict()

        p_11_drecord_count = self.p_11_drecord_count
        p_46_car_record_count = self.p_46_car_record_count
        p_11d: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.p_11d, Unset):
            if self.p_11d is None:
                p_11d = None
            else:
                p_11d = []
                for p_11d_item_data in self.p_11d:
                    p_11d_item = p_11d_item_data.to_dict()

                    p_11d.append(p_11d_item)

        related_tax_year = self.related_tax_year

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if employer is not UNSET:
            field_dict["employer"] = employer
        if declarations is not UNSET:
            field_dict["declarations"] = declarations
        if p_11_db is not UNSET:
            field_dict["p11Db"] = p_11_db
        if p_11_drecord_count is not UNSET:
            field_dict["p11DrecordCount"] = p_11_drecord_count
        if p_46_car_record_count is not UNSET:
            field_dict["p46CarRecordCount"] = p_46_car_record_count
        if p_11d is not UNSET:
            field_dict["p11D"] = p_11d
        if related_tax_year is not UNSET:
            field_dict["relatedTaxYear"] = related_tax_year

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _employer = d.pop("employer", UNSET)
        employer: Union[Unset, ExbEmployer]
        if isinstance(_employer, Unset):
            employer = UNSET
        else:
            employer = ExbEmployer.from_dict(_employer)

        _declarations = d.pop("declarations", UNSET)
        declarations: Union[Unset, ExbDeclarations]
        if isinstance(_declarations, Unset):
            declarations = UNSET
        else:
            declarations = ExbDeclarations.from_dict(_declarations)

        _p_11_db = d.pop("p11Db", UNSET)
        p_11_db: Union[Unset, ExbP11Db]
        if isinstance(_p_11_db, Unset):
            p_11_db = UNSET
        else:
            p_11_db = ExbP11Db.from_dict(_p_11_db)

        p_11_drecord_count = d.pop("p11DrecordCount", UNSET)

        p_46_car_record_count = d.pop("p46CarRecordCount", UNSET)

        p_11d = []
        _p_11d = d.pop("p11D", UNSET)
        for p_11d_item_data in _p_11d or []:
            p_11d_item = ExbP11D.from_dict(p_11d_item_data)

            p_11d.append(p_11d_item)

        related_tax_year = d.pop("relatedTaxYear", UNSET)

        expenses_and_benefits = cls(
            employer=employer,
            declarations=declarations,
            p_11_db=p_11_db,
            p_11_drecord_count=p_11_drecord_count,
            p_46_car_record_count=p_46_car_record_count,
            p_11d=p_11d,
            related_tax_year=related_tax_year,
        )

        return expenses_and_benefits
