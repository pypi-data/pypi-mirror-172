from typing import Any, Dict, Type, TypeVar, Union

import attr

from ..types import UNSET, Unset

T = TypeVar("T", bound="EmployerOpeningBalances")


@attr.s(auto_attribs=True)
class EmployerOpeningBalances:
    """
    Attributes:
        smp_recovered (Union[Unset, float]): Value of Statutory Maternity Pay recovered year to date
        spp_recovered (Union[Unset, float]): Value of Statutory Paternity Pay recovered year to date
        sap_recovered (Union[Unset, float]): Value of Statutory Adoption Pay recovered year to date
        sh_pp_recovered (Union[Unset, float]): Value of Shared Parental Pay recovered year to date
        spbp_recovered (Union[Unset, float]): Value of Statutory Parental Bereavment Pay recovered year to date
        nic_compensation_on_smp (Union[Unset, float]): Value of NIC compensation on SMP year to date
        nic_compensation_on_spp (Union[Unset, float]): Value of NIC compensation on Statutory Paternity Pay year to date
        nic_compensation_on_sap (Union[Unset, float]): Value of NIC compensation on Statutory Adoption Pay year to date
        nic_compensation_on_sh_pp (Union[Unset, float]): Value of NIC compensation on Shared Parental Pay year to date
        nic_compensation_on_spbp (Union[Unset, float]): Value of NIC compensation on Statutory Parental Bereavement Pay
            year to date
        cis_deductions_suffered (Union[Unset, float]): Value of CIS deductions suffered year to date
        apprenticeship_levy (Union[Unset, float]): Value of Apprenticeship levy paid year to date
    """

    smp_recovered: Union[Unset, float] = UNSET
    spp_recovered: Union[Unset, float] = UNSET
    sap_recovered: Union[Unset, float] = UNSET
    sh_pp_recovered: Union[Unset, float] = UNSET
    spbp_recovered: Union[Unset, float] = UNSET
    nic_compensation_on_smp: Union[Unset, float] = UNSET
    nic_compensation_on_spp: Union[Unset, float] = UNSET
    nic_compensation_on_sap: Union[Unset, float] = UNSET
    nic_compensation_on_sh_pp: Union[Unset, float] = UNSET
    nic_compensation_on_spbp: Union[Unset, float] = UNSET
    cis_deductions_suffered: Union[Unset, float] = UNSET
    apprenticeship_levy: Union[Unset, float] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        smp_recovered = self.smp_recovered
        spp_recovered = self.spp_recovered
        sap_recovered = self.sap_recovered
        sh_pp_recovered = self.sh_pp_recovered
        spbp_recovered = self.spbp_recovered
        nic_compensation_on_smp = self.nic_compensation_on_smp
        nic_compensation_on_spp = self.nic_compensation_on_spp
        nic_compensation_on_sap = self.nic_compensation_on_sap
        nic_compensation_on_sh_pp = self.nic_compensation_on_sh_pp
        nic_compensation_on_spbp = self.nic_compensation_on_spbp
        cis_deductions_suffered = self.cis_deductions_suffered
        apprenticeship_levy = self.apprenticeship_levy

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if smp_recovered is not UNSET:
            field_dict["smpRecovered"] = smp_recovered
        if spp_recovered is not UNSET:
            field_dict["sppRecovered"] = spp_recovered
        if sap_recovered is not UNSET:
            field_dict["sapRecovered"] = sap_recovered
        if sh_pp_recovered is not UNSET:
            field_dict["shPPRecovered"] = sh_pp_recovered
        if spbp_recovered is not UNSET:
            field_dict["spbpRecovered"] = spbp_recovered
        if nic_compensation_on_smp is not UNSET:
            field_dict["nicCompensationOnSMP"] = nic_compensation_on_smp
        if nic_compensation_on_spp is not UNSET:
            field_dict["nicCompensationOnSPP"] = nic_compensation_on_spp
        if nic_compensation_on_sap is not UNSET:
            field_dict["nicCompensationOnSAP"] = nic_compensation_on_sap
        if nic_compensation_on_sh_pp is not UNSET:
            field_dict["nicCompensationOnShPP"] = nic_compensation_on_sh_pp
        if nic_compensation_on_spbp is not UNSET:
            field_dict["nicCompensationOnSPBP"] = nic_compensation_on_spbp
        if cis_deductions_suffered is not UNSET:
            field_dict["cisDeductionsSuffered"] = cis_deductions_suffered
        if apprenticeship_levy is not UNSET:
            field_dict["apprenticeshipLevy"] = apprenticeship_levy

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        smp_recovered = d.pop("smpRecovered", UNSET)

        spp_recovered = d.pop("sppRecovered", UNSET)

        sap_recovered = d.pop("sapRecovered", UNSET)

        sh_pp_recovered = d.pop("shPPRecovered", UNSET)

        spbp_recovered = d.pop("spbpRecovered", UNSET)

        nic_compensation_on_smp = d.pop("nicCompensationOnSMP", UNSET)

        nic_compensation_on_spp = d.pop("nicCompensationOnSPP", UNSET)

        nic_compensation_on_sap = d.pop("nicCompensationOnSAP", UNSET)

        nic_compensation_on_sh_pp = d.pop("nicCompensationOnShPP", UNSET)

        nic_compensation_on_spbp = d.pop("nicCompensationOnSPBP", UNSET)

        cis_deductions_suffered = d.pop("cisDeductionsSuffered", UNSET)

        apprenticeship_levy = d.pop("apprenticeshipLevy", UNSET)

        employer_opening_balances = cls(
            smp_recovered=smp_recovered,
            spp_recovered=spp_recovered,
            sap_recovered=sap_recovered,
            sh_pp_recovered=sh_pp_recovered,
            spbp_recovered=spbp_recovered,
            nic_compensation_on_smp=nic_compensation_on_smp,
            nic_compensation_on_spp=nic_compensation_on_spp,
            nic_compensation_on_sap=nic_compensation_on_sap,
            nic_compensation_on_sh_pp=nic_compensation_on_sh_pp,
            nic_compensation_on_spbp=nic_compensation_on_spbp,
            cis_deductions_suffered=cis_deductions_suffered,
            apprenticeship_levy=apprenticeship_levy,
        )

        return employer_opening_balances
