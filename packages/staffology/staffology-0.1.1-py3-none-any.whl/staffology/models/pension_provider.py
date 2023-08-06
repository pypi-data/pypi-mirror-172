from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.address import Address
from ..models.papdis_version import PapdisVersion
from ..models.pension_csv_format import PensionCsvFormat
from ..types import UNSET, Unset

T = TypeVar("T", bound="PensionProvider")


@attr.s(auto_attribs=True)
class PensionProvider:
    """
    Attributes:
        name (str):
        account_no (Union[Unset, None, str]):
        portal (Union[Unset, None, str]):
        website (Union[Unset, None, str]):
        address (Union[Unset, Address]):
        telephone (Union[Unset, None, str]):
        papdis_version (Union[Unset, PapdisVersion]):
        papdis_provider_id (Union[Unset, None, str]):
        papdis_employer_id (Union[Unset, None, str]):
        csv_format (Union[Unset, PensionCsvFormat]):
        exclude_nil_paid_from_contributions (Union[Unset, bool]): If we're sending contributions to an external provider
            then we'll include all employees that were on the payrun.
            If you want to exclude employees that don't have any contributions to report then set this to true.
        pay_period_date_adjustment (Union[Unset, int]): If you need to adjust the reported dates of the contributions
            then you can do so by setting a non-zero value here.
            A negative value of will move the date back in time.
        misc_boolean_1 (Union[Unset, bool]): This field has different uses dependent on the ExternalDataProvider, if
            any.
            For Nest, it indicates whether or not contributions are reported as "Tax Weekly/Monthly" rather than just
            "Weekly/Monthly"
        misc_boolean_2 (Union[Unset, bool]): This field has different uses dependent on the ExternalDataProvider, if
            any.
            For Nest, it indicates whether or not to approve payments after submitting contributions
        misc_string_1 (Union[Unset, None, str]): This field has different uses dependent on the ExternalDataProvider, if
            any.
            For Nest, it dictates the PaymentSource.
        misc_string_2 (Union[Unset, None, str]): This field has different uses dependent on the ExternalDataProvider, if
            any.
        opt_out_window (Union[Unset, int]): The number of days or months that an employee has to Opt out after being
            enrolled
        opt_out_window_is_months (Union[Unset, bool]): Determines whether the value given for OptOutWindow is in Months
            (true) or days (false)
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    name: str
    account_no: Union[Unset, None, str] = UNSET
    portal: Union[Unset, None, str] = UNSET
    website: Union[Unset, None, str] = UNSET
    address: Union[Unset, Address] = UNSET
    telephone: Union[Unset, None, str] = UNSET
    papdis_version: Union[Unset, PapdisVersion] = UNSET
    papdis_provider_id: Union[Unset, None, str] = UNSET
    papdis_employer_id: Union[Unset, None, str] = UNSET
    csv_format: Union[Unset, PensionCsvFormat] = UNSET
    exclude_nil_paid_from_contributions: Union[Unset, bool] = UNSET
    pay_period_date_adjustment: Union[Unset, int] = UNSET
    misc_boolean_1: Union[Unset, bool] = UNSET
    misc_boolean_2: Union[Unset, bool] = UNSET
    misc_string_1: Union[Unset, None, str] = UNSET
    misc_string_2: Union[Unset, None, str] = UNSET
    opt_out_window: Union[Unset, int] = UNSET
    opt_out_window_is_months: Union[Unset, bool] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        name = self.name
        account_no = self.account_no
        portal = self.portal
        website = self.website
        address: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.address, Unset):
            address = self.address.to_dict()

        telephone = self.telephone
        papdis_version: Union[Unset, str] = UNSET
        if not isinstance(self.papdis_version, Unset):
            papdis_version = self.papdis_version.value

        papdis_provider_id = self.papdis_provider_id
        papdis_employer_id = self.papdis_employer_id
        csv_format: Union[Unset, str] = UNSET
        if not isinstance(self.csv_format, Unset):
            csv_format = self.csv_format.value

        exclude_nil_paid_from_contributions = self.exclude_nil_paid_from_contributions
        pay_period_date_adjustment = self.pay_period_date_adjustment
        misc_boolean_1 = self.misc_boolean_1
        misc_boolean_2 = self.misc_boolean_2
        misc_string_1 = self.misc_string_1
        misc_string_2 = self.misc_string_2
        opt_out_window = self.opt_out_window
        opt_out_window_is_months = self.opt_out_window_is_months
        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "name": name,
            }
        )
        if account_no is not UNSET:
            field_dict["accountNo"] = account_no
        if portal is not UNSET:
            field_dict["portal"] = portal
        if website is not UNSET:
            field_dict["website"] = website
        if address is not UNSET:
            field_dict["address"] = address
        if telephone is not UNSET:
            field_dict["telephone"] = telephone
        if papdis_version is not UNSET:
            field_dict["papdisVersion"] = papdis_version
        if papdis_provider_id is not UNSET:
            field_dict["papdisProviderId"] = papdis_provider_id
        if papdis_employer_id is not UNSET:
            field_dict["papdisEmployerId"] = papdis_employer_id
        if csv_format is not UNSET:
            field_dict["csvFormat"] = csv_format
        if exclude_nil_paid_from_contributions is not UNSET:
            field_dict[
                "excludeNilPaidFromContributions"
            ] = exclude_nil_paid_from_contributions
        if pay_period_date_adjustment is not UNSET:
            field_dict["payPeriodDateAdjustment"] = pay_period_date_adjustment
        if misc_boolean_1 is not UNSET:
            field_dict["miscBoolean1"] = misc_boolean_1
        if misc_boolean_2 is not UNSET:
            field_dict["miscBoolean2"] = misc_boolean_2
        if misc_string_1 is not UNSET:
            field_dict["miscString1"] = misc_string_1
        if misc_string_2 is not UNSET:
            field_dict["miscString2"] = misc_string_2
        if opt_out_window is not UNSET:
            field_dict["optOutWindow"] = opt_out_window
        if opt_out_window_is_months is not UNSET:
            field_dict["optOutWindowIsMonths"] = opt_out_window_is_months
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        name = d.pop("name")

        account_no = d.pop("accountNo", UNSET)

        portal = d.pop("portal", UNSET)

        website = d.pop("website", UNSET)

        _address = d.pop("address", UNSET)
        address: Union[Unset, Address]
        if isinstance(_address, Unset):
            address = UNSET
        else:
            address = Address.from_dict(_address)

        telephone = d.pop("telephone", UNSET)

        _papdis_version = d.pop("papdisVersion", UNSET)
        papdis_version: Union[Unset, PapdisVersion]
        if isinstance(_papdis_version, Unset):
            papdis_version = UNSET
        else:
            papdis_version = PapdisVersion(_papdis_version)

        papdis_provider_id = d.pop("papdisProviderId", UNSET)

        papdis_employer_id = d.pop("papdisEmployerId", UNSET)

        _csv_format = d.pop("csvFormat", UNSET)
        csv_format: Union[Unset, PensionCsvFormat]
        if isinstance(_csv_format, Unset):
            csv_format = UNSET
        else:
            csv_format = PensionCsvFormat(_csv_format)

        exclude_nil_paid_from_contributions = d.pop(
            "excludeNilPaidFromContributions", UNSET
        )

        pay_period_date_adjustment = d.pop("payPeriodDateAdjustment", UNSET)

        misc_boolean_1 = d.pop("miscBoolean1", UNSET)

        misc_boolean_2 = d.pop("miscBoolean2", UNSET)

        misc_string_1 = d.pop("miscString1", UNSET)

        misc_string_2 = d.pop("miscString2", UNSET)

        opt_out_window = d.pop("optOutWindow", UNSET)

        opt_out_window_is_months = d.pop("optOutWindowIsMonths", UNSET)

        id = d.pop("id", UNSET)

        pension_provider = cls(
            name=name,
            account_no=account_no,
            portal=portal,
            website=website,
            address=address,
            telephone=telephone,
            papdis_version=papdis_version,
            papdis_provider_id=papdis_provider_id,
            papdis_employer_id=papdis_employer_id,
            csv_format=csv_format,
            exclude_nil_paid_from_contributions=exclude_nil_paid_from_contributions,
            pay_period_date_adjustment=pay_period_date_adjustment,
            misc_boolean_1=misc_boolean_1,
            misc_boolean_2=misc_boolean_2,
            misc_string_1=misc_string_1,
            misc_string_2=misc_string_2,
            opt_out_window=opt_out_window,
            opt_out_window_is_months=opt_out_window_is_months,
            id=id,
        )

        return pension_provider
