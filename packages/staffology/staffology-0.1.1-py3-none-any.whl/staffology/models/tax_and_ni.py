import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.student_loan import StudentLoan
from ..types import UNSET, Unset

T = TypeVar("T", bound="TaxAndNi")


@attr.s(auto_attribs=True)
class TaxAndNi:
    """
    Attributes:
        ni_table (str): The appropriate NI letter for this Employee
        secondary_class_1_not_payable (Union[Unset, bool]): If set to true then no Employer NI will be paid for this
            Employee
        postgrad_loan (Union[Unset, bool]): Set to true if the Employee needs to make Post Graduate Loan repayments
        postgraduate_loan_start_date (Union[Unset, None, datetime.date]):
        postgraduate_loan_end_date (Union[Unset, None, datetime.date]):
        student_loan (Union[Unset, StudentLoan]):
        student_loan_start_date (Union[Unset, None, datetime.date]):
        student_loan_end_date (Union[Unset, None, datetime.date]):
        tax_code (Union[Unset, None, str]): The Tax Code for this Employee
        week_1_month_1 (Union[Unset, bool]): Determines whether PAYE should be calculated on a Week1/Month1 basis
            instead of on a cumulative basis.
            This is automatically set to false for any existing Employees when you start a new Tax Year.
    """

    ni_table: str
    secondary_class_1_not_payable: Union[Unset, bool] = UNSET
    postgrad_loan: Union[Unset, bool] = UNSET
    postgraduate_loan_start_date: Union[Unset, None, datetime.date] = UNSET
    postgraduate_loan_end_date: Union[Unset, None, datetime.date] = UNSET
    student_loan: Union[Unset, StudentLoan] = UNSET
    student_loan_start_date: Union[Unset, None, datetime.date] = UNSET
    student_loan_end_date: Union[Unset, None, datetime.date] = UNSET
    tax_code: Union[Unset, None, str] = UNSET
    week_1_month_1: Union[Unset, bool] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        ni_table = self.ni_table
        secondary_class_1_not_payable = self.secondary_class_1_not_payable
        postgrad_loan = self.postgrad_loan
        postgraduate_loan_start_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.postgraduate_loan_start_date, Unset):
            postgraduate_loan_start_date = (
                self.postgraduate_loan_start_date.isoformat()
                if self.postgraduate_loan_start_date
                else None
            )

        postgraduate_loan_end_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.postgraduate_loan_end_date, Unset):
            postgraduate_loan_end_date = (
                self.postgraduate_loan_end_date.isoformat()
                if self.postgraduate_loan_end_date
                else None
            )

        student_loan: Union[Unset, str] = UNSET
        if not isinstance(self.student_loan, Unset):
            student_loan = self.student_loan.value

        student_loan_start_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.student_loan_start_date, Unset):
            student_loan_start_date = (
                self.student_loan_start_date.isoformat()
                if self.student_loan_start_date
                else None
            )

        student_loan_end_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.student_loan_end_date, Unset):
            student_loan_end_date = (
                self.student_loan_end_date.isoformat()
                if self.student_loan_end_date
                else None
            )

        tax_code = self.tax_code
        week_1_month_1 = self.week_1_month_1

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "niTable": ni_table,
            }
        )
        if secondary_class_1_not_payable is not UNSET:
            field_dict["secondaryClass1NotPayable"] = secondary_class_1_not_payable
        if postgrad_loan is not UNSET:
            field_dict["postgradLoan"] = postgrad_loan
        if postgraduate_loan_start_date is not UNSET:
            field_dict["postgraduateLoanStartDate"] = postgraduate_loan_start_date
        if postgraduate_loan_end_date is not UNSET:
            field_dict["postgraduateLoanEndDate"] = postgraduate_loan_end_date
        if student_loan is not UNSET:
            field_dict["studentLoan"] = student_loan
        if student_loan_start_date is not UNSET:
            field_dict["studentLoanStartDate"] = student_loan_start_date
        if student_loan_end_date is not UNSET:
            field_dict["studentLoanEndDate"] = student_loan_end_date
        if tax_code is not UNSET:
            field_dict["taxCode"] = tax_code
        if week_1_month_1 is not UNSET:
            field_dict["week1Month1"] = week_1_month_1

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        ni_table = d.pop("niTable")

        secondary_class_1_not_payable = d.pop("secondaryClass1NotPayable", UNSET)

        postgrad_loan = d.pop("postgradLoan", UNSET)

        _postgraduate_loan_start_date = d.pop("postgraduateLoanStartDate", UNSET)
        postgraduate_loan_start_date: Union[Unset, None, datetime.date]
        if _postgraduate_loan_start_date is None:
            postgraduate_loan_start_date = None
        elif isinstance(_postgraduate_loan_start_date, Unset):
            postgraduate_loan_start_date = UNSET
        else:
            postgraduate_loan_start_date = isoparse(
                _postgraduate_loan_start_date
            ).date()

        _postgraduate_loan_end_date = d.pop("postgraduateLoanEndDate", UNSET)
        postgraduate_loan_end_date: Union[Unset, None, datetime.date]
        if _postgraduate_loan_end_date is None:
            postgraduate_loan_end_date = None
        elif isinstance(_postgraduate_loan_end_date, Unset):
            postgraduate_loan_end_date = UNSET
        else:
            postgraduate_loan_end_date = isoparse(_postgraduate_loan_end_date).date()

        _student_loan = d.pop("studentLoan", UNSET)
        student_loan: Union[Unset, StudentLoan]
        if isinstance(_student_loan, Unset):
            student_loan = UNSET
        else:
            student_loan = StudentLoan(_student_loan)

        _student_loan_start_date = d.pop("studentLoanStartDate", UNSET)
        student_loan_start_date: Union[Unset, None, datetime.date]
        if _student_loan_start_date is None:
            student_loan_start_date = None
        elif isinstance(_student_loan_start_date, Unset):
            student_loan_start_date = UNSET
        else:
            student_loan_start_date = isoparse(_student_loan_start_date).date()

        _student_loan_end_date = d.pop("studentLoanEndDate", UNSET)
        student_loan_end_date: Union[Unset, None, datetime.date]
        if _student_loan_end_date is None:
            student_loan_end_date = None
        elif isinstance(_student_loan_end_date, Unset):
            student_loan_end_date = UNSET
        else:
            student_loan_end_date = isoparse(_student_loan_end_date).date()

        tax_code = d.pop("taxCode", UNSET)

        week_1_month_1 = d.pop("week1Month1", UNSET)

        tax_and_ni = cls(
            ni_table=ni_table,
            secondary_class_1_not_payable=secondary_class_1_not_payable,
            postgrad_loan=postgrad_loan,
            postgraduate_loan_start_date=postgraduate_loan_start_date,
            postgraduate_loan_end_date=postgraduate_loan_end_date,
            student_loan=student_loan,
            student_loan_start_date=student_loan_start_date,
            student_loan_end_date=student_loan_end_date,
            tax_code=tax_code,
            week_1_month_1=week_1_month_1,
        )

        return tax_and_ni
