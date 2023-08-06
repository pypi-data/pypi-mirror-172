import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="BenefitDetailsLoan")


@attr.s(auto_attribs=True)
class BenefitDetailsLoan:
    """
    Attributes:
        number_of_joint_borrowers (Union[Unset, None, int]):
        loan_made (Union[Unset, None, datetime.date]):
        loan_discharged (Union[Unset, None, datetime.date]):
        starting_balance (Union[Unset, float]):
        closing_balance (Union[Unset, float]):
        max_balance_in_year (Union[Unset, float]):
        interest_paid (Union[Unset, float]):
        cash_equivalent (Union[Unset, float]): [readonly]
        full_tax_months (Union[Unset, int]): [readonly]
        monthly_value (Union[Unset, float]): [readonly]
        official_interest (Union[Unset, float]): [readonly]
    """

    number_of_joint_borrowers: Union[Unset, None, int] = UNSET
    loan_made: Union[Unset, None, datetime.date] = UNSET
    loan_discharged: Union[Unset, None, datetime.date] = UNSET
    starting_balance: Union[Unset, float] = UNSET
    closing_balance: Union[Unset, float] = UNSET
    max_balance_in_year: Union[Unset, float] = UNSET
    interest_paid: Union[Unset, float] = UNSET
    cash_equivalent: Union[Unset, float] = UNSET
    full_tax_months: Union[Unset, int] = UNSET
    monthly_value: Union[Unset, float] = UNSET
    official_interest: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        number_of_joint_borrowers = self.number_of_joint_borrowers
        loan_made: Union[Unset, None, str] = UNSET
        if not isinstance(self.loan_made, Unset):
            loan_made = self.loan_made.isoformat() if self.loan_made else None

        loan_discharged: Union[Unset, None, str] = UNSET
        if not isinstance(self.loan_discharged, Unset):
            loan_discharged = (
                self.loan_discharged.isoformat() if self.loan_discharged else None
            )

        starting_balance = self.starting_balance
        closing_balance = self.closing_balance
        max_balance_in_year = self.max_balance_in_year
        interest_paid = self.interest_paid
        cash_equivalent = self.cash_equivalent
        full_tax_months = self.full_tax_months
        monthly_value = self.monthly_value
        official_interest = self.official_interest

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if number_of_joint_borrowers is not UNSET:
            field_dict["numberOfJointBorrowers"] = number_of_joint_borrowers
        if loan_made is not UNSET:
            field_dict["loanMade"] = loan_made
        if loan_discharged is not UNSET:
            field_dict["loanDischarged"] = loan_discharged
        if starting_balance is not UNSET:
            field_dict["startingBalance"] = starting_balance
        if closing_balance is not UNSET:
            field_dict["closingBalance"] = closing_balance
        if max_balance_in_year is not UNSET:
            field_dict["maxBalanceInYear"] = max_balance_in_year
        if interest_paid is not UNSET:
            field_dict["interestPaid"] = interest_paid
        if cash_equivalent is not UNSET:
            field_dict["cashEquivalent"] = cash_equivalent
        if full_tax_months is not UNSET:
            field_dict["fullTaxMonths"] = full_tax_months
        if monthly_value is not UNSET:
            field_dict["monthlyValue"] = monthly_value
        if official_interest is not UNSET:
            field_dict["officialInterest"] = official_interest

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        number_of_joint_borrowers = d.pop("numberOfJointBorrowers", UNSET)

        _loan_made = d.pop("loanMade", UNSET)
        loan_made: Union[Unset, None, datetime.date]
        if _loan_made is None:
            loan_made = None
        elif isinstance(_loan_made, Unset):
            loan_made = UNSET
        else:
            loan_made = isoparse(_loan_made).date()

        _loan_discharged = d.pop("loanDischarged", UNSET)
        loan_discharged: Union[Unset, None, datetime.date]
        if _loan_discharged is None:
            loan_discharged = None
        elif isinstance(_loan_discharged, Unset):
            loan_discharged = UNSET
        else:
            loan_discharged = isoparse(_loan_discharged).date()

        starting_balance = d.pop("startingBalance", UNSET)

        closing_balance = d.pop("closingBalance", UNSET)

        max_balance_in_year = d.pop("maxBalanceInYear", UNSET)

        interest_paid = d.pop("interestPaid", UNSET)

        cash_equivalent = d.pop("cashEquivalent", UNSET)

        full_tax_months = d.pop("fullTaxMonths", UNSET)

        monthly_value = d.pop("monthlyValue", UNSET)

        official_interest = d.pop("officialInterest", UNSET)

        benefit_details_loan = cls(
            number_of_joint_borrowers=number_of_joint_borrowers,
            loan_made=loan_made,
            loan_discharged=loan_discharged,
            starting_balance=starting_balance,
            closing_balance=closing_balance,
            max_balance_in_year=max_balance_in_year,
            interest_paid=interest_paid,
            cash_equivalent=cash_equivalent,
            full_tax_months=full_tax_months,
            monthly_value=monthly_value,
            official_interest=official_interest,
        )

        return benefit_details_loan
