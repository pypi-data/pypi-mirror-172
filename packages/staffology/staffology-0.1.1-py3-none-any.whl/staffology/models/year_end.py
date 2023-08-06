from typing import Any, Dict, List, Type, TypeVar, Union

import attr

from ..models.external_data_provider_id import ExternalDataProviderId
from ..models.item import Item
from ..models.tax_year import TaxYear
from ..models.year_end_tax_code_change import YearEndTaxCodeChange
from ..types import UNSET, Unset

T = TypeVar("T", bound="YearEnd")


@attr.s(auto_attribs=True)
class YearEnd:
    """This model gives you a summary of what will happen when you confirm the closing of one year and the start of the
    next

        Attributes:
            ending_year (Union[Unset, TaxYear]):
            starting_year (Union[Unset, TaxYear]):
            create_eps_for_final_submission (Union[Unset, bool]): [readonly] Whether or not the system will automatically
                create an EPS to tell HMRC the year has ended.
            create_eps_for_employment_allowance (Union[Unset, bool]): [readonly] Whether or not the system will
                automatically create an EPS to tell HMRC you qualify for Employment Allowance.
            create_exb (Union[Unset, bool]): [readonly] Whether or not the system will automatically create an EXB to inform
                HMRC of Expenses and Benefits
            set_employment_allowance (Union[Unset, None, float]): [readonly] If the Employment Allowance needs to be
                changed, this indicates the new value
            tax_code_changes (Union[Unset, None, List[YearEndTaxCodeChange]]): [readonly] Details of changes that wil be
                made to Tax Codes
            remove_week_1_month_1 (Union[Unset, None, List[Item]]): [readonly] Employees that will have the Week1Month1 flag
                removed from their tax code
            email_p60 (Union[Unset, None, List[Item]]): [readonly] Employees who will be automatically emailed P60s
            push_p60 (Union[Unset, None, List[ExternalDataProviderId]]): [readonly] ExternalDataProviderIds to which P60s
                can be pushed
            email_cis_statement (Union[Unset, None, List[Item]]): [readonly] Subcontractors who will be automatically sent
                an annual CIS Statement
    """

    ending_year: Union[Unset, TaxYear] = UNSET
    starting_year: Union[Unset, TaxYear] = UNSET
    create_eps_for_final_submission: Union[Unset, bool] = UNSET
    create_eps_for_employment_allowance: Union[Unset, bool] = UNSET
    create_exb: Union[Unset, bool] = UNSET
    set_employment_allowance: Union[Unset, None, float] = UNSET
    tax_code_changes: Union[Unset, None, List[YearEndTaxCodeChange]] = UNSET
    remove_week_1_month_1: Union[Unset, None, List[Item]] = UNSET
    email_p60: Union[Unset, None, List[Item]] = UNSET
    push_p60: Union[Unset, None, List[ExternalDataProviderId]] = UNSET
    email_cis_statement: Union[Unset, None, List[Item]] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        ending_year: Union[Unset, str] = UNSET
        if not isinstance(self.ending_year, Unset):
            ending_year = self.ending_year.value

        starting_year: Union[Unset, str] = UNSET
        if not isinstance(self.starting_year, Unset):
            starting_year = self.starting_year.value

        create_eps_for_final_submission = self.create_eps_for_final_submission
        create_eps_for_employment_allowance = self.create_eps_for_employment_allowance
        create_exb = self.create_exb
        set_employment_allowance = self.set_employment_allowance
        tax_code_changes: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.tax_code_changes, Unset):
            if self.tax_code_changes is None:
                tax_code_changes = None
            else:
                tax_code_changes = []
                for tax_code_changes_item_data in self.tax_code_changes:
                    tax_code_changes_item = tax_code_changes_item_data.to_dict()

                    tax_code_changes.append(tax_code_changes_item)

        remove_week_1_month_1: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.remove_week_1_month_1, Unset):
            if self.remove_week_1_month_1 is None:
                remove_week_1_month_1 = None
            else:
                remove_week_1_month_1 = []
                for remove_week_1_month_1_item_data in self.remove_week_1_month_1:
                    remove_week_1_month_1_item = (
                        remove_week_1_month_1_item_data.to_dict()
                    )

                    remove_week_1_month_1.append(remove_week_1_month_1_item)

        email_p60: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.email_p60, Unset):
            if self.email_p60 is None:
                email_p60 = None
            else:
                email_p60 = []
                for email_p60_item_data in self.email_p60:
                    email_p60_item = email_p60_item_data.to_dict()

                    email_p60.append(email_p60_item)

        push_p60: Union[Unset, None, List[str]] = UNSET
        if not isinstance(self.push_p60, Unset):
            if self.push_p60 is None:
                push_p60 = None
            else:
                push_p60 = []
                for push_p60_item_data in self.push_p60:
                    push_p60_item = push_p60_item_data.value

                    push_p60.append(push_p60_item)

        email_cis_statement: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.email_cis_statement, Unset):
            if self.email_cis_statement is None:
                email_cis_statement = None
            else:
                email_cis_statement = []
                for email_cis_statement_item_data in self.email_cis_statement:
                    email_cis_statement_item = email_cis_statement_item_data.to_dict()

                    email_cis_statement.append(email_cis_statement_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if ending_year is not UNSET:
            field_dict["endingYear"] = ending_year
        if starting_year is not UNSET:
            field_dict["startingYear"] = starting_year
        if create_eps_for_final_submission is not UNSET:
            field_dict["createEpsForFinalSubmission"] = create_eps_for_final_submission
        if create_eps_for_employment_allowance is not UNSET:
            field_dict[
                "createEpsForEmploymentAllowance"
            ] = create_eps_for_employment_allowance
        if create_exb is not UNSET:
            field_dict["createExb"] = create_exb
        if set_employment_allowance is not UNSET:
            field_dict["setEmploymentAllowance"] = set_employment_allowance
        if tax_code_changes is not UNSET:
            field_dict["taxCodeChanges"] = tax_code_changes
        if remove_week_1_month_1 is not UNSET:
            field_dict["removeWeek1Month1"] = remove_week_1_month_1
        if email_p60 is not UNSET:
            field_dict["emailP60"] = email_p60
        if push_p60 is not UNSET:
            field_dict["pushP60"] = push_p60
        if email_cis_statement is not UNSET:
            field_dict["emailCisStatement"] = email_cis_statement

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _ending_year = d.pop("endingYear", UNSET)
        ending_year: Union[Unset, TaxYear]
        if isinstance(_ending_year, Unset):
            ending_year = UNSET
        else:
            ending_year = TaxYear(_ending_year)

        _starting_year = d.pop("startingYear", UNSET)
        starting_year: Union[Unset, TaxYear]
        if isinstance(_starting_year, Unset):
            starting_year = UNSET
        else:
            starting_year = TaxYear(_starting_year)

        create_eps_for_final_submission = d.pop("createEpsForFinalSubmission", UNSET)

        create_eps_for_employment_allowance = d.pop(
            "createEpsForEmploymentAllowance", UNSET
        )

        create_exb = d.pop("createExb", UNSET)

        set_employment_allowance = d.pop("setEmploymentAllowance", UNSET)

        tax_code_changes = []
        _tax_code_changes = d.pop("taxCodeChanges", UNSET)
        for tax_code_changes_item_data in _tax_code_changes or []:
            tax_code_changes_item = YearEndTaxCodeChange.from_dict(
                tax_code_changes_item_data
            )

            tax_code_changes.append(tax_code_changes_item)

        remove_week_1_month_1 = []
        _remove_week_1_month_1 = d.pop("removeWeek1Month1", UNSET)
        for remove_week_1_month_1_item_data in _remove_week_1_month_1 or []:
            remove_week_1_month_1_item = Item.from_dict(remove_week_1_month_1_item_data)

            remove_week_1_month_1.append(remove_week_1_month_1_item)

        email_p60 = []
        _email_p60 = d.pop("emailP60", UNSET)
        for email_p60_item_data in _email_p60 or []:
            email_p60_item = Item.from_dict(email_p60_item_data)

            email_p60.append(email_p60_item)

        push_p60 = []
        _push_p60 = d.pop("pushP60", UNSET)
        for push_p60_item_data in _push_p60 or []:
            push_p60_item = ExternalDataProviderId(push_p60_item_data)

            push_p60.append(push_p60_item)

        email_cis_statement = []
        _email_cis_statement = d.pop("emailCisStatement", UNSET)
        for email_cis_statement_item_data in _email_cis_statement or []:
            email_cis_statement_item = Item.from_dict(email_cis_statement_item_data)

            email_cis_statement.append(email_cis_statement_item)

        year_end = cls(
            ending_year=ending_year,
            starting_year=starting_year,
            create_eps_for_final_submission=create_eps_for_final_submission,
            create_eps_for_employment_allowance=create_eps_for_employment_allowance,
            create_exb=create_exb,
            set_employment_allowance=set_employment_allowance,
            tax_code_changes=tax_code_changes,
            remove_week_1_month_1=remove_week_1_month_1,
            email_p60=email_p60,
            push_p60=push_p60,
            email_cis_statement=email_cis_statement,
        )

        return year_end
