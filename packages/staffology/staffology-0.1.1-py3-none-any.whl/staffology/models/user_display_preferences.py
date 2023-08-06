from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.cookie_preference import CookiePreference
from ..models.userstart_page import UserstartPage
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserDisplayPreferences")


@attr.s(auto_attribs=True)
class UserDisplayPreferences:
    """
    Attributes:
        start_page (Union[Unset, UserstartPage]):
        show_zeroes (Union[Unset, bool]):
        show_tax_code_when_viewing_payrun_entry (Union[Unset, bool]):
        allow_journal_resubmit (Union[Unset, bool]):
        hide_salary_on_employee_index_page (Union[Unset, bool]):
        enable_multi_employer_import (Union[Unset, bool]):
        enable_covid_19_features (Union[Unset, bool]):
        hide_payslip_checkboxes (Union[Unset, bool]):
        hide_payslip_search_and_sort (Union[Unset, bool]):
        show_ytd_in_payslip_view (Union[Unset, bool]):
        enable_dps_xml_upload (Union[Unset, bool]):
        enable_rti_timestamp_override (Union[Unset, bool]):
        enable_payrun_warnings (Union[Unset, bool]):
        enable_working_days_overrides (Union[Unset, bool]):
        cookie_preference (Union[Unset, CookiePreference]):
    """

    start_page: Union[Unset, UserstartPage] = UNSET
    show_zeroes: Union[Unset, bool] = UNSET
    show_tax_code_when_viewing_payrun_entry: Union[Unset, bool] = UNSET
    allow_journal_resubmit: Union[Unset, bool] = UNSET
    hide_salary_on_employee_index_page: Union[Unset, bool] = UNSET
    enable_multi_employer_import: Union[Unset, bool] = UNSET
    enable_covid_19_features: Union[Unset, bool] = UNSET
    hide_payslip_checkboxes: Union[Unset, bool] = UNSET
    hide_payslip_search_and_sort: Union[Unset, bool] = UNSET
    show_ytd_in_payslip_view: Union[Unset, bool] = UNSET
    enable_dps_xml_upload: Union[Unset, bool] = UNSET
    enable_rti_timestamp_override: Union[Unset, bool] = UNSET
    enable_payrun_warnings: Union[Unset, bool] = UNSET
    enable_working_days_overrides: Union[Unset, bool] = UNSET
    cookie_preference: Union[Unset, CookiePreference] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        start_page: Union[Unset, str] = UNSET
        if not isinstance(self.start_page, Unset):
            start_page = self.start_page.value

        show_zeroes = self.show_zeroes
        show_tax_code_when_viewing_payrun_entry = (
            self.show_tax_code_when_viewing_payrun_entry
        )
        allow_journal_resubmit = self.allow_journal_resubmit
        hide_salary_on_employee_index_page = self.hide_salary_on_employee_index_page
        enable_multi_employer_import = self.enable_multi_employer_import
        enable_covid_19_features = self.enable_covid_19_features
        hide_payslip_checkboxes = self.hide_payslip_checkboxes
        hide_payslip_search_and_sort = self.hide_payslip_search_and_sort
        show_ytd_in_payslip_view = self.show_ytd_in_payslip_view
        enable_dps_xml_upload = self.enable_dps_xml_upload
        enable_rti_timestamp_override = self.enable_rti_timestamp_override
        enable_payrun_warnings = self.enable_payrun_warnings
        enable_working_days_overrides = self.enable_working_days_overrides
        cookie_preference: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.cookie_preference, Unset):
            cookie_preference = self.cookie_preference.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if start_page is not UNSET:
            field_dict["startPage"] = start_page
        if show_zeroes is not UNSET:
            field_dict["showZeroes"] = show_zeroes
        if show_tax_code_when_viewing_payrun_entry is not UNSET:
            field_dict[
                "showTaxCodeWhenViewingPayrunEntry"
            ] = show_tax_code_when_viewing_payrun_entry
        if allow_journal_resubmit is not UNSET:
            field_dict["allowJournalResubmit"] = allow_journal_resubmit
        if hide_salary_on_employee_index_page is not UNSET:
            field_dict[
                "hideSalaryOnEmployeeIndexPage"
            ] = hide_salary_on_employee_index_page
        if enable_multi_employer_import is not UNSET:
            field_dict["enableMultiEmployerImport"] = enable_multi_employer_import
        if enable_covid_19_features is not UNSET:
            field_dict["enableCovid19Features"] = enable_covid_19_features
        if hide_payslip_checkboxes is not UNSET:
            field_dict["hidePayslipCheckboxes"] = hide_payslip_checkboxes
        if hide_payslip_search_and_sort is not UNSET:
            field_dict["hidePayslipSearchAndSort"] = hide_payslip_search_and_sort
        if show_ytd_in_payslip_view is not UNSET:
            field_dict["showYtdInPayslipView"] = show_ytd_in_payslip_view
        if enable_dps_xml_upload is not UNSET:
            field_dict["enableDpsXmlUpload"] = enable_dps_xml_upload
        if enable_rti_timestamp_override is not UNSET:
            field_dict["enableRtiTimestampOverride"] = enable_rti_timestamp_override
        if enable_payrun_warnings is not UNSET:
            field_dict["enablePayrunWarnings"] = enable_payrun_warnings
        if enable_working_days_overrides is not UNSET:
            field_dict["enableWorkingDaysOverrides"] = enable_working_days_overrides
        if cookie_preference is not UNSET:
            field_dict["cookiePreference"] = cookie_preference

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _start_page = d.pop("startPage", UNSET)
        start_page: Union[Unset, UserstartPage]
        if isinstance(_start_page, Unset):
            start_page = UNSET
        else:
            start_page = UserstartPage(_start_page)

        show_zeroes = d.pop("showZeroes", UNSET)

        show_tax_code_when_viewing_payrun_entry = d.pop(
            "showTaxCodeWhenViewingPayrunEntry", UNSET
        )

        allow_journal_resubmit = d.pop("allowJournalResubmit", UNSET)

        hide_salary_on_employee_index_page = d.pop(
            "hideSalaryOnEmployeeIndexPage", UNSET
        )

        enable_multi_employer_import = d.pop("enableMultiEmployerImport", UNSET)

        enable_covid_19_features = d.pop("enableCovid19Features", UNSET)

        hide_payslip_checkboxes = d.pop("hidePayslipCheckboxes", UNSET)

        hide_payslip_search_and_sort = d.pop("hidePayslipSearchAndSort", UNSET)

        show_ytd_in_payslip_view = d.pop("showYtdInPayslipView", UNSET)

        enable_dps_xml_upload = d.pop("enableDpsXmlUpload", UNSET)

        enable_rti_timestamp_override = d.pop("enableRtiTimestampOverride", UNSET)

        enable_payrun_warnings = d.pop("enablePayrunWarnings", UNSET)

        enable_working_days_overrides = d.pop("enableWorkingDaysOverrides", UNSET)

        _cookie_preference = d.pop("cookiePreference", UNSET)
        cookie_preference: Union[Unset, CookiePreference]
        if isinstance(_cookie_preference, Unset):
            cookie_preference = UNSET
        else:
            cookie_preference = CookiePreference.from_dict(_cookie_preference)

        user_display_preferences = cls(
            start_page=start_page,
            show_zeroes=show_zeroes,
            show_tax_code_when_viewing_payrun_entry=show_tax_code_when_viewing_payrun_entry,
            allow_journal_resubmit=allow_journal_resubmit,
            hide_salary_on_employee_index_page=hide_salary_on_employee_index_page,
            enable_multi_employer_import=enable_multi_employer_import,
            enable_covid_19_features=enable_covid_19_features,
            hide_payslip_checkboxes=hide_payslip_checkboxes,
            hide_payslip_search_and_sort=hide_payslip_search_and_sort,
            show_ytd_in_payslip_view=show_ytd_in_payslip_view,
            enable_dps_xml_upload=enable_dps_xml_upload,
            enable_rti_timestamp_override=enable_rti_timestamp_override,
            enable_payrun_warnings=enable_payrun_warnings,
            enable_working_days_overrides=enable_working_days_overrides,
            cookie_preference=cookie_preference,
        )

        return user_display_preferences
