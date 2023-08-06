from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.mail_settings import MailSettings
from ..models.tenant_billing_settings import TenantBillingSettings
from ..models.tenant_html_insertion import TenantHtmlInsertion
from ..types import UNSET, Unset

T = TypeVar("T", bound="Tenant")


@attr.s(auto_attribs=True)
class Tenant:
    """The Tenant model represents the brand that provides the account.
    This is used by our White Label partners to manage and brand their user accounts.
    Unless you are an admin for a White Label account you'll have no interest in this model.

        Attributes:
            brand_code (Union[Unset, None, str]): [readonly]
            app_name (Union[Unset, None, str]):
            home_url (Union[Unset, None, str]):
            head_content (Union[Unset, None, str]):
            log_out_url (Union[Unset, None, str]):
            login_img_url (Union[Unset, None, str]): [readonly]
            home_img_url (Union[Unset, None, str]): [readonly]
            fav_icon (Union[Unset, None, str]): [readonly]
            css_colors_file (Union[Unset, None, str]): [readonly]
            css_file (Union[Unset, None, str]): [readonly]
            mailing_list (Union[Unset, bool]):
            html_insertions (Union[Unset, None, List[TenantHtmlInsertion]]):
            mail_settings (Union[Unset, MailSettings]): Determines the settings used when the Employer sends emails.
                If CustomiseSmtpSettings is false then SmtpSettings will be null and our default internal settings will be used;
            signup_url (Union[Unset, None, str]):
            terms_url (Union[Unset, None, str]):
            help_url (Union[Unset, None, str]):
            support_email (Union[Unset, None, str]):
            new_user_signup_email (Union[Unset, None, str]):
            approve_new_users (Union[Unset, bool]):
            enable_bureau_features (Union[Unset, bool]):
            require_dd_mandate_before_allowing_billable_activity (Union[Unset, bool]):
            enable_omnipresent_users (Union[Unset, bool]):
            tenant_owns_billing (Union[Unset, bool]): [readonly]
            billing_settings (Union[Unset, TenantBillingSettings]):
            id (Union[Unset, str]): [readonly] The unique id of the object
    """

    brand_code: Union[Unset, None, str] = UNSET
    app_name: Union[Unset, None, str] = UNSET
    home_url: Union[Unset, None, str] = UNSET
    head_content: Union[Unset, None, str] = UNSET
    log_out_url: Union[Unset, None, str] = UNSET
    login_img_url: Union[Unset, None, str] = UNSET
    home_img_url: Union[Unset, None, str] = UNSET
    fav_icon: Union[Unset, None, str] = UNSET
    css_colors_file: Union[Unset, None, str] = UNSET
    css_file: Union[Unset, None, str] = UNSET
    mailing_list: Union[Unset, bool] = UNSET
    html_insertions: Union[Unset, None, List[TenantHtmlInsertion]] = UNSET
    mail_settings: Union[Unset, MailSettings] = UNSET
    signup_url: Union[Unset, None, str] = UNSET
    terms_url: Union[Unset, None, str] = UNSET
    help_url: Union[Unset, None, str] = UNSET
    support_email: Union[Unset, None, str] = UNSET
    new_user_signup_email: Union[Unset, None, str] = UNSET
    approve_new_users: Union[Unset, bool] = UNSET
    enable_bureau_features: Union[Unset, bool] = UNSET
    require_dd_mandate_before_allowing_billable_activity: Union[Unset, bool] = UNSET
    enable_omnipresent_users: Union[Unset, bool] = UNSET
    tenant_owns_billing: Union[Unset, bool] = UNSET
    billing_settings: Union[Unset, TenantBillingSettings] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        brand_code = self.brand_code
        app_name = self.app_name
        home_url = self.home_url
        head_content = self.head_content
        log_out_url = self.log_out_url
        login_img_url = self.login_img_url
        home_img_url = self.home_img_url
        fav_icon = self.fav_icon
        css_colors_file = self.css_colors_file
        css_file = self.css_file
        mailing_list = self.mailing_list
        html_insertions: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.html_insertions, Unset):
            if self.html_insertions is None:
                html_insertions = None
            else:
                html_insertions = []
                for html_insertions_item_data in self.html_insertions:
                    html_insertions_item = html_insertions_item_data.to_dict()

                    html_insertions.append(html_insertions_item)

        mail_settings: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.mail_settings, Unset):
            mail_settings = self.mail_settings.to_dict()

        signup_url = self.signup_url
        terms_url = self.terms_url
        help_url = self.help_url
        support_email = self.support_email
        new_user_signup_email = self.new_user_signup_email
        approve_new_users = self.approve_new_users
        enable_bureau_features = self.enable_bureau_features
        require_dd_mandate_before_allowing_billable_activity = (
            self.require_dd_mandate_before_allowing_billable_activity
        )
        enable_omnipresent_users = self.enable_omnipresent_users
        tenant_owns_billing = self.tenant_owns_billing
        billing_settings: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.billing_settings, Unset):
            billing_settings = self.billing_settings.to_dict()

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if brand_code is not UNSET:
            field_dict["brandCode"] = brand_code
        if app_name is not UNSET:
            field_dict["appName"] = app_name
        if home_url is not UNSET:
            field_dict["homeUrl"] = home_url
        if head_content is not UNSET:
            field_dict["headContent"] = head_content
        if log_out_url is not UNSET:
            field_dict["logOutUrl"] = log_out_url
        if login_img_url is not UNSET:
            field_dict["loginImgUrl"] = login_img_url
        if home_img_url is not UNSET:
            field_dict["homeImgUrl"] = home_img_url
        if fav_icon is not UNSET:
            field_dict["favIcon"] = fav_icon
        if css_colors_file is not UNSET:
            field_dict["cssColorsFile"] = css_colors_file
        if css_file is not UNSET:
            field_dict["cssFile"] = css_file
        if mailing_list is not UNSET:
            field_dict["mailingList"] = mailing_list
        if html_insertions is not UNSET:
            field_dict["htmlInsertions"] = html_insertions
        if mail_settings is not UNSET:
            field_dict["mailSettings"] = mail_settings
        if signup_url is not UNSET:
            field_dict["signupUrl"] = signup_url
        if terms_url is not UNSET:
            field_dict["termsUrl"] = terms_url
        if help_url is not UNSET:
            field_dict["helpUrl"] = help_url
        if support_email is not UNSET:
            field_dict["supportEmail"] = support_email
        if new_user_signup_email is not UNSET:
            field_dict["newUserSignupEmail"] = new_user_signup_email
        if approve_new_users is not UNSET:
            field_dict["approveNewUsers"] = approve_new_users
        if enable_bureau_features is not UNSET:
            field_dict["enableBureauFeatures"] = enable_bureau_features
        if require_dd_mandate_before_allowing_billable_activity is not UNSET:
            field_dict[
                "requireDdMandateBeforeAllowingBillableActivity"
            ] = require_dd_mandate_before_allowing_billable_activity
        if enable_omnipresent_users is not UNSET:
            field_dict["enableOmnipresentUsers"] = enable_omnipresent_users
        if tenant_owns_billing is not UNSET:
            field_dict["tenantOwnsBilling"] = tenant_owns_billing
        if billing_settings is not UNSET:
            field_dict["billingSettings"] = billing_settings
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        brand_code = d.pop("brandCode", UNSET)

        app_name = d.pop("appName", UNSET)

        home_url = d.pop("homeUrl", UNSET)

        head_content = d.pop("headContent", UNSET)

        log_out_url = d.pop("logOutUrl", UNSET)

        login_img_url = d.pop("loginImgUrl", UNSET)

        home_img_url = d.pop("homeImgUrl", UNSET)

        fav_icon = d.pop("favIcon", UNSET)

        css_colors_file = d.pop("cssColorsFile", UNSET)

        css_file = d.pop("cssFile", UNSET)

        mailing_list = d.pop("mailingList", UNSET)

        html_insertions = []
        _html_insertions = d.pop("htmlInsertions", UNSET)
        for html_insertions_item_data in _html_insertions or []:
            html_insertions_item = TenantHtmlInsertion.from_dict(
                html_insertions_item_data
            )

            html_insertions.append(html_insertions_item)

        _mail_settings = d.pop("mailSettings", UNSET)
        mail_settings: Union[Unset, MailSettings]
        if isinstance(_mail_settings, Unset):
            mail_settings = UNSET
        else:
            mail_settings = MailSettings.from_dict(_mail_settings)

        signup_url = d.pop("signupUrl", UNSET)

        terms_url = d.pop("termsUrl", UNSET)

        help_url = d.pop("helpUrl", UNSET)

        support_email = d.pop("supportEmail", UNSET)

        new_user_signup_email = d.pop("newUserSignupEmail", UNSET)

        approve_new_users = d.pop("approveNewUsers", UNSET)

        enable_bureau_features = d.pop("enableBureauFeatures", UNSET)

        require_dd_mandate_before_allowing_billable_activity = d.pop(
            "requireDdMandateBeforeAllowingBillableActivity", UNSET
        )

        enable_omnipresent_users = d.pop("enableOmnipresentUsers", UNSET)

        tenant_owns_billing = d.pop("tenantOwnsBilling", UNSET)

        _billing_settings = d.pop("billingSettings", UNSET)
        billing_settings: Union[Unset, TenantBillingSettings]
        if isinstance(_billing_settings, Unset):
            billing_settings = UNSET
        else:
            billing_settings = TenantBillingSettings.from_dict(_billing_settings)

        id = d.pop("id", UNSET)

        tenant = cls(
            brand_code=brand_code,
            app_name=app_name,
            home_url=home_url,
            head_content=head_content,
            log_out_url=log_out_url,
            login_img_url=login_img_url,
            home_img_url=home_img_url,
            fav_icon=fav_icon,
            css_colors_file=css_colors_file,
            css_file=css_file,
            mailing_list=mailing_list,
            html_insertions=html_insertions,
            mail_settings=mail_settings,
            signup_url=signup_url,
            terms_url=terms_url,
            help_url=help_url,
            support_email=support_email,
            new_user_signup_email=new_user_signup_email,
            approve_new_users=approve_new_users,
            enable_bureau_features=enable_bureau_features,
            require_dd_mandate_before_allowing_billable_activity=require_dd_mandate_before_allowing_billable_activity,
            enable_omnipresent_users=enable_omnipresent_users,
            tenant_owns_billing=tenant_owns_billing,
            billing_settings=billing_settings,
            id=id,
        )

        return tenant
