from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.address import Address
from ..models.rti_contact import RtiContact
from ..types import UNSET, Unset

T = TypeVar("T", bound="RtiAgent")


@attr.s(auto_attribs=True)
class RtiAgent:
    """
    Attributes:
        agent_id (Union[Unset, None, str]):
        company (Union[Unset, None, str]):
        address (Union[Unset, Address]):
        contact (Union[Unset, RtiContact]):
    """

    agent_id: Union[Unset, None, str] = UNSET
    company: Union[Unset, None, str] = UNSET
    address: Union[Unset, Address] = UNSET
    contact: Union[Unset, RtiContact] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        agent_id = self.agent_id
        company = self.company
        address: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.address, Unset):
            address = self.address.to_dict()

        contact: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.contact, Unset):
            contact = self.contact.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if agent_id is not UNSET:
            field_dict["agentId"] = agent_id
        if company is not UNSET:
            field_dict["company"] = company
        if address is not UNSET:
            field_dict["address"] = address
        if contact is not UNSET:
            field_dict["contact"] = contact

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        agent_id = d.pop("agentId", UNSET)

        company = d.pop("company", UNSET)

        _address = d.pop("address", UNSET)
        address: Union[Unset, Address]
        if isinstance(_address, Unset):
            address = UNSET
        else:
            address = Address.from_dict(_address)

        _contact = d.pop("contact", UNSET)
        contact: Union[Unset, RtiContact]
        if isinstance(_contact, Unset):
            contact = UNSET
        else:
            contact = RtiContact.from_dict(_contact)

        rti_agent = cls(
            agent_id=agent_id,
            company=company,
            address=address,
            contact=contact,
        )

        return rti_agent
