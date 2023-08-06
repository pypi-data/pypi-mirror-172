from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.cis_partnership import CisPartnership
from ..models.item import Item
from ..models.rti_employee_address import RtiEmployeeAddress
from ..models.rti_employee_name import RtiEmployeeName
from ..types import UNSET, Unset

T = TypeVar("T", bound="CisSubContractor")


@attr.s(auto_attribs=True)
class CisSubContractor:
    """
    Attributes:
        employee_unique_id (Union[Unset, str]):
        email_statement_to (Union[Unset, None, str]):
        number_of_payments (Union[Unset, int]):
        item (Union[Unset, Item]):
        display_name (Union[Unset, None, str]):
        action (Union[Unset, None, str]):
        type (Union[Unset, None, str]):
        name (Union[Unset, RtiEmployeeName]):
        trading_name (Union[Unset, None, str]):
        works_ref (Union[Unset, None, str]):
        unmatched_rate (Union[Unset, None, str]):
        utr (Union[Unset, None, str]):
        crn (Union[Unset, None, str]):
        nino (Union[Unset, None, str]):
        partnership (Union[Unset, CisPartnership]): If an Employee is marked as a CIS Subcontractor and is registered as
            a Partnership then this model provides further details specifically related to the CIS Partnership.
        address (Union[Unset, RtiEmployeeAddress]):
        telephone (Union[Unset, None, str]):
        total_payments_unrounded (Union[Unset, None, str]):
        cost_of_materials_unrounded (Union[Unset, None, str]):
        umbrella_fee (Union[Unset, None, str]):
        validation_msg (Union[Unset, None, str]):
        verification_number (Union[Unset, None, str]):
        total_payments (Union[Unset, None, str]):
        cost_of_materials (Union[Unset, None, str]):
        total_deducted (Union[Unset, None, str]):
        matched (Union[Unset, None, str]):
        tax_treatment (Union[Unset, None, str]):
    """

    employee_unique_id: Union[Unset, str] = UNSET
    email_statement_to: Union[Unset, None, str] = UNSET
    number_of_payments: Union[Unset, int] = UNSET
    item: Union[Unset, Item] = UNSET
    display_name: Union[Unset, None, str] = UNSET
    action: Union[Unset, None, str] = UNSET
    type: Union[Unset, None, str] = UNSET
    name: Union[Unset, RtiEmployeeName] = UNSET
    trading_name: Union[Unset, None, str] = UNSET
    works_ref: Union[Unset, None, str] = UNSET
    unmatched_rate: Union[Unset, None, str] = UNSET
    utr: Union[Unset, None, str] = UNSET
    crn: Union[Unset, None, str] = UNSET
    nino: Union[Unset, None, str] = UNSET
    partnership: Union[Unset, CisPartnership] = UNSET
    address: Union[Unset, RtiEmployeeAddress] = UNSET
    telephone: Union[Unset, None, str] = UNSET
    total_payments_unrounded: Union[Unset, None, str] = UNSET
    cost_of_materials_unrounded: Union[Unset, None, str] = UNSET
    umbrella_fee: Union[Unset, None, str] = UNSET
    validation_msg: Union[Unset, None, str] = UNSET
    verification_number: Union[Unset, None, str] = UNSET
    total_payments: Union[Unset, None, str] = UNSET
    cost_of_materials: Union[Unset, None, str] = UNSET
    total_deducted: Union[Unset, None, str] = UNSET
    matched: Union[Unset, None, str] = UNSET
    tax_treatment: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        employee_unique_id = self.employee_unique_id
        email_statement_to = self.email_statement_to
        number_of_payments = self.number_of_payments
        item: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.item, Unset):
            item = self.item.to_dict()

        display_name = self.display_name
        action = self.action
        type = self.type
        name: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.name, Unset):
            name = self.name.to_dict()

        trading_name = self.trading_name
        works_ref = self.works_ref
        unmatched_rate = self.unmatched_rate
        utr = self.utr
        crn = self.crn
        nino = self.nino
        partnership: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.partnership, Unset):
            partnership = self.partnership.to_dict()

        address: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.address, Unset):
            address = self.address.to_dict()

        telephone = self.telephone
        total_payments_unrounded = self.total_payments_unrounded
        cost_of_materials_unrounded = self.cost_of_materials_unrounded
        umbrella_fee = self.umbrella_fee
        validation_msg = self.validation_msg
        verification_number = self.verification_number
        total_payments = self.total_payments
        cost_of_materials = self.cost_of_materials
        total_deducted = self.total_deducted
        matched = self.matched
        tax_treatment = self.tax_treatment

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if employee_unique_id is not UNSET:
            field_dict["employeeUniqueId"] = employee_unique_id
        if email_statement_to is not UNSET:
            field_dict["emailStatementTo"] = email_statement_to
        if number_of_payments is not UNSET:
            field_dict["numberOfPayments"] = number_of_payments
        if item is not UNSET:
            field_dict["item"] = item
        if display_name is not UNSET:
            field_dict["displayName"] = display_name
        if action is not UNSET:
            field_dict["action"] = action
        if type is not UNSET:
            field_dict["type"] = type
        if name is not UNSET:
            field_dict["name"] = name
        if trading_name is not UNSET:
            field_dict["tradingName"] = trading_name
        if works_ref is not UNSET:
            field_dict["worksRef"] = works_ref
        if unmatched_rate is not UNSET:
            field_dict["unmatchedRate"] = unmatched_rate
        if utr is not UNSET:
            field_dict["utr"] = utr
        if crn is not UNSET:
            field_dict["crn"] = crn
        if nino is not UNSET:
            field_dict["nino"] = nino
        if partnership is not UNSET:
            field_dict["partnership"] = partnership
        if address is not UNSET:
            field_dict["address"] = address
        if telephone is not UNSET:
            field_dict["telephone"] = telephone
        if total_payments_unrounded is not UNSET:
            field_dict["totalPaymentsUnrounded"] = total_payments_unrounded
        if cost_of_materials_unrounded is not UNSET:
            field_dict["costOfMaterialsUnrounded"] = cost_of_materials_unrounded
        if umbrella_fee is not UNSET:
            field_dict["umbrellaFee"] = umbrella_fee
        if validation_msg is not UNSET:
            field_dict["validationMsg"] = validation_msg
        if verification_number is not UNSET:
            field_dict["verificationNumber"] = verification_number
        if total_payments is not UNSET:
            field_dict["totalPayments"] = total_payments
        if cost_of_materials is not UNSET:
            field_dict["costOfMaterials"] = cost_of_materials
        if total_deducted is not UNSET:
            field_dict["totalDeducted"] = total_deducted
        if matched is not UNSET:
            field_dict["matched"] = matched
        if tax_treatment is not UNSET:
            field_dict["taxTreatment"] = tax_treatment

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        employee_unique_id = d.pop("employeeUniqueId", UNSET)

        email_statement_to = d.pop("emailStatementTo", UNSET)

        number_of_payments = d.pop("numberOfPayments", UNSET)

        _item = d.pop("item", UNSET)
        item: Union[Unset, Item]
        if isinstance(_item, Unset):
            item = UNSET
        else:
            item = Item.from_dict(_item)

        display_name = d.pop("displayName", UNSET)

        action = d.pop("action", UNSET)

        type = d.pop("type", UNSET)

        _name = d.pop("name", UNSET)
        name: Union[Unset, RtiEmployeeName]
        if isinstance(_name, Unset):
            name = UNSET
        else:
            name = RtiEmployeeName.from_dict(_name)

        trading_name = d.pop("tradingName", UNSET)

        works_ref = d.pop("worksRef", UNSET)

        unmatched_rate = d.pop("unmatchedRate", UNSET)

        utr = d.pop("utr", UNSET)

        crn = d.pop("crn", UNSET)

        nino = d.pop("nino", UNSET)

        _partnership = d.pop("partnership", UNSET)
        partnership: Union[Unset, CisPartnership]
        if isinstance(_partnership, Unset):
            partnership = UNSET
        else:
            partnership = CisPartnership.from_dict(_partnership)

        _address = d.pop("address", UNSET)
        address: Union[Unset, RtiEmployeeAddress]
        if isinstance(_address, Unset):
            address = UNSET
        else:
            address = RtiEmployeeAddress.from_dict(_address)

        telephone = d.pop("telephone", UNSET)

        total_payments_unrounded = d.pop("totalPaymentsUnrounded", UNSET)

        cost_of_materials_unrounded = d.pop("costOfMaterialsUnrounded", UNSET)

        umbrella_fee = d.pop("umbrellaFee", UNSET)

        validation_msg = d.pop("validationMsg", UNSET)

        verification_number = d.pop("verificationNumber", UNSET)

        total_payments = d.pop("totalPayments", UNSET)

        cost_of_materials = d.pop("costOfMaterials", UNSET)

        total_deducted = d.pop("totalDeducted", UNSET)

        matched = d.pop("matched", UNSET)

        tax_treatment = d.pop("taxTreatment", UNSET)

        cis_sub_contractor = cls(
            employee_unique_id=employee_unique_id,
            email_statement_to=email_statement_to,
            number_of_payments=number_of_payments,
            item=item,
            display_name=display_name,
            action=action,
            type=type,
            name=name,
            trading_name=trading_name,
            works_ref=works_ref,
            unmatched_rate=unmatched_rate,
            utr=utr,
            crn=crn,
            nino=nino,
            partnership=partnership,
            address=address,
            telephone=telephone,
            total_payments_unrounded=total_payments_unrounded,
            cost_of_materials_unrounded=cost_of_materials_unrounded,
            umbrella_fee=umbrella_fee,
            validation_msg=validation_msg,
            verification_number=verification_number,
            total_payments=total_payments,
            cost_of_materials=cost_of_materials,
            total_deducted=total_deducted,
            matched=matched,
            tax_treatment=tax_treatment,
        )

        return cis_sub_contractor
