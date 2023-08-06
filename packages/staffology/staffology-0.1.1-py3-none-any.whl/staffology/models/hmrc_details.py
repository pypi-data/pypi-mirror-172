from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="HmrcDetails")


@attr.s(auto_attribs=True)
class HmrcDetails:
    """
    Attributes:
        office_number (Union[Unset, None, str]):
        paye_reference (Union[Unset, None, str]):
        accounts_office_reference (Union[Unset, None, str]):
        econ (Union[Unset, None, str]):
        utr (Union[Unset, None, str]):
        co_tax (Union[Unset, None, str]):
        employment_allowance (Union[Unset, bool]):
        employment_allowance_max_claim (Union[Unset, float]): You might reduce this from the default if you've made/are
            making a claim in another system
        small_employers_relief (Union[Unset, bool]):
        apprenticeship_levy (Union[Unset, bool]):
        apprenticeship_levy_allowance (Union[Unset, float]):
        quarterly_payment_schedule (Union[Unset, bool]): Set to true if the employer pays HMRC on a quarterly schedule.
            A value of false implies a monthly schedule.
            <b>Warning:</b> Changing this value after starting PayRuns will
            delete any existing payments or adjustments you may have entered.
        include_employment_allowance_on_monthly_journal (Union[Unset, bool]): If the employer is not on a
            QuarterlyPaymentSchedule
            and is claiming EmploymentAllowance, then set this to true to include a line for
            Employment Allowance on the journal for the monthly schedule.
        carry_forward_unpaid_liabilities (Union[Unset, bool]): If set to true then any unpaid amounts from previous
            periods will be brought forward
            to work out the liability for the current period.
            You'd set this to false if you don't want to track payments.
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    office_number: Union[Unset, None, str] = UNSET
    paye_reference: Union[Unset, None, str] = UNSET
    accounts_office_reference: Union[Unset, None, str] = UNSET
    econ: Union[Unset, None, str] = UNSET
    utr: Union[Unset, None, str] = UNSET
    co_tax: Union[Unset, None, str] = UNSET
    employment_allowance: Union[Unset, bool] = UNSET
    employment_allowance_max_claim: Union[Unset, float] = UNSET
    small_employers_relief: Union[Unset, bool] = UNSET
    apprenticeship_levy: Union[Unset, bool] = UNSET
    apprenticeship_levy_allowance: Union[Unset, float] = UNSET
    quarterly_payment_schedule: Union[Unset, bool] = UNSET
    include_employment_allowance_on_monthly_journal: Union[Unset, bool] = UNSET
    carry_forward_unpaid_liabilities: Union[Unset, bool] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        office_number = self.office_number
        paye_reference = self.paye_reference
        accounts_office_reference = self.accounts_office_reference
        econ = self.econ
        utr = self.utr
        co_tax = self.co_tax
        employment_allowance = self.employment_allowance
        employment_allowance_max_claim = self.employment_allowance_max_claim
        small_employers_relief = self.small_employers_relief
        apprenticeship_levy = self.apprenticeship_levy
        apprenticeship_levy_allowance = self.apprenticeship_levy_allowance
        quarterly_payment_schedule = self.quarterly_payment_schedule
        include_employment_allowance_on_monthly_journal = (
            self.include_employment_allowance_on_monthly_journal
        )
        carry_forward_unpaid_liabilities = self.carry_forward_unpaid_liabilities
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if office_number is not UNSET:
            field_dict["officeNumber"] = office_number
        if paye_reference is not UNSET:
            field_dict["payeReference"] = paye_reference
        if accounts_office_reference is not UNSET:
            field_dict["accountsOfficeReference"] = accounts_office_reference
        if econ is not UNSET:
            field_dict["econ"] = econ
        if utr is not UNSET:
            field_dict["utr"] = utr
        if co_tax is not UNSET:
            field_dict["coTax"] = co_tax
        if employment_allowance is not UNSET:
            field_dict["employmentAllowance"] = employment_allowance
        if employment_allowance_max_claim is not UNSET:
            field_dict["employmentAllowanceMaxClaim"] = employment_allowance_max_claim
        if small_employers_relief is not UNSET:
            field_dict["smallEmployersRelief"] = small_employers_relief
        if apprenticeship_levy is not UNSET:
            field_dict["apprenticeshipLevy"] = apprenticeship_levy
        if apprenticeship_levy_allowance is not UNSET:
            field_dict["apprenticeshipLevyAllowance"] = apprenticeship_levy_allowance
        if quarterly_payment_schedule is not UNSET:
            field_dict["quarterlyPaymentSchedule"] = quarterly_payment_schedule
        if include_employment_allowance_on_monthly_journal is not UNSET:
            field_dict[
                "includeEmploymentAllowanceOnMonthlyJournal"
            ] = include_employment_allowance_on_monthly_journal
        if carry_forward_unpaid_liabilities is not UNSET:
            field_dict[
                "carryForwardUnpaidLiabilities"
            ] = carry_forward_unpaid_liabilities
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        office_number = d.pop("officeNumber", UNSET)

        paye_reference = d.pop("payeReference", UNSET)

        accounts_office_reference = d.pop("accountsOfficeReference", UNSET)

        econ = d.pop("econ", UNSET)

        utr = d.pop("utr", UNSET)

        co_tax = d.pop("coTax", UNSET)

        employment_allowance = d.pop("employmentAllowance", UNSET)

        employment_allowance_max_claim = d.pop("employmentAllowanceMaxClaim", UNSET)

        small_employers_relief = d.pop("smallEmployersRelief", UNSET)

        apprenticeship_levy = d.pop("apprenticeshipLevy", UNSET)

        apprenticeship_levy_allowance = d.pop("apprenticeshipLevyAllowance", UNSET)

        quarterly_payment_schedule = d.pop("quarterlyPaymentSchedule", UNSET)

        include_employment_allowance_on_monthly_journal = d.pop(
            "includeEmploymentAllowanceOnMonthlyJournal", UNSET
        )

        carry_forward_unpaid_liabilities = d.pop("carryForwardUnpaidLiabilities", UNSET)

        id = d.pop("id", UNSET)

        hmrc_details = cls(
            office_number=office_number,
            paye_reference=paye_reference,
            accounts_office_reference=accounts_office_reference,
            econ=econ,
            utr=utr,
            co_tax=co_tax,
            employment_allowance=employment_allowance,
            employment_allowance_max_claim=employment_allowance_max_claim,
            small_employers_relief=small_employers_relief,
            apprenticeship_levy=apprenticeship_levy,
            apprenticeship_levy_allowance=apprenticeship_levy_allowance,
            quarterly_payment_schedule=quarterly_payment_schedule,
            include_employment_allowance_on_monthly_journal=include_employment_allowance_on_monthly_journal,
            carry_forward_unpaid_liabilities=carry_forward_unpaid_liabilities,
            id=id,
        )

        return hmrc_details
