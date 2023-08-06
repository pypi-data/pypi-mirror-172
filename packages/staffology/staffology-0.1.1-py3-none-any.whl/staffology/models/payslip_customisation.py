from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.pdf_paper_margins import PdfPaperMargins
from ..models.pdf_paper_orientation import PdfPaperOrientation
from ..models.pdf_paper_size import PdfPaperSize
from ..models.report_custom_css_option import ReportCustomCssOption
from ..types import UNSET, Unset

T = TypeVar("T", bound="PayslipCustomisation")


@attr.s(auto_attribs=True)
class PayslipCustomisation:
    """Used to represent any customisations you make to the look of Payslip PDFs.
    This is covered in detail in the Guides section.

        Attributes:
            custom (Union[Unset, bool]): Whether or not you are customising the Payslip.
                This should always be true if you are providing any other values.
            include_logo (Union[Unset, bool]): Whether or not to include the employer logo on the payslip.
            custom_css_option (Union[Unset, ReportCustomCssOption]):
            custom_css (Union[Unset, None, str]):
            remove_ytd (Union[Unset, bool]): Whether or not to remove the YTD column
            include_employer_address (Union[Unset, bool]): Whether or not to include the employer address
            use_umbrella_format (Union[Unset, bool]): If true then the format the payslip will include details of the
                Umbrella Payment as well as employer costs
            filename (Union[Unset, None, str]):
            include_department (Union[Unset, bool]): Whether or not to include the primary department of the employee on the
                payslip
            include_health_and_social_care_message (Union[Unset, bool]): Whether or not to include health and social car
                message
            include_benefits (Union[Unset, bool]): Whether or not to include any payrolled benefits
            paper_size (Union[Unset, PdfPaperSize]):
            orientation (Union[Unset, PdfPaperOrientation]):
            margins (Union[Unset, PdfPaperMargins]):
            id (Union[Unset, str]): [readonly] The unique id of the object
    """

    custom: Union[Unset, bool] = UNSET
    include_logo: Union[Unset, bool] = UNSET
    custom_css_option: Union[Unset, ReportCustomCssOption] = UNSET
    custom_css: Union[Unset, None, str] = UNSET
    remove_ytd: Union[Unset, bool] = UNSET
    include_employer_address: Union[Unset, bool] = UNSET
    use_umbrella_format: Union[Unset, bool] = UNSET
    filename: Union[Unset, None, str] = UNSET
    include_department: Union[Unset, bool] = UNSET
    include_health_and_social_care_message: Union[Unset, bool] = UNSET
    include_benefits: Union[Unset, bool] = UNSET
    paper_size: Union[Unset, PdfPaperSize] = UNSET
    orientation: Union[Unset, PdfPaperOrientation] = UNSET
    margins: Union[Unset, PdfPaperMargins] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        custom = self.custom
        include_logo = self.include_logo
        custom_css_option: Union[Unset, str] = UNSET
        if not isinstance(self.custom_css_option, Unset):
            custom_css_option = self.custom_css_option.value

        custom_css = self.custom_css
        remove_ytd = self.remove_ytd
        include_employer_address = self.include_employer_address
        use_umbrella_format = self.use_umbrella_format
        filename = self.filename
        include_department = self.include_department
        include_health_and_social_care_message = (
            self.include_health_and_social_care_message
        )
        include_benefits = self.include_benefits
        paper_size: Union[Unset, str] = UNSET
        if not isinstance(self.paper_size, Unset):
            paper_size = self.paper_size.value

        orientation: Union[Unset, str] = UNSET
        if not isinstance(self.orientation, Unset):
            orientation = self.orientation.value

        margins: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.margins, Unset):
            margins = self.margins.to_dict()

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if custom is not UNSET:
            field_dict["custom"] = custom
        if include_logo is not UNSET:
            field_dict["includeLogo"] = include_logo
        if custom_css_option is not UNSET:
            field_dict["customCssOption"] = custom_css_option
        if custom_css is not UNSET:
            field_dict["customCss"] = custom_css
        if remove_ytd is not UNSET:
            field_dict["removeYtd"] = remove_ytd
        if include_employer_address is not UNSET:
            field_dict["includeEmployerAddress"] = include_employer_address
        if use_umbrella_format is not UNSET:
            field_dict["useUmbrellaFormat"] = use_umbrella_format
        if filename is not UNSET:
            field_dict["filename"] = filename
        if include_department is not UNSET:
            field_dict["includeDepartment"] = include_department
        if include_health_and_social_care_message is not UNSET:
            field_dict[
                "includeHealthAndSocialCareMessage"
            ] = include_health_and_social_care_message
        if include_benefits is not UNSET:
            field_dict["includeBenefits"] = include_benefits
        if paper_size is not UNSET:
            field_dict["paperSize"] = paper_size
        if orientation is not UNSET:
            field_dict["orientation"] = orientation
        if margins is not UNSET:
            field_dict["margins"] = margins
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        custom = d.pop("custom", UNSET)

        include_logo = d.pop("includeLogo", UNSET)

        _custom_css_option = d.pop("customCssOption", UNSET)
        custom_css_option: Union[Unset, ReportCustomCssOption]
        if isinstance(_custom_css_option, Unset):
            custom_css_option = UNSET
        else:
            custom_css_option = ReportCustomCssOption(_custom_css_option)

        custom_css = d.pop("customCss", UNSET)

        remove_ytd = d.pop("removeYtd", UNSET)

        include_employer_address = d.pop("includeEmployerAddress", UNSET)

        use_umbrella_format = d.pop("useUmbrellaFormat", UNSET)

        filename = d.pop("filename", UNSET)

        include_department = d.pop("includeDepartment", UNSET)

        include_health_and_social_care_message = d.pop(
            "includeHealthAndSocialCareMessage", UNSET
        )

        include_benefits = d.pop("includeBenefits", UNSET)

        _paper_size = d.pop("paperSize", UNSET)
        paper_size: Union[Unset, PdfPaperSize]
        if isinstance(_paper_size, Unset):
            paper_size = UNSET
        else:
            paper_size = PdfPaperSize(_paper_size)

        _orientation = d.pop("orientation", UNSET)
        orientation: Union[Unset, PdfPaperOrientation]
        if isinstance(_orientation, Unset):
            orientation = UNSET
        else:
            orientation = PdfPaperOrientation(_orientation)

        _margins = d.pop("margins", UNSET)
        margins: Union[Unset, PdfPaperMargins]
        if isinstance(_margins, Unset):
            margins = UNSET
        else:
            margins = PdfPaperMargins.from_dict(_margins)

        id = d.pop("id", UNSET)

        payslip_customisation = cls(
            custom=custom,
            include_logo=include_logo,
            custom_css_option=custom_css_option,
            custom_css=custom_css,
            remove_ytd=remove_ytd,
            include_employer_address=include_employer_address,
            use_umbrella_format=use_umbrella_format,
            filename=filename,
            include_department=include_department,
            include_health_and_social_care_message=include_health_and_social_care_message,
            include_benefits=include_benefits,
            paper_size=paper_size,
            orientation=orientation,
            margins=margins,
            id=id,
        )

        return payslip_customisation
