import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.address import Address
from ..models.employment_details import EmploymentDetails
from ..models.hmrc_details import HmrcDetails
from ..models.item import Item
from ..models.pay_options import PayOptions
from ..models.pay_run_totals import PayRunTotals
from ..models.payslip_line import PayslipLine
from ..models.personal_details import PersonalDetails
from ..types import UNSET, Unset

T = TypeVar("T", bound="Payslip")


@attr.s(auto_attribs=True)
class Payslip:
    """If you don't want to use our customisable PDFs for Payslips then you can retrieve the raw data used to create a
    Payslip.
    This is the model you will be provided with for each employee.

        Attributes:
            is_closed (Union[Unset, bool]): [readonly] Indicates if the Payrun has been finalised
            period (Union[Unset, None, str]): [readonly] A description of the period that Payslip relates to.
            from_ (Union[Unset, datetime.date]): [readonly] The start date of the period this Payslip covers.
            to (Union[Unset, datetime.date]): [readonly] The end date of the period this Payslip covers.
            payment_date (Union[Unset, datetime.date]): [readonly] The date the Employee will be paid on
            note (Union[Unset, None, str]): [readonly] Any note that should appear on the payslip
            allowance_note (Union[Unset, None, str]): [readonly] Details of remaining allowance to show on payslip
            employee (Union[Unset, Item]):
            logo_url (Union[Unset, None, str]): [readonly] The Logo to include on the payslip
            employer (Union[Unset, Item]):
            employer_address (Union[Unset, Address]):
            hmrc_details (Union[Unset, HmrcDetails]):
            pay_options (Union[Unset, PayOptions]): This object forms the basis of the Employees payment.
            employment_details (Union[Unset, EmploymentDetails]):
            personal_details (Union[Unset, PersonalDetails]):
            totals (Union[Unset, PayRunTotals]): Used to represent totals for a PayRun or PayRunEntry.
                If a value is 0 then it will not be shown in the JSON.
            totals_ytd (Union[Unset, PayRunTotals]): Used to represent totals for a PayRun or PayRunEntry.
                If a value is 0 then it will not be shown in the JSON.
            lines (Union[Unset, None, List[PayslipLine]]): [readonly] The lines to display on the Payslip
            employer_ni (Union[Unset, float]): [readonly] The Employer NI Contribution amount
            employer_pension_contribs (Union[Unset, float]): [readonly] AThe Employer Pension Contribution Amount
    """

    is_closed: Union[Unset, bool] = UNSET
    period: Union[Unset, None, str] = UNSET
    from_: Union[Unset, datetime.date] = UNSET
    to: Union[Unset, datetime.date] = UNSET
    payment_date: Union[Unset, datetime.date] = UNSET
    note: Union[Unset, None, str] = UNSET
    allowance_note: Union[Unset, None, str] = UNSET
    employee: Union[Unset, Item] = UNSET
    logo_url: Union[Unset, None, str] = UNSET
    employer: Union[Unset, Item] = UNSET
    employer_address: Union[Unset, Address] = UNSET
    hmrc_details: Union[Unset, HmrcDetails] = UNSET
    pay_options: Union[Unset, PayOptions] = UNSET
    employment_details: Union[Unset, EmploymentDetails] = UNSET
    personal_details: Union[Unset, PersonalDetails] = UNSET
    totals: Union[Unset, PayRunTotals] = UNSET
    totals_ytd: Union[Unset, PayRunTotals] = UNSET
    lines: Union[Unset, None, List[PayslipLine]] = UNSET
    employer_ni: Union[Unset, float] = UNSET
    employer_pension_contribs: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        is_closed = self.is_closed
        period = self.period
        from_: Union[Unset, str] = UNSET
        if not isinstance(self.from_, Unset):
            from_ = self.from_.isoformat()

        to: Union[Unset, str] = UNSET
        if not isinstance(self.to, Unset):
            to = self.to.isoformat()

        payment_date: Union[Unset, str] = UNSET
        if not isinstance(self.payment_date, Unset):
            payment_date = self.payment_date.isoformat()

        note = self.note
        allowance_note = self.allowance_note
        employee: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employee, Unset):
            employee = self.employee.to_dict()

        logo_url = self.logo_url
        employer: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employer, Unset):
            employer = self.employer.to_dict()

        employer_address: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employer_address, Unset):
            employer_address = self.employer_address.to_dict()

        hmrc_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.hmrc_details, Unset):
            hmrc_details = self.hmrc_details.to_dict()

        pay_options: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.pay_options, Unset):
            pay_options = self.pay_options.to_dict()

        employment_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employment_details, Unset):
            employment_details = self.employment_details.to_dict()

        personal_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.personal_details, Unset):
            personal_details = self.personal_details.to_dict()

        totals: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.totals, Unset):
            totals = self.totals.to_dict()

        totals_ytd: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.totals_ytd, Unset):
            totals_ytd = self.totals_ytd.to_dict()

        lines: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.lines, Unset):
            if self.lines is None:
                lines = None
            else:
                lines = []
                for lines_item_data in self.lines:
                    lines_item = lines_item_data.to_dict()

                    lines.append(lines_item)

        employer_ni = self.employer_ni
        employer_pension_contribs = self.employer_pension_contribs

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if is_closed is not UNSET:
            field_dict["isClosed"] = is_closed
        if period is not UNSET:
            field_dict["period"] = period
        if from_ is not UNSET:
            field_dict["from"] = from_
        if to is not UNSET:
            field_dict["to"] = to
        if payment_date is not UNSET:
            field_dict["paymentDate"] = payment_date
        if note is not UNSET:
            field_dict["note"] = note
        if allowance_note is not UNSET:
            field_dict["allowanceNote"] = allowance_note
        if employee is not UNSET:
            field_dict["employee"] = employee
        if logo_url is not UNSET:
            field_dict["logoUrl"] = logo_url
        if employer is not UNSET:
            field_dict["employer"] = employer
        if employer_address is not UNSET:
            field_dict["employerAddress"] = employer_address
        if hmrc_details is not UNSET:
            field_dict["hmrcDetails"] = hmrc_details
        if pay_options is not UNSET:
            field_dict["payOptions"] = pay_options
        if employment_details is not UNSET:
            field_dict["employmentDetails"] = employment_details
        if personal_details is not UNSET:
            field_dict["personalDetails"] = personal_details
        if totals is not UNSET:
            field_dict["totals"] = totals
        if totals_ytd is not UNSET:
            field_dict["totalsYtd"] = totals_ytd
        if lines is not UNSET:
            field_dict["lines"] = lines
        if employer_ni is not UNSET:
            field_dict["employerNi"] = employer_ni
        if employer_pension_contribs is not UNSET:
            field_dict["employerPensionContribs"] = employer_pension_contribs

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        is_closed = d.pop("isClosed", UNSET)

        period = d.pop("period", UNSET)

        _from_ = d.pop("from", UNSET)
        from_: Union[Unset, datetime.date]
        if isinstance(_from_, Unset):
            from_ = UNSET
        else:
            from_ = isoparse(_from_).date()

        _to = d.pop("to", UNSET)
        to: Union[Unset, datetime.date]
        if isinstance(_to, Unset):
            to = UNSET
        else:
            to = isoparse(_to).date()

        _payment_date = d.pop("paymentDate", UNSET)
        payment_date: Union[Unset, datetime.date]
        if isinstance(_payment_date, Unset):
            payment_date = UNSET
        else:
            payment_date = isoparse(_payment_date).date()

        note = d.pop("note", UNSET)

        allowance_note = d.pop("allowanceNote", UNSET)

        _employee = d.pop("employee", UNSET)
        employee: Union[Unset, Item]
        if isinstance(_employee, Unset):
            employee = UNSET
        else:
            employee = Item.from_dict(_employee)

        logo_url = d.pop("logoUrl", UNSET)

        _employer = d.pop("employer", UNSET)
        employer: Union[Unset, Item]
        if isinstance(_employer, Unset):
            employer = UNSET
        else:
            employer = Item.from_dict(_employer)

        _employer_address = d.pop("employerAddress", UNSET)
        employer_address: Union[Unset, Address]
        if isinstance(_employer_address, Unset):
            employer_address = UNSET
        else:
            employer_address = Address.from_dict(_employer_address)

        _hmrc_details = d.pop("hmrcDetails", UNSET)
        hmrc_details: Union[Unset, HmrcDetails]
        if isinstance(_hmrc_details, Unset):
            hmrc_details = UNSET
        else:
            hmrc_details = HmrcDetails.from_dict(_hmrc_details)

        _pay_options = d.pop("payOptions", UNSET)
        pay_options: Union[Unset, PayOptions]
        if isinstance(_pay_options, Unset):
            pay_options = UNSET
        else:
            pay_options = PayOptions.from_dict(_pay_options)

        _employment_details = d.pop("employmentDetails", UNSET)
        employment_details: Union[Unset, EmploymentDetails]
        if isinstance(_employment_details, Unset):
            employment_details = UNSET
        else:
            employment_details = EmploymentDetails.from_dict(_employment_details)

        _personal_details = d.pop("personalDetails", UNSET)
        personal_details: Union[Unset, PersonalDetails]
        if isinstance(_personal_details, Unset):
            personal_details = UNSET
        else:
            personal_details = PersonalDetails.from_dict(_personal_details)

        _totals = d.pop("totals", UNSET)
        totals: Union[Unset, PayRunTotals]
        if isinstance(_totals, Unset):
            totals = UNSET
        else:
            totals = PayRunTotals.from_dict(_totals)

        _totals_ytd = d.pop("totalsYtd", UNSET)
        totals_ytd: Union[Unset, PayRunTotals]
        if isinstance(_totals_ytd, Unset):
            totals_ytd = UNSET
        else:
            totals_ytd = PayRunTotals.from_dict(_totals_ytd)

        lines = []
        _lines = d.pop("lines", UNSET)
        for lines_item_data in _lines or []:
            lines_item = PayslipLine.from_dict(lines_item_data)

            lines.append(lines_item)

        employer_ni = d.pop("employerNi", UNSET)

        employer_pension_contribs = d.pop("employerPensionContribs", UNSET)

        payslip = cls(
            is_closed=is_closed,
            period=period,
            from_=from_,
            to=to,
            payment_date=payment_date,
            note=note,
            allowance_note=allowance_note,
            employee=employee,
            logo_url=logo_url,
            employer=employer,
            employer_address=employer_address,
            hmrc_details=hmrc_details,
            pay_options=pay_options,
            employment_details=employment_details,
            personal_details=personal_details,
            totals=totals,
            totals_ytd=totals_ytd,
            lines=lines,
            employer_ni=employer_ni,
            employer_pension_contribs=employer_pension_contribs,
        )

        return payslip
