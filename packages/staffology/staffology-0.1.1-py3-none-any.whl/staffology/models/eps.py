from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..models.emp_refs import EmpRefs
from ..models.eps_account import EpsAccount
from ..models.eps_apprenticeship_levy import EpsApprenticeshipLevy
from ..models.eps_de_minimis_state_aid import EpsDeMinimisStateAid
from ..models.eps_final_submission import EpsFinalSubmission
from ..models.from_to_dates import FromToDates
from ..models.gov_talk_submission import GovTalkSubmission
from ..models.recoverable_amounts import RecoverableAmounts
from ..models.tax_year import TaxYear
from ..types import UNSET, Unset

T = TypeVar("T", bound="Eps")


@attr.s(auto_attribs=True)
class Eps:
    """
    Attributes:
        period_of_inactivity (Union[Unset, FromToDates]):
        no_payment_for_period (Union[Unset, FromToDates]):
        final_submission (Union[Unset, EpsFinalSubmission]): Used on an EPS to declare a Final Submission
        recoverable_amounts (Union[Unset, RecoverableAmounts]):
        apprenticeship_levy (Union[Unset, EpsApprenticeshipLevy]): Used on an EPS to declare an Apprenticeship Levy
            amount
        account (Union[Unset, EpsAccount]): Used on an EPS to send bank account information
        eligible_for_employment_allowance (Union[Unset, None, bool]):
        de_minimis_state_aid (Union[Unset, EpsDeMinimisStateAid]): Used on an EPS to declare an Employment Allowance
            DeMinimis State Aid information
        i_rmark (Union[Unset, None, str]):
        xml (Union[Unset, None, str]):
        tax_year (Union[Unset, TaxYear]):
        employer_references (Union[Unset, EmpRefs]):
        gov_talk_submission (Union[Unset, GovTalkSubmission]):
        id (Union[Unset, str]): [readonly] The unique id of the object
    """

    period_of_inactivity: Union[Unset, FromToDates] = UNSET
    no_payment_for_period: Union[Unset, FromToDates] = UNSET
    final_submission: Union[Unset, EpsFinalSubmission] = UNSET
    recoverable_amounts: Union[Unset, RecoverableAmounts] = UNSET
    apprenticeship_levy: Union[Unset, EpsApprenticeshipLevy] = UNSET
    account: Union[Unset, EpsAccount] = UNSET
    eligible_for_employment_allowance: Union[Unset, None, bool] = UNSET
    de_minimis_state_aid: Union[Unset, EpsDeMinimisStateAid] = UNSET
    i_rmark: Union[Unset, None, str] = UNSET
    xml: Union[Unset, None, str] = UNSET
    tax_year: Union[Unset, TaxYear] = UNSET
    employer_references: Union[Unset, EmpRefs] = UNSET
    gov_talk_submission: Union[Unset, GovTalkSubmission] = UNSET
    id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        period_of_inactivity: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.period_of_inactivity, Unset):
            period_of_inactivity = self.period_of_inactivity.to_dict()

        no_payment_for_period: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.no_payment_for_period, Unset):
            no_payment_for_period = self.no_payment_for_period.to_dict()

        final_submission: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.final_submission, Unset):
            final_submission = self.final_submission.to_dict()

        recoverable_amounts: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.recoverable_amounts, Unset):
            recoverable_amounts = self.recoverable_amounts.to_dict()

        apprenticeship_levy: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.apprenticeship_levy, Unset):
            apprenticeship_levy = self.apprenticeship_levy.to_dict()

        account: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.account, Unset):
            account = self.account.to_dict()

        eligible_for_employment_allowance = self.eligible_for_employment_allowance
        de_minimis_state_aid: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.de_minimis_state_aid, Unset):
            de_minimis_state_aid = self.de_minimis_state_aid.to_dict()

        i_rmark = self.i_rmark
        xml = self.xml
        tax_year: Union[Unset, str] = UNSET
        if not isinstance(self.tax_year, Unset):
            tax_year = self.tax_year.value

        employer_references: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.employer_references, Unset):
            employer_references = self.employer_references.to_dict()

        gov_talk_submission: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.gov_talk_submission, Unset):
            gov_talk_submission = self.gov_talk_submission.to_dict()

        id = self.id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if period_of_inactivity is not UNSET:
            field_dict["periodOfInactivity"] = period_of_inactivity
        if no_payment_for_period is not UNSET:
            field_dict["noPaymentForPeriod"] = no_payment_for_period
        if final_submission is not UNSET:
            field_dict["finalSubmission"] = final_submission
        if recoverable_amounts is not UNSET:
            field_dict["recoverableAmounts"] = recoverable_amounts
        if apprenticeship_levy is not UNSET:
            field_dict["apprenticeshipLevy"] = apprenticeship_levy
        if account is not UNSET:
            field_dict["account"] = account
        if eligible_for_employment_allowance is not UNSET:
            field_dict[
                "eligibleForEmploymentAllowance"
            ] = eligible_for_employment_allowance
        if de_minimis_state_aid is not UNSET:
            field_dict["deMinimisStateAid"] = de_minimis_state_aid
        if i_rmark is not UNSET:
            field_dict["iRmark"] = i_rmark
        if xml is not UNSET:
            field_dict["xml"] = xml
        if tax_year is not UNSET:
            field_dict["taxYear"] = tax_year
        if employer_references is not UNSET:
            field_dict["employerReferences"] = employer_references
        if gov_talk_submission is not UNSET:
            field_dict["govTalkSubmission"] = gov_talk_submission
        if id is not UNSET:
            field_dict["id"] = id

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _period_of_inactivity = d.pop("periodOfInactivity", UNSET)
        period_of_inactivity: Union[Unset, FromToDates]
        if isinstance(_period_of_inactivity, Unset):
            period_of_inactivity = UNSET
        else:
            period_of_inactivity = FromToDates.from_dict(_period_of_inactivity)

        _no_payment_for_period = d.pop("noPaymentForPeriod", UNSET)
        no_payment_for_period: Union[Unset, FromToDates]
        if isinstance(_no_payment_for_period, Unset):
            no_payment_for_period = UNSET
        else:
            no_payment_for_period = FromToDates.from_dict(_no_payment_for_period)

        _final_submission = d.pop("finalSubmission", UNSET)
        final_submission: Union[Unset, EpsFinalSubmission]
        if isinstance(_final_submission, Unset):
            final_submission = UNSET
        else:
            final_submission = EpsFinalSubmission.from_dict(_final_submission)

        _recoverable_amounts = d.pop("recoverableAmounts", UNSET)
        recoverable_amounts: Union[Unset, RecoverableAmounts]
        if isinstance(_recoverable_amounts, Unset):
            recoverable_amounts = UNSET
        else:
            recoverable_amounts = RecoverableAmounts.from_dict(_recoverable_amounts)

        _apprenticeship_levy = d.pop("apprenticeshipLevy", UNSET)
        apprenticeship_levy: Union[Unset, EpsApprenticeshipLevy]
        if isinstance(_apprenticeship_levy, Unset):
            apprenticeship_levy = UNSET
        else:
            apprenticeship_levy = EpsApprenticeshipLevy.from_dict(_apprenticeship_levy)

        _account = d.pop("account", UNSET)
        account: Union[Unset, EpsAccount]
        if isinstance(_account, Unset):
            account = UNSET
        else:
            account = EpsAccount.from_dict(_account)

        eligible_for_employment_allowance = d.pop(
            "eligibleForEmploymentAllowance", UNSET
        )

        _de_minimis_state_aid = d.pop("deMinimisStateAid", UNSET)
        de_minimis_state_aid: Union[Unset, EpsDeMinimisStateAid]
        if isinstance(_de_minimis_state_aid, Unset):
            de_minimis_state_aid = UNSET
        else:
            de_minimis_state_aid = EpsDeMinimisStateAid.from_dict(_de_minimis_state_aid)

        i_rmark = d.pop("iRmark", UNSET)

        xml = d.pop("xml", UNSET)

        _tax_year = d.pop("taxYear", UNSET)
        tax_year: Union[Unset, TaxYear]
        if isinstance(_tax_year, Unset):
            tax_year = UNSET
        else:
            tax_year = TaxYear(_tax_year)

        _employer_references = d.pop("employerReferences", UNSET)
        employer_references: Union[Unset, EmpRefs]
        if isinstance(_employer_references, Unset):
            employer_references = UNSET
        else:
            employer_references = EmpRefs.from_dict(_employer_references)

        _gov_talk_submission = d.pop("govTalkSubmission", UNSET)
        gov_talk_submission: Union[Unset, GovTalkSubmission]
        if isinstance(_gov_talk_submission, Unset):
            gov_talk_submission = UNSET
        else:
            gov_talk_submission = GovTalkSubmission.from_dict(_gov_talk_submission)

        id = d.pop("id", UNSET)

        eps = cls(
            period_of_inactivity=period_of_inactivity,
            no_payment_for_period=no_payment_for_period,
            final_submission=final_submission,
            recoverable_amounts=recoverable_amounts,
            apprenticeship_levy=apprenticeship_levy,
            account=account,
            eligible_for_employment_allowance=eligible_for_employment_allowance,
            de_minimis_state_aid=de_minimis_state_aid,
            i_rmark=i_rmark,
            xml=xml,
            tax_year=tax_year,
            employer_references=employer_references,
            gov_talk_submission=gov_talk_submission,
            id=id,
        )

        return eps
