import datetime
from typing import Any, Dict, List, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.cis_details import CisDetails
from ..models.department import Department
from ..models.directorship_details import DirectorshipDetails
from ..models.furlough_calculation_basis import FurloughCalculationBasis
from ..models.item import Item
from ..models.leaver_details import LeaverDetails
from ..models.starter_details import StarterDetails
from ..models.veteran_details import VeteranDetails
from ..types import UNSET, Unset

T = TypeVar("T", bound="EmploymentDetails")


@attr.s(auto_attribs=True)
class EmploymentDetails:
    """
    Attributes:
        payroll_code (str): The Employees Payroll Code. Must be unique within the Employer.
        cis_sub_contractor (Union[Unset, bool]): Set to True if this Employee is a CIS Subcontractor. The
            <code>Cis</code> property contains further information
        job_title (Union[Unset, None, str]): Job Title of Primary post of the Employee
        on_hold (Union[Unset, bool]): Set to true to temporarily exclude the employee from payruns
        on_furlough (Union[Unset, bool]): Set to true if the employee is on furlough.
        furlough_start (Union[Unset, None, datetime.date]): Furlough Start Date.
        furlough_end (Union[Unset, None, datetime.date]): Furlough End Date.
        furlough_calculation_basis (Union[Unset, FurloughCalculationBasis]):
        furlough_calculation_basis_amount (Union[Unset, float]):
        partial_furlough (Union[Unset, bool]): Set to true if the employee is partially furloughed.
        furlough_hours_normally_worked (Union[Unset, float]):
        furlough_hours_on_furlough (Union[Unset, float]):
        is_apprentice (Union[Unset, bool]): Set to True if this Employee is an apprentice. This affects the calculations
            for National Minimum Wage
        apprenticeship_start_date (Union[Unset, None, datetime.date]):
        apprenticeship_end_date (Union[Unset, None, datetime.date]):
        working_pattern (Union[Unset, None, str]): Used when calculating payments for Leave.
            If null then the default Working Pattern is used
        force_previous_payroll_code (Union[Unset, None, str]): If this property has a non-empty value then a change of
            Payroll code will be declared on the next FPS.
        starter_details (Union[Unset, StarterDetails]):
        directorship_details (Union[Unset, DirectorshipDetails]):
        leaver_details (Union[Unset, LeaverDetails]):
        cis (Union[Unset, CisDetails]): If an Employee is marked as a CIS Subcontractor then this model provides further
            details specifically related to the CIS details of the Employee.
        department (Union[Unset, Department]):
        posts (Union[Unset, None, List[Item]]): List of Posts held by Employee
        is_working_in_free_port (Union[Unset, bool]): Flag indicating the employee is employed in a Freeport
        veteran_details (Union[Unset, VeteranDetails]): Employment details for veterans
    """

    payroll_code: str
    cis_sub_contractor: Union[Unset, bool] = UNSET
    job_title: Union[Unset, None, str] = UNSET
    on_hold: Union[Unset, bool] = UNSET
    on_furlough: Union[Unset, bool] = UNSET
    furlough_start: Union[Unset, None, datetime.date] = UNSET
    furlough_end: Union[Unset, None, datetime.date] = UNSET
    furlough_calculation_basis: Union[Unset, FurloughCalculationBasis] = UNSET
    furlough_calculation_basis_amount: Union[Unset, float] = UNSET
    partial_furlough: Union[Unset, bool] = UNSET
    furlough_hours_normally_worked: Union[Unset, float] = UNSET
    furlough_hours_on_furlough: Union[Unset, float] = UNSET
    is_apprentice: Union[Unset, bool] = UNSET
    apprenticeship_start_date: Union[Unset, None, datetime.date] = UNSET
    apprenticeship_end_date: Union[Unset, None, datetime.date] = UNSET
    working_pattern: Union[Unset, None, str] = UNSET
    force_previous_payroll_code: Union[Unset, None, str] = UNSET
    starter_details: Union[Unset, StarterDetails] = UNSET
    directorship_details: Union[Unset, DirectorshipDetails] = UNSET
    leaver_details: Union[Unset, LeaverDetails] = UNSET
    cis: Union[Unset, CisDetails] = UNSET
    department: Union[Unset, Department] = UNSET
    posts: Union[Unset, None, List[Item]] = UNSET
    is_working_in_free_port: Union[Unset, bool] = UNSET
    veteran_details: Union[Unset, VeteranDetails] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        payroll_code = self.payroll_code
        cis_sub_contractor = self.cis_sub_contractor
        job_title = self.job_title
        on_hold = self.on_hold
        on_furlough = self.on_furlough
        furlough_start: Union[Unset, None, str] = UNSET
        if not isinstance(self.furlough_start, Unset):
            furlough_start = (
                self.furlough_start.isoformat() if self.furlough_start else None
            )

        furlough_end: Union[Unset, None, str] = UNSET
        if not isinstance(self.furlough_end, Unset):
            furlough_end = self.furlough_end.isoformat() if self.furlough_end else None

        furlough_calculation_basis: Union[Unset, str] = UNSET
        if not isinstance(self.furlough_calculation_basis, Unset):
            furlough_calculation_basis = self.furlough_calculation_basis.value

        furlough_calculation_basis_amount = self.furlough_calculation_basis_amount
        partial_furlough = self.partial_furlough
        furlough_hours_normally_worked = self.furlough_hours_normally_worked
        furlough_hours_on_furlough = self.furlough_hours_on_furlough
        is_apprentice = self.is_apprentice
        apprenticeship_start_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.apprenticeship_start_date, Unset):
            apprenticeship_start_date = (
                self.apprenticeship_start_date.isoformat()
                if self.apprenticeship_start_date
                else None
            )

        apprenticeship_end_date: Union[Unset, None, str] = UNSET
        if not isinstance(self.apprenticeship_end_date, Unset):
            apprenticeship_end_date = (
                self.apprenticeship_end_date.isoformat()
                if self.apprenticeship_end_date
                else None
            )

        working_pattern = self.working_pattern
        force_previous_payroll_code = self.force_previous_payroll_code
        starter_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.starter_details, Unset):
            starter_details = self.starter_details.to_dict()

        directorship_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.directorship_details, Unset):
            directorship_details = self.directorship_details.to_dict()

        leaver_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.leaver_details, Unset):
            leaver_details = self.leaver_details.to_dict()

        cis: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.cis, Unset):
            cis = self.cis.to_dict()

        department: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.department, Unset):
            department = self.department.to_dict()

        posts: Union[Unset, None, List[Dict[str, Any]]] = UNSET
        if not isinstance(self.posts, Unset):
            if self.posts is None:
                posts = None
            else:
                posts = []
                for posts_item_data in self.posts:
                    posts_item = posts_item_data.to_dict()

                    posts.append(posts_item)

        is_working_in_free_port = self.is_working_in_free_port
        veteran_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.veteran_details, Unset):
            veteran_details = self.veteran_details.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "payrollCode": payroll_code,
            }
        )
        if cis_sub_contractor is not UNSET:
            field_dict["cisSubContractor"] = cis_sub_contractor
        if job_title is not UNSET:
            field_dict["jobTitle"] = job_title
        if on_hold is not UNSET:
            field_dict["onHold"] = on_hold
        if on_furlough is not UNSET:
            field_dict["onFurlough"] = on_furlough
        if furlough_start is not UNSET:
            field_dict["furloughStart"] = furlough_start
        if furlough_end is not UNSET:
            field_dict["furloughEnd"] = furlough_end
        if furlough_calculation_basis is not UNSET:
            field_dict["furloughCalculationBasis"] = furlough_calculation_basis
        if furlough_calculation_basis_amount is not UNSET:
            field_dict[
                "furloughCalculationBasisAmount"
            ] = furlough_calculation_basis_amount
        if partial_furlough is not UNSET:
            field_dict["partialFurlough"] = partial_furlough
        if furlough_hours_normally_worked is not UNSET:
            field_dict["furloughHoursNormallyWorked"] = furlough_hours_normally_worked
        if furlough_hours_on_furlough is not UNSET:
            field_dict["furloughHoursOnFurlough"] = furlough_hours_on_furlough
        if is_apprentice is not UNSET:
            field_dict["isApprentice"] = is_apprentice
        if apprenticeship_start_date is not UNSET:
            field_dict["apprenticeshipStartDate"] = apprenticeship_start_date
        if apprenticeship_end_date is not UNSET:
            field_dict["apprenticeshipEndDate"] = apprenticeship_end_date
        if working_pattern is not UNSET:
            field_dict["workingPattern"] = working_pattern
        if force_previous_payroll_code is not UNSET:
            field_dict["forcePreviousPayrollCode"] = force_previous_payroll_code
        if starter_details is not UNSET:
            field_dict["starterDetails"] = starter_details
        if directorship_details is not UNSET:
            field_dict["directorshipDetails"] = directorship_details
        if leaver_details is not UNSET:
            field_dict["leaverDetails"] = leaver_details
        if cis is not UNSET:
            field_dict["cis"] = cis
        if department is not UNSET:
            field_dict["department"] = department
        if posts is not UNSET:
            field_dict["posts"] = posts
        if is_working_in_free_port is not UNSET:
            field_dict["isWorkingInFreePort"] = is_working_in_free_port
        if veteran_details is not UNSET:
            field_dict["veteranDetails"] = veteran_details

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        payroll_code = d.pop("payrollCode")

        cis_sub_contractor = d.pop("cisSubContractor", UNSET)

        job_title = d.pop("jobTitle", UNSET)

        on_hold = d.pop("onHold", UNSET)

        on_furlough = d.pop("onFurlough", UNSET)

        _furlough_start = d.pop("furloughStart", UNSET)
        furlough_start: Union[Unset, None, datetime.date]
        if _furlough_start is None:
            furlough_start = None
        elif isinstance(_furlough_start, Unset):
            furlough_start = UNSET
        else:
            furlough_start = isoparse(_furlough_start).date()

        _furlough_end = d.pop("furloughEnd", UNSET)
        furlough_end: Union[Unset, None, datetime.date]
        if _furlough_end is None:
            furlough_end = None
        elif isinstance(_furlough_end, Unset):
            furlough_end = UNSET
        else:
            furlough_end = isoparse(_furlough_end).date()

        _furlough_calculation_basis = d.pop("furloughCalculationBasis", UNSET)
        furlough_calculation_basis: Union[Unset, FurloughCalculationBasis]
        if isinstance(_furlough_calculation_basis, Unset):
            furlough_calculation_basis = UNSET
        else:
            furlough_calculation_basis = FurloughCalculationBasis(
                _furlough_calculation_basis
            )

        furlough_calculation_basis_amount = d.pop(
            "furloughCalculationBasisAmount", UNSET
        )

        partial_furlough = d.pop("partialFurlough", UNSET)

        furlough_hours_normally_worked = d.pop("furloughHoursNormallyWorked", UNSET)

        furlough_hours_on_furlough = d.pop("furloughHoursOnFurlough", UNSET)

        is_apprentice = d.pop("isApprentice", UNSET)

        _apprenticeship_start_date = d.pop("apprenticeshipStartDate", UNSET)
        apprenticeship_start_date: Union[Unset, None, datetime.date]
        if _apprenticeship_start_date is None:
            apprenticeship_start_date = None
        elif isinstance(_apprenticeship_start_date, Unset):
            apprenticeship_start_date = UNSET
        else:
            apprenticeship_start_date = isoparse(_apprenticeship_start_date).date()

        _apprenticeship_end_date = d.pop("apprenticeshipEndDate", UNSET)
        apprenticeship_end_date: Union[Unset, None, datetime.date]
        if _apprenticeship_end_date is None:
            apprenticeship_end_date = None
        elif isinstance(_apprenticeship_end_date, Unset):
            apprenticeship_end_date = UNSET
        else:
            apprenticeship_end_date = isoparse(_apprenticeship_end_date).date()

        working_pattern = d.pop("workingPattern", UNSET)

        force_previous_payroll_code = d.pop("forcePreviousPayrollCode", UNSET)

        _starter_details = d.pop("starterDetails", UNSET)
        starter_details: Union[Unset, StarterDetails]
        if isinstance(_starter_details, Unset):
            starter_details = UNSET
        else:
            starter_details = StarterDetails.from_dict(_starter_details)

        _directorship_details = d.pop("directorshipDetails", UNSET)
        directorship_details: Union[Unset, DirectorshipDetails]
        if isinstance(_directorship_details, Unset):
            directorship_details = UNSET
        else:
            directorship_details = DirectorshipDetails.from_dict(_directorship_details)

        _leaver_details = d.pop("leaverDetails", UNSET)
        leaver_details: Union[Unset, LeaverDetails]
        if isinstance(_leaver_details, Unset):
            leaver_details = UNSET
        else:
            leaver_details = LeaverDetails.from_dict(_leaver_details)

        _cis = d.pop("cis", UNSET)
        cis: Union[Unset, CisDetails]
        if isinstance(_cis, Unset):
            cis = UNSET
        else:
            cis = CisDetails.from_dict(_cis)

        _department = d.pop("department", UNSET)
        department: Union[Unset, Department]
        if isinstance(_department, Unset):
            department = UNSET
        else:
            department = Department.from_dict(_department)

        posts = []
        _posts = d.pop("posts", UNSET)
        for posts_item_data in _posts or []:
            posts_item = Item.from_dict(posts_item_data)

            posts.append(posts_item)

        is_working_in_free_port = d.pop("isWorkingInFreePort", UNSET)

        _veteran_details = d.pop("veteranDetails", UNSET)
        veteran_details: Union[Unset, VeteranDetails]
        if isinstance(_veteran_details, Unset):
            veteran_details = UNSET
        else:
            veteran_details = VeteranDetails.from_dict(_veteran_details)

        employment_details = cls(
            payroll_code=payroll_code,
            cis_sub_contractor=cis_sub_contractor,
            job_title=job_title,
            on_hold=on_hold,
            on_furlough=on_furlough,
            furlough_start=furlough_start,
            furlough_end=furlough_end,
            furlough_calculation_basis=furlough_calculation_basis,
            furlough_calculation_basis_amount=furlough_calculation_basis_amount,
            partial_furlough=partial_furlough,
            furlough_hours_normally_worked=furlough_hours_normally_worked,
            furlough_hours_on_furlough=furlough_hours_on_furlough,
            is_apprentice=is_apprentice,
            apprenticeship_start_date=apprenticeship_start_date,
            apprenticeship_end_date=apprenticeship_end_date,
            working_pattern=working_pattern,
            force_previous_payroll_code=force_previous_payroll_code,
            starter_details=starter_details,
            directorship_details=directorship_details,
            leaver_details=leaver_details,
            cis=cis,
            department=department,
            posts=posts,
            is_working_in_free_port=is_working_in_free_port,
            veteran_details=veteran_details,
        )

        return employment_details
