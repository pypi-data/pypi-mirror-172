from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.papdis_employee_assessment import PapdisEmployeeAssessment
from ..models.papdis_employee_contact import PapdisEmployeeContact
from ..models.papdis_employee_contribution import PapdisEmployeeContribution
from ..models.papdis_employee_exit import PapdisEmployeeExit
from ..models.papdis_employee_identity import PapdisEmployeeIdentity
from ..models.papdis_employee_name import PapdisEmployeeName
from ..models.papdis_employee_pay import PapdisEmployeePay
from ..types import UNSET, Unset

T = TypeVar("T", bound="PapdisEmployee")


@attr.s(auto_attribs=True)
class PapdisEmployee:
    """
    Attributes:
        employee_id (Union[Unset, str]): [readonly]
        name (Union[Unset, PapdisEmployeeName]):
        identity (Union[Unset, PapdisEmployeeIdentity]):
        contact (Union[Unset, PapdisEmployeeContact]):
        pay (Union[Unset, PapdisEmployeePay]):
        assessment (Union[Unset, PapdisEmployeeAssessment]):
        contribution (Union[Unset, PapdisEmployeeContribution]):
        exit_ (Union[Unset, PapdisEmployeeExit]):
    """

    employee_id: Union[Unset, str] = UNSET
    name: Union[Unset, PapdisEmployeeName] = UNSET
    identity: Union[Unset, PapdisEmployeeIdentity] = UNSET
    contact: Union[Unset, PapdisEmployeeContact] = UNSET
    pay: Union[Unset, PapdisEmployeePay] = UNSET
    assessment: Union[Unset, PapdisEmployeeAssessment] = UNSET
    contribution: Union[Unset, PapdisEmployeeContribution] = UNSET
    exit_: Union[Unset, PapdisEmployeeExit] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        employee_id = self.employee_id
        name: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.name, Unset):
            name = self.name.to_dict()

        identity: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.identity, Unset):
            identity = self.identity.to_dict()

        contact: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.contact, Unset):
            contact = self.contact.to_dict()

        pay: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pay, Unset):
            pay = self.pay.to_dict()

        assessment: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.assessment, Unset):
            assessment = self.assessment.to_dict()

        contribution: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.contribution, Unset):
            contribution = self.contribution.to_dict()

        exit_: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.exit_, Unset):
            exit_ = self.exit_.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if employee_id is not UNSET:
            field_dict["employeeId"] = employee_id
        if name is not UNSET:
            field_dict["name"] = name
        if identity is not UNSET:
            field_dict["identity"] = identity
        if contact is not UNSET:
            field_dict["contact"] = contact
        if pay is not UNSET:
            field_dict["pay"] = pay
        if assessment is not UNSET:
            field_dict["assessment"] = assessment
        if contribution is not UNSET:
            field_dict["contribution"] = contribution
        if exit_ is not UNSET:
            field_dict["exit"] = exit_

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        employee_id = d.pop("employeeId", UNSET)

        _name = d.pop("name", UNSET)
        name: Union[Unset, PapdisEmployeeName]
        if isinstance(_name, Unset):
            name = UNSET
        else:
            name = PapdisEmployeeName.from_dict(_name)

        _identity = d.pop("identity", UNSET)
        identity: Union[Unset, PapdisEmployeeIdentity]
        if isinstance(_identity, Unset):
            identity = UNSET
        else:
            identity = PapdisEmployeeIdentity.from_dict(_identity)

        _contact = d.pop("contact", UNSET)
        contact: Union[Unset, PapdisEmployeeContact]
        if isinstance(_contact, Unset):
            contact = UNSET
        else:
            contact = PapdisEmployeeContact.from_dict(_contact)

        _pay = d.pop("pay", UNSET)
        pay: Union[Unset, PapdisEmployeePay]
        if isinstance(_pay, Unset):
            pay = UNSET
        else:
            pay = PapdisEmployeePay.from_dict(_pay)

        _assessment = d.pop("assessment", UNSET)
        assessment: Union[Unset, PapdisEmployeeAssessment]
        if isinstance(_assessment, Unset):
            assessment = UNSET
        else:
            assessment = PapdisEmployeeAssessment.from_dict(_assessment)

        _contribution = d.pop("contribution", UNSET)
        contribution: Union[Unset, PapdisEmployeeContribution]
        if isinstance(_contribution, Unset):
            contribution = UNSET
        else:
            contribution = PapdisEmployeeContribution.from_dict(_contribution)

        _exit_ = d.pop("exit", UNSET)
        exit_: Union[Unset, PapdisEmployeeExit]
        if isinstance(_exit_, Unset):
            exit_ = UNSET
        else:
            exit_ = PapdisEmployeeExit.from_dict(_exit_)

        papdis_employee = cls(
            employee_id=employee_id,
            name=name,
            identity=identity,
            contact=contact,
            pay=pay,
            assessment=assessment,
            contribution=contribution,
            exit_=exit_,
        )

        return papdis_employee
