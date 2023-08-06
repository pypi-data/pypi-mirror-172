from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="GovTalk")


@attr.s(auto_attribs=True)
class GovTalk:
    """Part of the TaxYearConfig that our engine uses submit documents to the HMRC Gateway.
    It is used internally when our engine communicates with HMRC.
    You do not need to do anything with this model, it's provided purely for informational purposes.

        Attributes:
            full_payment_submission_namespace (Union[Unset, None, str]): [readonly]
            employer_payment_summary_namespace (Union[Unset, None, str]): [readonly]
            ni_no_verification_request_name_space (Union[Unset, None, str]): [readonly]
            cis_verification_request_name_space (Union[Unset, None, str]): [readonly]
            cis_300_name_space (Union[Unset, None, str]): [readonly]
            expenses_and_benefits_name_space (Union[Unset, None, str]): [readonly]
    """

    full_payment_submission_namespace: Union[Unset, None, str] = UNSET
    employer_payment_summary_namespace: Union[Unset, None, str] = UNSET
    ni_no_verification_request_name_space: Union[Unset, None, str] = UNSET
    cis_verification_request_name_space: Union[Unset, None, str] = UNSET
    cis_300_name_space: Union[Unset, None, str] = UNSET
    expenses_and_benefits_name_space: Union[Unset, None, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        full_payment_submission_namespace = self.full_payment_submission_namespace
        employer_payment_summary_namespace = self.employer_payment_summary_namespace
        ni_no_verification_request_name_space = (
            self.ni_no_verification_request_name_space
        )
        cis_verification_request_name_space = self.cis_verification_request_name_space
        cis_300_name_space = self.cis_300_name_space
        expenses_and_benefits_name_space = self.expenses_and_benefits_name_space

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if full_payment_submission_namespace is not UNSET:
            field_dict[
                "fullPaymentSubmissionNamespace"
            ] = full_payment_submission_namespace
        if employer_payment_summary_namespace is not UNSET:
            field_dict[
                "employerPaymentSummaryNamespace"
            ] = employer_payment_summary_namespace
        if ni_no_verification_request_name_space is not UNSET:
            field_dict[
                "niNoVerificationRequestNameSpace"
            ] = ni_no_verification_request_name_space
        if cis_verification_request_name_space is not UNSET:
            field_dict[
                "cisVerificationRequestNameSpace"
            ] = cis_verification_request_name_space
        if cis_300_name_space is not UNSET:
            field_dict["cis300NameSpace"] = cis_300_name_space
        if expenses_and_benefits_name_space is not UNSET:
            field_dict[
                "expensesAndBenefitsNameSpace"
            ] = expenses_and_benefits_name_space

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        full_payment_submission_namespace = d.pop(
            "fullPaymentSubmissionNamespace", UNSET
        )

        employer_payment_summary_namespace = d.pop(
            "employerPaymentSummaryNamespace", UNSET
        )

        ni_no_verification_request_name_space = d.pop(
            "niNoVerificationRequestNameSpace", UNSET
        )

        cis_verification_request_name_space = d.pop(
            "cisVerificationRequestNameSpace", UNSET
        )

        cis_300_name_space = d.pop("cis300NameSpace", UNSET)

        expenses_and_benefits_name_space = d.pop("expensesAndBenefitsNameSpace", UNSET)

        gov_talk = cls(
            full_payment_submission_namespace=full_payment_submission_namespace,
            employer_payment_summary_namespace=employer_payment_summary_namespace,
            ni_no_verification_request_name_space=ni_no_verification_request_name_space,
            cis_verification_request_name_space=cis_verification_request_name_space,
            cis_300_name_space=cis_300_name_space,
            expenses_and_benefits_name_space=expenses_and_benefits_name_space,
        )

        return gov_talk
