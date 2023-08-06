from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.rti_agent import RtiAgent
from ..models.rti_contact import RtiContact
from ..models.rti_sender_type import RtiSenderType
from ..types import UNSET, Unset

T = TypeVar("T", bound="RtiSubmissionSettings")


@attr.s(auto_attribs=True)
class RtiSubmissionSettings:
    """
    Attributes:
        sender_type (Union[Unset, RtiSenderType]):
        sender_id (Union[Unset, None, str]): The SenderId used to submit RTI documents to HMRC
        password (Union[Unset, None, str]): The Password used to submit RTI documents to HMRC
        exclude_nil_paid (Union[Unset, bool]): Whether or not to include Employees paid a zero amount on your FPS
        include_hash_cross_ref (Union[Unset, bool]): [readonly] Whether or not the Bacs Cross Ref field is included on
            your FPS submissions
            This is automatically set to true if you use a bank payments CSV format that supports it
            or set to false if not
        auto_submit_fps (Union[Unset, bool]): If set to true, we'll automatically send your FPS to HMRC whenever you
            finalise a PayRun
        test_in_live (Union[Unset, bool]): Used for testing the RTI gateway. If set to true then the Document Type name
            will have "-TIL" appended to it
        use_test_gateway (Union[Unset, bool]): If set to true then your RTI documents will be sent to HMRCs test
            services instead of the live service
        override_timestamp_value (Union[Unset, None, str]): If a value is provided then it will be used as the timestamp
            on the RTI submission. This would normally only be used for testing purposes.
        contact (Union[Unset, RtiContact]):
        agent (Union[Unset, RtiAgent]):
    """

    sender_type: Union[Unset, RtiSenderType] = UNSET
    sender_id: Union[Unset, None, str] = UNSET
    password: Union[Unset, None, str] = UNSET
    exclude_nil_paid: Union[Unset, bool] = UNSET
    include_hash_cross_ref: Union[Unset, bool] = UNSET
    auto_submit_fps: Union[Unset, bool] = UNSET
    test_in_live: Union[Unset, bool] = UNSET
    use_test_gateway: Union[Unset, bool] = UNSET
    override_timestamp_value: Union[Unset, None, str] = UNSET
    contact: Union[Unset, RtiContact] = UNSET
    agent: Union[Unset, RtiAgent] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        sender_type: Union[Unset, str] = UNSET
        if not isinstance(self.sender_type, Unset):
            sender_type = self.sender_type.value

        sender_id = self.sender_id
        password = self.password
        exclude_nil_paid = self.exclude_nil_paid
        include_hash_cross_ref = self.include_hash_cross_ref
        auto_submit_fps = self.auto_submit_fps
        test_in_live = self.test_in_live
        use_test_gateway = self.use_test_gateway
        override_timestamp_value = self.override_timestamp_value
        contact: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.contact, Unset):
            contact = self.contact.to_dict()

        agent: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.agent, Unset):
            agent = self.agent.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if sender_type is not UNSET:
            field_dict["senderType"] = sender_type
        if sender_id is not UNSET:
            field_dict["senderId"] = sender_id
        if password is not UNSET:
            field_dict["password"] = password
        if exclude_nil_paid is not UNSET:
            field_dict["excludeNilPaid"] = exclude_nil_paid
        if include_hash_cross_ref is not UNSET:
            field_dict["includeHashCrossRef"] = include_hash_cross_ref
        if auto_submit_fps is not UNSET:
            field_dict["autoSubmitFps"] = auto_submit_fps
        if test_in_live is not UNSET:
            field_dict["testInLive"] = test_in_live
        if use_test_gateway is not UNSET:
            field_dict["useTestGateway"] = use_test_gateway
        if override_timestamp_value is not UNSET:
            field_dict["overrideTimestampValue"] = override_timestamp_value
        if contact is not UNSET:
            field_dict["contact"] = contact
        if agent is not UNSET:
            field_dict["agent"] = agent

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _sender_type = d.pop("senderType", UNSET)
        sender_type: Union[Unset, RtiSenderType]
        if isinstance(_sender_type, Unset):
            sender_type = UNSET
        else:
            sender_type = RtiSenderType(_sender_type)

        sender_id = d.pop("senderId", UNSET)

        password = d.pop("password", UNSET)

        exclude_nil_paid = d.pop("excludeNilPaid", UNSET)

        include_hash_cross_ref = d.pop("includeHashCrossRef", UNSET)

        auto_submit_fps = d.pop("autoSubmitFps", UNSET)

        test_in_live = d.pop("testInLive", UNSET)

        use_test_gateway = d.pop("useTestGateway", UNSET)

        override_timestamp_value = d.pop("overrideTimestampValue", UNSET)

        _contact = d.pop("contact", UNSET)
        contact: Union[Unset, RtiContact]
        if isinstance(_contact, Unset):
            contact = UNSET
        else:
            contact = RtiContact.from_dict(_contact)

        _agent = d.pop("agent", UNSET)
        agent: Union[Unset, RtiAgent]
        if isinstance(_agent, Unset):
            agent = UNSET
        else:
            agent = RtiAgent.from_dict(_agent)

        rti_submission_settings = cls(
            sender_type=sender_type,
            sender_id=sender_id,
            password=password,
            exclude_nil_paid=exclude_nil_paid,
            include_hash_cross_ref=include_hash_cross_ref,
            auto_submit_fps=auto_submit_fps,
            test_in_live=test_in_live,
            use_test_gateway=use_test_gateway,
            override_timestamp_value=override_timestamp_value,
            contact=contact,
            agent=agent,
        )

        return rti_submission_settings
