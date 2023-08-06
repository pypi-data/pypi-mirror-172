from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="BureauSettings")


@attr.s(auto_attribs=True)
class BureauSettings:
    """Represents the BureauSettings for an Employer.

    Attributes:
        enable_approvals (Union[Unset, bool]): Whether or not Payruns for this employer need to go through an Approval
            process
        processor_user_id (Union[Unset, None, str]): The Id of the user, if any, that is the allocated Processor
        report_pack_id (Union[Unset, None, str]): The Id of the ReportPack, if any, to present to the Payroll Client
        is_bacs_client (Union[Unset, bool]): Indicates that the bureau is responsible for BACS payments of net wages to
            employees
        is_bacs_client_for_hmrc (Union[Unset, bool]): Indicates that the bureau is responsible for BACS payments of HMRC
            liabilites
        show_contact_card (Union[Unset, bool]): Show a Contact card with the Processors details  on the PayrollClient
            dashboard
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    enable_approvals: Union[Unset, bool] = UNSET
    processor_user_id: Union[Unset, None, str] = UNSET
    report_pack_id: Union[Unset, None, str] = UNSET
    is_bacs_client: Union[Unset, bool] = UNSET
    is_bacs_client_for_hmrc: Union[Unset, bool] = UNSET
    show_contact_card: Union[Unset, bool] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        enable_approvals = self.enable_approvals
        processor_user_id = self.processor_user_id
        report_pack_id = self.report_pack_id
        is_bacs_client = self.is_bacs_client
        is_bacs_client_for_hmrc = self.is_bacs_client_for_hmrc
        show_contact_card = self.show_contact_card
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if enable_approvals is not UNSET:
            field_dict["enableApprovals"] = enable_approvals
        if processor_user_id is not UNSET:
            field_dict["processorUserId"] = processor_user_id
        if report_pack_id is not UNSET:
            field_dict["reportPackId"] = report_pack_id
        if is_bacs_client is not UNSET:
            field_dict["isBacsClient"] = is_bacs_client
        if is_bacs_client_for_hmrc is not UNSET:
            field_dict["isBacsClientForHmrc"] = is_bacs_client_for_hmrc
        if show_contact_card is not UNSET:
            field_dict["showContactCard"] = show_contact_card
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        enable_approvals = d.pop("enableApprovals", UNSET)

        processor_user_id = d.pop("processorUserId", UNSET)

        report_pack_id = d.pop("reportPackId", UNSET)

        is_bacs_client = d.pop("isBacsClient", UNSET)

        is_bacs_client_for_hmrc = d.pop("isBacsClientForHmrc", UNSET)

        show_contact_card = d.pop("showContactCard", UNSET)

        id = d.pop("id", UNSET)

        bureau_settings = cls(
            enable_approvals=enable_approvals,
            processor_user_id=processor_user_id,
            report_pack_id=report_pack_id,
            is_bacs_client=is_bacs_client,
            is_bacs_client_for_hmrc=is_bacs_client_for_hmrc,
            show_contact_card=show_contact_card,
            id=id,
        )

        return bureau_settings
