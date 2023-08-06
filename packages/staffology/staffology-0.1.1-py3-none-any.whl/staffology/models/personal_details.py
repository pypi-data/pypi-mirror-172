import datetime
from typing import Any, Dict, Type, TypeVar, Union

import attr
from dateutil.parser import isoparse

from ..models.address import Address
from ..models.gender import Gender
from ..models.marital_status import MaritalStatus
from ..models.partner_details import PartnerDetails
from ..models.pdf_password_type import PdfPasswordType
from ..types import UNSET, Unset

T = TypeVar("T", bound="PersonalDetails")


@attr.s(auto_attribs=True)
class PersonalDetails:
    """
    Attributes:
        marital_status (MaritalStatus):
        date_of_birth (datetime.date):
        gender (Gender):
        address (Union[Unset, Address]):
        title (Union[Unset, None, str]):
        first_name (Union[Unset, None, str]):
        middle_name (Union[Unset, None, str]):
        last_name (Union[Unset, None, str]):
        email (Union[Unset, None, str]):
        email_payslip (Union[Unset, bool]): If set to true then the employees Payslip will be sent by email when a
            PayRun is finalised.
        password_protect_payslip (Union[Unset, bool]): If set to true then when a payslip is sent by email a password
            will be set on it.
        pdf_password (Union[Unset, None, str]): Set the password to be used on PDFs. If blank then we'll create a
            password based on the PdfPasswordType property.
        pdf_password_type (Union[Unset, PdfPasswordType]):
        email_statement (Union[Unset, bool]): Only applicable to CIS Subcontractors. If set to true then we will
            automatically email a CIS Statement when a CIS300 is accepted.
        photo_url (Union[Unset, None, str]):
        telephone (Union[Unset, None, str]):
        mobile (Union[Unset, None, str]):
        state_pension_age (Union[Unset, int]): [readonly] Automatically calculated.
        ni_number (Union[Unset, None, str]):
        passport_number (Union[Unset, None, str]):
        partner_details (Union[Unset, PartnerDetails]):
    """

    marital_status: MaritalStatus
    date_of_birth: datetime.date
    gender: Gender
    address: Union[Unset, Address] = UNSET
    title: Union[Unset, None, str] = UNSET
    first_name: Union[Unset, None, str] = UNSET
    middle_name: Union[Unset, None, str] = UNSET
    last_name: Union[Unset, None, str] = UNSET
    email: Union[Unset, None, str] = UNSET
    email_payslip: Union[Unset, bool] = UNSET
    password_protect_payslip: Union[Unset, bool] = UNSET
    pdf_password: Union[Unset, None, str] = UNSET
    pdf_password_type: Union[Unset, PdfPasswordType] = UNSET
    email_statement: Union[Unset, bool] = UNSET
    photo_url: Union[Unset, None, str] = UNSET
    telephone: Union[Unset, None, str] = UNSET
    mobile: Union[Unset, None, str] = UNSET
    state_pension_age: Union[Unset, int] = UNSET
    ni_number: Union[Unset, None, str] = UNSET
    passport_number: Union[Unset, None, str] = UNSET
    partner_details: Union[Unset, PartnerDetails] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        marital_status = self.marital_status.value

        date_of_birth = self.date_of_birth.isoformat()
        gender = self.gender.value

        address: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.address, Unset):
            address = self.address.to_dict()

        title = self.title
        first_name = self.first_name
        middle_name = self.middle_name
        last_name = self.last_name
        email = self.email
        email_payslip = self.email_payslip
        password_protect_payslip = self.password_protect_payslip
        pdf_password = self.pdf_password
        pdf_password_type: Union[Unset, str] = UNSET
        if not isinstance(self.pdf_password_type, Unset):
            pdf_password_type = self.pdf_password_type.value

        email_statement = self.email_statement
        photo_url = self.photo_url
        telephone = self.telephone
        mobile = self.mobile
        state_pension_age = self.state_pension_age
        ni_number = self.ni_number
        passport_number = self.passport_number
        partner_details: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.partner_details, Unset):
            partner_details = self.partner_details.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "maritalStatus": marital_status,
                "dateOfBirth": date_of_birth,
                "gender": gender,
            }
        )
        if address is not UNSET:
            field_dict["address"] = address
        if title is not UNSET:
            field_dict["title"] = title
        if first_name is not UNSET:
            field_dict["firstName"] = first_name
        if middle_name is not UNSET:
            field_dict["middleName"] = middle_name
        if last_name is not UNSET:
            field_dict["lastName"] = last_name
        if email is not UNSET:
            field_dict["email"] = email
        if email_payslip is not UNSET:
            field_dict["emailPayslip"] = email_payslip
        if password_protect_payslip is not UNSET:
            field_dict["passwordProtectPayslip"] = password_protect_payslip
        if pdf_password is not UNSET:
            field_dict["pdfPassword"] = pdf_password
        if pdf_password_type is not UNSET:
            field_dict["pdfPasswordType"] = pdf_password_type
        if email_statement is not UNSET:
            field_dict["emailStatement"] = email_statement
        if photo_url is not UNSET:
            field_dict["photoUrl"] = photo_url
        if telephone is not UNSET:
            field_dict["telephone"] = telephone
        if mobile is not UNSET:
            field_dict["mobile"] = mobile
        if state_pension_age is not UNSET:
            field_dict["statePensionAge"] = state_pension_age
        if ni_number is not UNSET:
            field_dict["niNumber"] = ni_number
        if passport_number is not UNSET:
            field_dict["passportNumber"] = passport_number
        if partner_details is not UNSET:
            field_dict["partnerDetails"] = partner_details

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        marital_status = MaritalStatus(d.pop("maritalStatus"))

        date_of_birth = isoparse(d.pop("dateOfBirth")).date()

        gender = Gender(d.pop("gender"))

        _address = d.pop("address", UNSET)
        address: Union[Unset, Address]
        if isinstance(_address, Unset):
            address = UNSET
        else:
            address = Address.from_dict(_address)

        title = d.pop("title", UNSET)

        first_name = d.pop("firstName", UNSET)

        middle_name = d.pop("middleName", UNSET)

        last_name = d.pop("lastName", UNSET)

        email = d.pop("email", UNSET)

        email_payslip = d.pop("emailPayslip", UNSET)

        password_protect_payslip = d.pop("passwordProtectPayslip", UNSET)

        pdf_password = d.pop("pdfPassword", UNSET)

        _pdf_password_type = d.pop("pdfPasswordType", UNSET)
        pdf_password_type: Union[Unset, PdfPasswordType]
        if isinstance(_pdf_password_type, Unset):
            pdf_password_type = UNSET
        else:
            pdf_password_type = PdfPasswordType(_pdf_password_type)

        email_statement = d.pop("emailStatement", UNSET)

        photo_url = d.pop("photoUrl", UNSET)

        telephone = d.pop("telephone", UNSET)

        mobile = d.pop("mobile", UNSET)

        state_pension_age = d.pop("statePensionAge", UNSET)

        ni_number = d.pop("niNumber", UNSET)

        passport_number = d.pop("passportNumber", UNSET)

        _partner_details = d.pop("partnerDetails", UNSET)
        partner_details: Union[Unset, PartnerDetails]
        if isinstance(_partner_details, Unset):
            partner_details = UNSET
        else:
            partner_details = PartnerDetails.from_dict(_partner_details)

        personal_details = cls(
            marital_status=marital_status,
            date_of_birth=date_of_birth,
            gender=gender,
            address=address,
            title=title,
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,
            email=email,
            email_payslip=email_payslip,
            password_protect_payslip=password_protect_payslip,
            pdf_password=pdf_password,
            pdf_password_type=pdf_password_type,
            email_statement=email_statement,
            photo_url=photo_url,
            telephone=telephone,
            mobile=mobile,
            state_pension_age=state_pension_age,
            ni_number=ni_number,
            passport_number=passport_number,
            partner_details=partner_details,
        )

        return personal_details
