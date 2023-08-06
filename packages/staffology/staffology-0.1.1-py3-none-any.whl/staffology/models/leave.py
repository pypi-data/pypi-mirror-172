import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.external_data_provider_id import ExternalDataProviderId
from ..models.item import Item
from ..models.leave_pay_type import LeavePayType
from ..models.leave_type import LeaveType
from ..models.linked_piw import LinkedPiw
from ..types import UNSET, Unset

T = TypeVar("T", bound="Leave")


@attr.s(auto_attribs=True)
class Leave:
    """Used to represent Leave, including Holiday and Statutory leave (such as Maternity Leave)

    Attributes:
        provider_id (Union[Unset, ExternalDataProviderId]):
        external_id (Union[Unset, None, str]): If the Leave comes from an ExternalDataProvider, then this is its Id in
            the ExternalDataProvider
        type (Union[Unset, LeaveType]):
        pay (Union[Unset, LeavePayType]):
        from_ (Union[Unset, datetime.datetime]): The first day of Leave.
            If it's a half day PM then set the time portion to 12:00:00, otherwise leave it blank or set it to 00:00:00
        to (Union[Unset, datetime.datetime]): The last day of Leave.
            If it's a half day AM then set the time portion to 11:59:59, otherwise set it to 23:59:59
        notes (Union[Unset, None, str]): A free-form text field to record any comments
        average_weekly_earnings (Union[Unset, float]): The employees average weekly earnings. Only relevant for
            Statutory Pay
            It's advised that you don't try to calculate this yourself.
        automatic_awe_calculation (Union[Unset, bool]): If set to True then we'll automatically calculate the
            AverageWeeklyEarnings.
            Set it to false if you want to manually provide a figure that overrides our calculations
        baby_date (Union[Unset, None, datetime.date]): Only required for Parental Leave with Statutory Pay
            If Type is Maternity or Paternity then this is the date the baby is due.
            For Adoption this is the Matching Date.
        secondary_baby_date (Union[Unset, None, datetime.date]): Only used for Parental Leave with Statutory Pay
            If Type is Maternity, Paternity, SharedParental (Birth) then this is the the Baby Born Date.
            For Adoption or SharedParental (Adoption) this is the Expected Placement Date.
        tertiary_baby_date (Union[Unset, None, datetime.date]): Only used for Parental Leave with Statutory Pay
            If Type is Adoption this is the Placement Date.
        override_payment_description (Union[Unset, bool]): If Pay is StatutoryPay and you want to override our
            description that goes with the payment then set this to true
        overriden_payment_description (Union[Unset, None, str]): If OverridePaymentDescription is true and Pay is set to
            StatutoryPay then we'll use this as the description for the payment amount.
        working_days (Union[Unset, float]): [readonly] The number of working days covered by this leave.
            This is calculated based on the employees Working Pattern.
        working_days_override (Union[Unset, None, float]): If a value is provided here then this will be used in place
            of the calculated WorkingDays value
        total_days (Union[Unset, float]): [readonly] The number of days covered by this leave, regardless of whether or
            not they're working days.
            This is calculated based on the employees Working Pattern.
        total_days_override (Union[Unset, None, float]): If a value is provided here then this will be used in place of
            the calculated TotalDays value
        use_assumed_pensionable_pay (Union[Unset, bool]): If this Leave has Statutory Pay (and isn't for Sick) then if
            this is set to True
            we will use the value set in AssumedPensionablePay to work out the employer pension contributions
        assumed_pensionable_pay (Union[Unset, None, float]): if AssumedPensionablePay is True, then this is the value
            used to calculate the employer pension contributions
        offset_pay (Union[Unset, bool]): If this Leave has Statutory Pay  and this is set to True and the employe eis
            paid a fixed amoutn per period
            with Leave Adjustments set to automatic, then we'll reduce their pay for the period by the statutory amount
            so the employee still gets paid the full amount.
        ssp_pay_from_day_one (Union[Unset, bool]): If this is Sick Leave with Statutory Pay then setting this to true
            will force SSP to be paid from day one rather than the usual rule
            of the first Working Day after 3 Qualifying Days
        linked_piw (Union[Unset, LinkedPiw]): Linked Period of Incapacity for Work.
            If you record Sick Leave and select Statutory Pay then any other Sick Leave with Statutory Pay
            lasting 4 or more days in the previous 8 weeks will be linked to it
        kit_split_days (Union[Unset, None, List[datetime.datetime]]): If the LeaveType supports KIT/SPLIT days then use
            this property to store the list of dates
        document_count (Union[Unset, int]): [readonly] The number of attachments associated with this model
        documents (Union[Unset, None, List[Item]]): [readonly] The attachments associated with this model
        employee (Union[Unset, Item]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    provider_id: Union[Unset, ExternalDataProviderId] = UNSET
    external_id: Union[Unset, None, str] = UNSET
    type: Union[Unset, LeaveType] = UNSET
    pay: Union[Unset, LeavePayType] = UNSET
    from_: Union[Unset, datetime.datetime] = UNSET
    to: Union[Unset, datetime.datetime] = UNSET
    notes: Union[Unset, None, str] = UNSET
    average_weekly_earnings: Union[Unset, float] = UNSET
    automatic_awe_calculation: Union[Unset, bool] = UNSET
    baby_date: Union[Unset, None, datetime.date] = UNSET
    secondary_baby_date: Union[Unset, None, datetime.date] = UNSET
    tertiary_baby_date: Union[Unset, None, datetime.date] = UNSET
    override_payment_description: Union[Unset, bool] = UNSET
    overriden_payment_description: Union[Unset, None, str] = UNSET
    working_days: Union[Unset, float] = UNSET
    working_days_override: Union[Unset, None, float] = UNSET
    total_days: Union[Unset, float] = UNSET
    total_days_override: Union[Unset, None, float] = UNSET
    use_assumed_pensionable_pay: Union[Unset, bool] = UNSET
    assumed_pensionable_pay: Union[Unset, None, float] = UNSET
    offset_pay: Union[Unset, bool] = UNSET
    ssp_pay_from_day_one: Union[Unset, bool] = UNSET
    linked_piw: Union[Unset, LinkedPiw] = UNSET
    kit_split_days: Union[Unset, None, List[datetime.datetime]] = UNSET
    document_count: Union[Unset, int] = UNSET
    documents: Union[Unset, None, List[Item]] = UNSET
    employee: Union[Unset, Item] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        provider_id: Union[Unset, str] = UNSET
        if not isinstance(self.provider_id, Unset):
            provider_id = self.provider_id.value

        external_id = self.external_id
        type: Union[Unset, str] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        pay: Union[Unset, str] = UNSET
        if not isinstance(self.pay, Unset):
            pay = self.pay.value

        from_: Union[Unset, str] = UNSET
        if not isinstance(self.from_, Unset):
            from_ = self.from_.isoformat()

        to: Union[Unset, str] = UNSET
        if not isinstance(self.to, Unset):
            to = self.to.isoformat()

        notes = self.notes
        average_weekly_earnings = self.average_weekly_earnings
        automatic_awe_calculation = self.automatic_awe_calculation
        baby_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.baby_date, Unset):
            baby_date = self.baby_date.isoformat() if self.baby_date else None

        secondary_baby_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.secondary_baby_date, Unset):
            secondary_baby_date = (
                self.secondary_baby_date.isoformat()
                if self.secondary_baby_date
                else None
            )

        tertiary_baby_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.tertiary_baby_date, Unset):
            tertiary_baby_date = (
                self.tertiary_baby_date.isoformat() if self.tertiary_baby_date else None
            )

        override_payment_description = self.override_payment_description
        overriden_payment_description = self.overriden_payment_description
        working_days = self.working_days
        working_days_override = self.working_days_override
        total_days = self.total_days
        total_days_override = self.total_days_override
        use_assumed_pensionable_pay = self.use_assumed_pensionable_pay
        assumed_pensionable_pay = self.assumed_pensionable_pay
        offset_pay = self.offset_pay
        ssp_pay_from_day_one = self.ssp_pay_from_day_one
        linked_piw: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.linked_piw, Unset):
            linked_piw = self.linked_piw.to_dict()

        kit_split_days: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.kit_split_days, Unset):
            if self.kit_split_days is None:
                kit_split_days = None
            else:
                kit_split_days = []
                for kit_split_days_item_data in self.kit_split_days:
                    kit_split_days_item = kit_split_days_item_data.isoformat()

                    kit_split_days.append(kit_split_days_item)

        document_count = self.document_count
        documents: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.documents, Unset):
            if self.documents is None:
                documents = None
            else:
                documents = []
                for documents_item_data in self.documents:
                    documents_item = documents_item_data.to_dict()

                    documents.append(documents_item)

        employee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employee, Unset):
            employee = self.employee.to_dict()

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if provider_id is not UNSET:
            field_dict["providerId"] = provider_id
        if external_id is not UNSET:
            field_dict["externalId"] = external_id
        if type is not UNSET:
            field_dict["type"] = type
        if pay is not UNSET:
            field_dict["pay"] = pay
        if from_ is not UNSET:
            field_dict["from"] = from_
        if to is not UNSET:
            field_dict["to"] = to
        if notes is not UNSET:
            field_dict["notes"] = notes
        if average_weekly_earnings is not UNSET:
            field_dict["averageWeeklyEarnings"] = average_weekly_earnings
        if automatic_awe_calculation is not UNSET:
            field_dict["automaticAWECalculation"] = automatic_awe_calculation
        if baby_date is not UNSET:
            field_dict["babyDate"] = baby_date
        if secondary_baby_date is not UNSET:
            field_dict["secondaryBabyDate"] = secondary_baby_date
        if tertiary_baby_date is not UNSET:
            field_dict["tertiaryBabyDate"] = tertiary_baby_date
        if override_payment_description is not UNSET:
            field_dict["overridePaymentDescription"] = override_payment_description
        if overriden_payment_description is not UNSET:
            field_dict["overridenPaymentDescription"] = overriden_payment_description
        if working_days is not UNSET:
            field_dict["workingDays"] = working_days
        if working_days_override is not UNSET:
            field_dict["workingDaysOverride"] = working_days_override
        if total_days is not UNSET:
            field_dict["totalDays"] = total_days
        if total_days_override is not UNSET:
            field_dict["totalDaysOverride"] = total_days_override
        if use_assumed_pensionable_pay is not UNSET:
            field_dict["useAssumedPensionablePay"] = use_assumed_pensionable_pay
        if assumed_pensionable_pay is not UNSET:
            field_dict["assumedPensionablePay"] = assumed_pensionable_pay
        if offset_pay is not UNSET:
            field_dict["offsetPay"] = offset_pay
        if ssp_pay_from_day_one is not UNSET:
            field_dict["sspPayFromDayOne"] = ssp_pay_from_day_one
        if linked_piw is not UNSET:
            field_dict["linkedPiw"] = linked_piw
        if kit_split_days is not UNSET:
            field_dict["kitSplitDays"] = kit_split_days
        if document_count is not UNSET:
            field_dict["documentCount"] = document_count
        if documents is not UNSET:
            field_dict["documents"] = documents
        if employee is not UNSET:
            field_dict["employee"] = employee
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _provider_id = d.pop("providerId", UNSET)
        provider_id: Union[Unset, ExternalDataProviderId]
        if isinstance(_provider_id, Unset):
            provider_id = UNSET
        else:
            provider_id = ExternalDataProviderId(_provider_id)

        external_id = d.pop("externalId", UNSET)

        _type = d.pop("type", UNSET)
        type: Union[Unset, LeaveType]
        if isinstance(_type, Unset):
            type = UNSET
        else:
            type = LeaveType(_type)

        _pay = d.pop("pay", UNSET)
        pay: Union[Unset, LeavePayType]
        if isinstance(_pay, Unset):
            pay = UNSET
        else:
            pay = LeavePayType(_pay)

        _from_ = d.pop("from", UNSET)
        from_: Union[Unset, datetime.datetime]
        if isinstance(_from_, Unset):
            from_ = UNSET
        else:
            from_ = isoparse(_from_)

        _to = d.pop("to", UNSET)
        to: Union[Unset, datetime.datetime]
        if isinstance(_to, Unset):
            to = UNSET
        else:
            to = isoparse(_to)

        notes = d.pop("notes", UNSET)

        average_weekly_earnings = d.pop("averageWeeklyEarnings", UNSET)

        automatic_awe_calculation = d.pop("automaticAWECalculation", UNSET)

        _baby_date = d.pop("babyDate", UNSET)
        baby_date: Union[Unset, None, datetime.date]
        if _baby_date is None:
            baby_date = None
        elif isinstance(_baby_date, Unset):
            baby_date = UNSET
        else:
            baby_date = isoparse(_baby_date).date()

        _secondary_baby_date = d.pop("secondaryBabyDate", UNSET)
        secondary_baby_date: Union[Unset, None, datetime.date]
        if _secondary_baby_date is None:
            secondary_baby_date = None
        elif isinstance(_secondary_baby_date, Unset):
            secondary_baby_date = UNSET
        else:
            secondary_baby_date = isoparse(_secondary_baby_date).date()

        _tertiary_baby_date = d.pop("tertiaryBabyDate", UNSET)
        tertiary_baby_date: Union[Unset, None, datetime.date]
        if _tertiary_baby_date is None:
            tertiary_baby_date = None
        elif isinstance(_tertiary_baby_date, Unset):
            tertiary_baby_date = UNSET
        else:
            tertiary_baby_date = isoparse(_tertiary_baby_date).date()

        override_payment_description = d.pop("overridePaymentDescription", UNSET)

        overriden_payment_description = d.pop("overridenPaymentDescription", UNSET)

        working_days = d.pop("workingDays", UNSET)

        working_days_override = d.pop("workingDaysOverride", UNSET)

        total_days = d.pop("totalDays", UNSET)

        total_days_override = d.pop("totalDaysOverride", UNSET)

        use_assumed_pensionable_pay = d.pop("useAssumedPensionablePay", UNSET)

        assumed_pensionable_pay = d.pop("assumedPensionablePay", UNSET)

        offset_pay = d.pop("offsetPay", UNSET)

        ssp_pay_from_day_one = d.pop("sspPayFromDayOne", UNSET)

        _linked_piw = d.pop("linkedPiw", UNSET)
        linked_piw: Union[Unset, LinkedPiw]
        if isinstance(_linked_piw, Unset):
            linked_piw = UNSET
        else:
            linked_piw = LinkedPiw.from_dict(_linked_piw)

        kit_split_days = []
        _kit_split_days = d.pop("kitSplitDays", UNSET)
        for kit_split_days_item_data in _kit_split_days or []:
            kit_split_days_item = isoparse(kit_split_days_item_data)

            kit_split_days.append(kit_split_days_item)

        document_count = d.pop("documentCount", UNSET)

        documents = []
        _documents = d.pop("documents", UNSET)
        for documents_item_data in _documents or []:
            documents_item = Item.from_dict(documents_item_data)

            documents.append(documents_item)

        _employee = d.pop("employee", UNSET)
        employee: Union[Unset, Item]
        if isinstance(_employee, Unset):
            employee = UNSET
        else:
            employee = Item.from_dict(_employee)

        id = d.pop("id", UNSET)

        leave = cls(
            provider_id=provider_id,
            external_id=external_id,
            type=type,
            pay=pay,
            from_=from_,
            to=to,
            notes=notes,
            average_weekly_earnings=average_weekly_earnings,
            automatic_awe_calculation=automatic_awe_calculation,
            baby_date=baby_date,
            secondary_baby_date=secondary_baby_date,
            tertiary_baby_date=tertiary_baby_date,
            override_payment_description=override_payment_description,
            overriden_payment_description=overriden_payment_description,
            working_days=working_days,
            working_days_override=working_days_override,
            total_days=total_days,
            total_days_override=total_days_override,
            use_assumed_pensionable_pay=use_assumed_pensionable_pay,
            assumed_pensionable_pay=assumed_pensionable_pay,
            offset_pay=offset_pay,
            ssp_pay_from_day_one=ssp_pay_from_day_one,
            linked_piw=linked_piw,
            kit_split_days=kit_split_days,
            document_count=document_count,
            documents=documents,
            employee=employee,
            id=id,
        )

        return leave
