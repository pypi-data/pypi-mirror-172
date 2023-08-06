import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.address import Address
from ..models.direct_debit_mandate import DirectDebitMandate
from ..models.monthly_minimum import MonthlyMinimum
from ..models.role import Role
from ..models.tenant import Tenant
from ..models.user_authorization import UserAuthorization
from ..models.user_category import UserCategory
from ..models.user_display_preferences import UserDisplayPreferences
from ..models.user_industry import UserIndustry
from ..models.user_job_type import UserJobType
from ..models.utm_info import UtmInfo
from ..types import UNSET, Unset

T = TypeVar("T", bound="User")


@attr.s(auto_attribs=True)
class User:
    """Represents a User Account.
    As well as basic details about the user it also includes details of Employers that the user account can access.

        Attributes:
            category (Union[Unset, UserCategory]):
            email_address (Union[Unset, None, str]):
            pending_email_address (Union[Unset, None, str]): If the user has requested to change their email address then
                the
                address it'll be changed to after verification will be shown here.
            first_name (Union[Unset, None, str]):
            last_name (Union[Unset, None, str]):
            salutation (Union[Unset, None, str]):
            user_identifier (Union[Unset, None, str]):
            photo (Union[Unset, None, str]):
            role (Union[Unset, Role]):
            job_type (Union[Unset, UserJobType]):
            job_title (Union[Unset, None, str]):
            telephone_number (Union[Unset, None, str]):
            business_name (Union[Unset, None, str]):
            industry (Union[Unset, UserIndustry]):
            address (Union[Unset, Address]):
            stated_employee_count (Union[Unset, None, int]):
            email_verified (Union[Unset, bool]):
            gdpr_optin (Union[Unset, bool]):
            invite_code (Union[Unset, None, str]):
            registration_ip (Union[Unset, None, str]):
            registration_date (Union[Unset, datetime.date]):
            last_login (Union[Unset, None, datetime.date]):
            is_activated (Union[Unset, bool]):
            authorization (Union[Unset, UserAuthorization]): This model provides information about what the User is able to
                access.
                This would usually just be a list of Employers. But if the user is an administrator for a White Label instance
                then this will be shown in the list of Tenants.
            is_super_admin (Union[Unset, bool]):
            can_use_bureau_features (Union[Unset, bool]):
            omnipresent_role (Union[Unset, Role]):
            tenant (Union[Unset, Tenant]): The Tenant model represents the brand that provides the account.
                This is used by our White Label partners to manage and brand their user accounts.
                Unless you are an admin for a White Label account you'll have no interest in this model.
            request_dd_setup (Union[Unset, bool]): [readonly] If true then the user is required to set up a direct debit
                mandate
            disabled (Union[Unset, bool]): [readonly] If true then any employers the owner managed will not be able to run
                new payruns.
                DisabledReason will give a reason why the account is disabled
            can_create_employers (Union[Unset, bool]): [readonly] If false then the user cannot create new employers.
                This can be turned on or off by the tenant admin.
            disabled_reason (Union[Unset, None, str]):
            direct_debit_mandate (Union[Unset, DirectDebitMandate]):
            display_prefs (Union[Unset, UserDisplayPreferences]):
            show_bills (Union[Unset, None, bool]): [readonly] Whether or not the user can see bills. This will be false if
                the Tenant manages billing and the user is not an admin for the Tenant
            accounting_customer_id (Union[Unset, None, str]): [readonly] Used internally to manage billing
            utm_info (Union[Unset, UtmInfo]):
            first_billable_activity_date (Union[Unset, None, datetime.date]):
            bureau_notification_email_address (Union[Unset, None, str]): If an email address is provided here then Bureau-
                related notifications will go to this address instead of the EmailAddress
            monthly_minimum (Union[Unset, MonthlyMinimum]):
            id (Union[Unset, str]): [readonly] The unique id of the object
    """

    category: Union[Unset, UserCategory] = UNSET
    email_address: Union[Unset, None, str] = UNSET
    pending_email_address: Union[Unset, None, str] = UNSET
    first_name: Union[Unset, None, str] = UNSET
    last_name: Union[Unset, None, str] = UNSET
    salutation: Union[Unset, None, str] = UNSET
    user_identifier: Union[Unset, None, str] = UNSET
    photo: Union[Unset, None, str] = UNSET
    role: Union[Unset, Role] = UNSET
    job_type: Union[Unset, UserJobType] = UNSET
    job_title: Union[Unset, None, str] = UNSET
    telephone_number: Union[Unset, None, str] = UNSET
    business_name: Union[Unset, None, str] = UNSET
    industry: Union[Unset, UserIndustry] = UNSET
    address: Union[Unset, Address] = UNSET
    stated_employee_count: Union[Unset, None, int] = UNSET
    email_verified: Union[Unset, bool] = UNSET
    gdpr_optin: Union[Unset, bool] = UNSET
    invite_code: Union[Unset, None, str] = UNSET
    registration_ip: Union[Unset, None, str] = UNSET
    registration_date: Union[Unset, datetime.date] = UNSET
    last_login: Union[Unset, None, datetime.date] = UNSET
    is_activated: Union[Unset, bool] = UNSET
    authorization: Union[Unset, UserAuthorization] = UNSET
    is_super_admin: Union[Unset, bool] = UNSET
    can_use_bureau_features: Union[Unset, bool] = UNSET
    omnipresent_role: Union[Unset, Role] = UNSET
    tenant: Union[Unset, Tenant] = UNSET
    request_dd_setup: Union[Unset, bool] = UNSET
    disabled: Union[Unset, bool] = UNSET
    can_create_employers: Union[Unset, bool] = UNSET
    disabled_reason: Union[Unset, None, str] = UNSET
    direct_debit_mandate: Union[Unset, DirectDebitMandate] = UNSET
    display_prefs: Union[Unset, UserDisplayPreferences] = UNSET
    show_bills: Union[Unset, None, bool] = UNSET
    accounting_customer_id: Union[Unset, None, str] = UNSET
    utm_info: Union[Unset, UtmInfo] = UNSET
    first_billable_activity_date: Union[Unset, None, datetime.date] = UNSET
    bureau_notification_email_address: Union[Unset, None, str] = UNSET
    monthly_minimum: Union[Unset, MonthlyMinimum] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        category: Union[Unset, str] = UNSET
        if not isinstance(self.category, Unset):
            category = self.category.value

        email_address = self.email_address
        pending_email_address = self.pending_email_address
        first_name = self.first_name
        last_name = self.last_name
        salutation = self.salutation
        user_identifier = self.user_identifier
        photo = self.photo
        role: Union[Unset, str] = UNSET
        if not isinstance(self.role, Unset):
            role = self.role.value

        job_type: Union[Unset, str] = UNSET
        if not isinstance(self.job_type, Unset):
            job_type = self.job_type.value

        job_title = self.job_title
        telephone_number = self.telephone_number
        business_name = self.business_name
        industry: Union[Unset, str] = UNSET
        if not isinstance(self.industry, Unset):
            industry = self.industry.value

        address: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.address, Unset):
            address = self.address.to_dict()

        stated_employee_count = self.stated_employee_count
        email_verified = self.email_verified
        gdpr_optin = self.gdpr_optin
        invite_code = self.invite_code
        registration_ip = self.registration_ip
        registration_date: Union[Unset, str] = UNSET
        if not isinstance(self.registration_date, Unset):
            registration_date = self.registration_date.isoformat()

        last_login: Union[Unset, None, str] = UNSET
        if not isinstance(self.last_login, Unset):
            last_login = self.last_login.isoformat() if self.last_login else None

        is_activated = self.is_activated
        authorization: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.authorization, Unset):
            authorization = self.authorization.to_dict()

        is_super_admin = self.is_super_admin
        can_use_bureau_features = self.can_use_bureau_features
        omnipresent_role: Union[Unset, str] = UNSET
        if not isinstance(self.omnipresent_role, Unset):
            omnipresent_role = self.omnipresent_role.value

        tenant: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.tenant, Unset):
            tenant = self.tenant.to_dict()

        request_dd_setup = self.request_dd_setup
        disabled = self.disabled
        can_create_employers = self.can_create_employers
        disabled_reason = self.disabled_reason
        direct_debit_mandate: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.direct_debit_mandate, Unset):
            direct_debit_mandate = self.direct_debit_mandate.to_dict()

        display_prefs: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.display_prefs, Unset):
            display_prefs = self.display_prefs.to_dict()

        show_bills = self.show_bills
        accounting_customer_id = self.accounting_customer_id
        utm_info: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.utm_info, Unset):
            utm_info = self.utm_info.to_dict()

        first_billable_activity_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.first_billable_activity_date, Unset):
            first_billable_activity_date = (
                self.first_billable_activity_date.isoformat()
                if self.first_billable_activity_date
                else None
            )

        bureau_notification_email_address = self.bureau_notification_email_address
        monthly_minimum: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.monthly_minimum, Unset):
            monthly_minimum = self.monthly_minimum.to_dict()

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if category is not UNSET:
            field_dict["category"] = category
        if email_address is not UNSET:
            field_dict["emailAddress"] = email_address
        if pending_email_address is not UNSET:
            field_dict["pendingEmailAddress"] = pending_email_address
        if first_name is not UNSET:
            field_dict["firstName"] = first_name
        if last_name is not UNSET:
            field_dict["lastName"] = last_name
        if salutation is not UNSET:
            field_dict["salutation"] = salutation
        if user_identifier is not UNSET:
            field_dict["userIdentifier"] = user_identifier
        if photo is not UNSET:
            field_dict["photo"] = photo
        if role is not UNSET:
            field_dict["role"] = role
        if job_type is not UNSET:
            field_dict["jobType"] = job_type
        if job_title is not UNSET:
            field_dict["jobTitle"] = job_title
        if telephone_number is not UNSET:
            field_dict["telephoneNumber"] = telephone_number
        if business_name is not UNSET:
            field_dict["businessName"] = business_name
        if industry is not UNSET:
            field_dict["industry"] = industry
        if address is not UNSET:
            field_dict["address"] = address
        if stated_employee_count is not UNSET:
            field_dict["statedEmployeeCount"] = stated_employee_count
        if email_verified is not UNSET:
            field_dict["emailVerified"] = email_verified
        if gdpr_optin is not UNSET:
            field_dict["gdprOptin"] = gdpr_optin
        if invite_code is not UNSET:
            field_dict["inviteCode"] = invite_code
        if registration_ip is not UNSET:
            field_dict["registrationIp"] = registration_ip
        if registration_date is not UNSET:
            field_dict["registrationDate"] = registration_date
        if last_login is not UNSET:
            field_dict["lastLogin"] = last_login
        if is_activated is not UNSET:
            field_dict["isActivated"] = is_activated
        if authorization is not UNSET:
            field_dict["authorization"] = authorization
        if is_super_admin is not UNSET:
            field_dict["isSuperAdmin"] = is_super_admin
        if can_use_bureau_features is not UNSET:
            field_dict["canUseBureauFeatures"] = can_use_bureau_features
        if omnipresent_role is not UNSET:
            field_dict["omnipresentRole"] = omnipresent_role
        if tenant is not UNSET:
            field_dict["tenant"] = tenant
        if request_dd_setup is not UNSET:
            field_dict["requestDdSetup"] = request_dd_setup
        if disabled is not UNSET:
            field_dict["disabled"] = disabled
        if can_create_employers is not UNSET:
            field_dict["canCreateEmployers"] = can_create_employers
        if disabled_reason is not UNSET:
            field_dict["disabledReason"] = disabled_reason
        if direct_debit_mandate is not UNSET:
            field_dict["directDebitMandate"] = direct_debit_mandate
        if display_prefs is not UNSET:
            field_dict["displayPrefs"] = display_prefs
        if show_bills is not UNSET:
            field_dict["showBills"] = show_bills
        if accounting_customer_id is not UNSET:
            field_dict["accountingCustomerId"] = accounting_customer_id
        if utm_info is not UNSET:
            field_dict["utmInfo"] = utm_info
        if first_billable_activity_date is not UNSET:
            field_dict["firstBillableActivityDate"] = first_billable_activity_date
        if bureau_notification_email_address is not UNSET:
            field_dict[
                "bureauNotificationEmailAddress"
            ] = bureau_notification_email_address
        if monthly_minimum is not UNSET:
            field_dict["monthlyMinimum"] = monthly_minimum
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _category = d.pop("category", UNSET)
        category: Union[Unset, UserCategory]
        if isinstance(_category, Unset):
            category = UNSET
        else:
            category = UserCategory(_category)

        email_address = d.pop("emailAddress", UNSET)

        pending_email_address = d.pop("pendingEmailAddress", UNSET)

        first_name = d.pop("firstName", UNSET)

        last_name = d.pop("lastName", UNSET)

        salutation = d.pop("salutation", UNSET)

        user_identifier = d.pop("userIdentifier", UNSET)

        photo = d.pop("photo", UNSET)

        _role = d.pop("role", UNSET)
        role: Union[Unset, Role]
        if isinstance(_role, Unset):
            role = UNSET
        else:
            role = Role(_role)

        _job_type = d.pop("jobType", UNSET)
        job_type: Union[Unset, UserJobType]
        if isinstance(_job_type, Unset):
            job_type = UNSET
        else:
            job_type = UserJobType(_job_type)

        job_title = d.pop("jobTitle", UNSET)

        telephone_number = d.pop("telephoneNumber", UNSET)

        business_name = d.pop("businessName", UNSET)

        _industry = d.pop("industry", UNSET)
        industry: Union[Unset, UserIndustry]
        if isinstance(_industry, Unset):
            industry = UNSET
        else:
            industry = UserIndustry(_industry)

        _address = d.pop("address", UNSET)
        address: Union[Unset, Address]
        if isinstance(_address, Unset):
            address = UNSET
        else:
            address = Address.from_dict(_address)

        stated_employee_count = d.pop("statedEmployeeCount", UNSET)

        email_verified = d.pop("emailVerified", UNSET)

        gdpr_optin = d.pop("gdprOptin", UNSET)

        invite_code = d.pop("inviteCode", UNSET)

        registration_ip = d.pop("registrationIp", UNSET)

        _registration_date = d.pop("registrationDate", UNSET)
        registration_date: Union[Unset, datetime.date]
        if isinstance(_registration_date, Unset):
            registration_date = UNSET
        else:
            registration_date = isoparse(_registration_date).date()

        _last_login = d.pop("lastLogin", UNSET)
        last_login: Union[Unset, None, datetime.date]
        if _last_login is None:
            last_login = None
        elif isinstance(_last_login, Unset):
            last_login = UNSET
        else:
            last_login = isoparse(_last_login).date()

        is_activated = d.pop("isActivated", UNSET)

        _authorization = d.pop("authorization", UNSET)
        authorization: Union[Unset, UserAuthorization]
        if isinstance(_authorization, Unset):
            authorization = UNSET
        else:
            authorization = UserAuthorization.from_dict(_authorization)

        is_super_admin = d.pop("isSuperAdmin", UNSET)

        can_use_bureau_features = d.pop("canUseBureauFeatures", UNSET)

        _omnipresent_role = d.pop("omnipresentRole", UNSET)
        omnipresent_role: Union[Unset, Role]
        if isinstance(_omnipresent_role, Unset):
            omnipresent_role = UNSET
        else:
            omnipresent_role = Role(_omnipresent_role)

        _tenant = d.pop("tenant", UNSET)
        tenant: Union[Unset, Tenant]
        if isinstance(_tenant, Unset):
            tenant = UNSET
        else:
            tenant = Tenant.from_dict(_tenant)

        request_dd_setup = d.pop("requestDdSetup", UNSET)

        disabled = d.pop("disabled", UNSET)

        can_create_employers = d.pop("canCreateEmployers", UNSET)

        disabled_reason = d.pop("disabledReason", UNSET)

        _direct_debit_mandate = d.pop("directDebitMandate", UNSET)
        direct_debit_mandate: Union[Unset, DirectDebitMandate]
        if isinstance(_direct_debit_mandate, Unset):
            direct_debit_mandate = UNSET
        else:
            direct_debit_mandate = DirectDebitMandate.from_dict(_direct_debit_mandate)

        _display_prefs = d.pop("displayPrefs", UNSET)
        display_prefs: Union[Unset, UserDisplayPreferences]
        if isinstance(_display_prefs, Unset):
            display_prefs = UNSET
        else:
            display_prefs = UserDisplayPreferences.from_dict(_display_prefs)

        show_bills = d.pop("showBills", UNSET)

        accounting_customer_id = d.pop("accountingCustomerId", UNSET)

        _utm_info = d.pop("utmInfo", UNSET)
        utm_info: Union[Unset, UtmInfo]
        if isinstance(_utm_info, Unset):
            utm_info = UNSET
        else:
            utm_info = UtmInfo.from_dict(_utm_info)

        _first_billable_activity_date = d.pop("firstBillableActivityDate", UNSET)
        first_billable_activity_date: Union[Unset, None, datetime.date]
        if _first_billable_activity_date is None:
            first_billable_activity_date = None
        elif isinstance(_first_billable_activity_date, Unset):
            first_billable_activity_date = UNSET
        else:
            first_billable_activity_date = isoparse(
                _first_billable_activity_date
            ).date()

        bureau_notification_email_address = d.pop(
            "bureauNotificationEmailAddress", UNSET
        )

        _monthly_minimum = d.pop("monthlyMinimum", UNSET)
        monthly_minimum: Union[Unset, MonthlyMinimum]
        if isinstance(_monthly_minimum, Unset):
            monthly_minimum = UNSET
        else:
            monthly_minimum = MonthlyMinimum.from_dict(_monthly_minimum)

        id = d.pop("id", UNSET)

        user = cls(
            category=category,
            email_address=email_address,
            pending_email_address=pending_email_address,
            first_name=first_name,
            last_name=last_name,
            salutation=salutation,
            user_identifier=user_identifier,
            photo=photo,
            role=role,
            job_type=job_type,
            job_title=job_title,
            telephone_number=telephone_number,
            business_name=business_name,
            industry=industry,
            address=address,
            stated_employee_count=stated_employee_count,
            email_verified=email_verified,
            gdpr_optin=gdpr_optin,
            invite_code=invite_code,
            registration_ip=registration_ip,
            registration_date=registration_date,
            last_login=last_login,
            is_activated=is_activated,
            authorization=authorization,
            is_super_admin=is_super_admin,
            can_use_bureau_features=can_use_bureau_features,
            omnipresent_role=omnipresent_role,
            tenant=tenant,
            request_dd_setup=request_dd_setup,
            disabled=disabled,
            can_create_employers=can_create_employers,
            disabled_reason=disabled_reason,
            direct_debit_mandate=direct_debit_mandate,
            display_prefs=display_prefs,
            show_bills=show_bills,
            accounting_customer_id=accounting_customer_id,
            utm_info=utm_info,
            first_billable_activity_date=first_billable_activity_date,
            bureau_notification_email_address=bureau_notification_email_address,
            monthly_minimum=monthly_minimum,
            id=id,
        )

        return user
