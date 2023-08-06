import datetime
from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bank_payment_instruction import BankPaymentInstruction
from ...models.external_data_provider_id import ExternalDataProviderId
from ...models.pay_periods import PayPeriods
from ...models.tax_year import TaxYear
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    id: ExternalDataProviderId,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    inc_employees: Union[Unset, None, bool] = UNSET,
    inc_hmrc: Union[Unset, None, bool] = UNSET,
    inc_pensions: Union[Unset, None, bool] = UNSET,
    inc_aeos: Union[Unset, None, bool] = UNSET,
    inc_deductions: Union[Unset, None, bool] = UNSET,
    force: Union[Unset, None, bool] = UNSET,
    ordinal: Union[Unset, None, int] = 1,
    payment_date: Union[Unset, None, datetime.datetime] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/external-data/{id}/{taxYear}/{payPeriod}/{periodNumber}/payments".format(
        client.base_url,
        employerId=employer_id,
        id=id,
        taxYear=tax_year,
        payPeriod=pay_period,
        periodNumber=period_number,
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["incEmployees"] = inc_employees

    params["incHmrc"] = inc_hmrc

    params["incPensions"] = inc_pensions

    params["incAeos"] = inc_aeos

    params["incDeductions"] = inc_deductions

    params["force"] = force

    params["ordinal"] = ordinal

    json_payment_date: Union[Unset, None, str] = UNSET
    if not isinstance(payment_date, Unset):
        json_payment_date = payment_date.isoformat() if payment_date else None

    params["paymentDate"] = json_payment_date

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[BankPaymentInstruction]:
    if response.status_code == 200:
        response_200 = BankPaymentInstruction.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[BankPaymentInstruction]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    id: ExternalDataProviderId,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    inc_employees: Union[Unset, None, bool] = UNSET,
    inc_hmrc: Union[Unset, None, bool] = UNSET,
    inc_pensions: Union[Unset, None, bool] = UNSET,
    inc_aeos: Union[Unset, None, bool] = UNSET,
    inc_deductions: Union[Unset, None, bool] = UNSET,
    force: Union[Unset, None, bool] = UNSET,
    ordinal: Union[Unset, None, int] = 1,
    payment_date: Union[Unset, None, datetime.datetime] = UNSET,
) -> Response[BankPaymentInstruction]:
    """Post Payments

     Post Payments for a payrun to the ExternalDataProvider
    A 200 response does not mean the payments were necessarily successfully posted.
    The BankPaymentInstruction is returned (without the payments) so that you can inspect the status to
    determine success

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        inc_employees (Union[Unset, None, bool]):
        inc_hmrc (Union[Unset, None, bool]):
        inc_pensions (Union[Unset, None, bool]):
        inc_aeos (Union[Unset, None, bool]):
        inc_deductions (Union[Unset, None, bool]):
        force (Union[Unset, None, bool]):
        ordinal (Union[Unset, None, int]):  Default: 1.
        payment_date (Union[Unset, None, datetime.datetime]):

    Returns:
        Response[BankPaymentInstruction]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        client=client,
        inc_employees=inc_employees,
        inc_hmrc=inc_hmrc,
        inc_pensions=inc_pensions,
        inc_aeos=inc_aeos,
        inc_deductions=inc_deductions,
        force=force,
        ordinal=ordinal,
        payment_date=payment_date,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    employer_id: str,
    id: ExternalDataProviderId,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    inc_employees: Union[Unset, None, bool] = UNSET,
    inc_hmrc: Union[Unset, None, bool] = UNSET,
    inc_pensions: Union[Unset, None, bool] = UNSET,
    inc_aeos: Union[Unset, None, bool] = UNSET,
    inc_deductions: Union[Unset, None, bool] = UNSET,
    force: Union[Unset, None, bool] = UNSET,
    ordinal: Union[Unset, None, int] = 1,
    payment_date: Union[Unset, None, datetime.datetime] = UNSET,
) -> Optional[BankPaymentInstruction]:
    """Post Payments

     Post Payments for a payrun to the ExternalDataProvider
    A 200 response does not mean the payments were necessarily successfully posted.
    The BankPaymentInstruction is returned (without the payments) so that you can inspect the status to
    determine success

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        inc_employees (Union[Unset, None, bool]):
        inc_hmrc (Union[Unset, None, bool]):
        inc_pensions (Union[Unset, None, bool]):
        inc_aeos (Union[Unset, None, bool]):
        inc_deductions (Union[Unset, None, bool]):
        force (Union[Unset, None, bool]):
        ordinal (Union[Unset, None, int]):  Default: 1.
        payment_date (Union[Unset, None, datetime.datetime]):

    Returns:
        Response[BankPaymentInstruction]
    """

    return sync_detailed(
        employer_id=employer_id,
        id=id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        client=client,
        inc_employees=inc_employees,
        inc_hmrc=inc_hmrc,
        inc_pensions=inc_pensions,
        inc_aeos=inc_aeos,
        inc_deductions=inc_deductions,
        force=force,
        ordinal=ordinal,
        payment_date=payment_date,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    id: ExternalDataProviderId,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    inc_employees: Union[Unset, None, bool] = UNSET,
    inc_hmrc: Union[Unset, None, bool] = UNSET,
    inc_pensions: Union[Unset, None, bool] = UNSET,
    inc_aeos: Union[Unset, None, bool] = UNSET,
    inc_deductions: Union[Unset, None, bool] = UNSET,
    force: Union[Unset, None, bool] = UNSET,
    ordinal: Union[Unset, None, int] = 1,
    payment_date: Union[Unset, None, datetime.datetime] = UNSET,
) -> Response[BankPaymentInstruction]:
    """Post Payments

     Post Payments for a payrun to the ExternalDataProvider
    A 200 response does not mean the payments were necessarily successfully posted.
    The BankPaymentInstruction is returned (without the payments) so that you can inspect the status to
    determine success

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        inc_employees (Union[Unset, None, bool]):
        inc_hmrc (Union[Unset, None, bool]):
        inc_pensions (Union[Unset, None, bool]):
        inc_aeos (Union[Unset, None, bool]):
        inc_deductions (Union[Unset, None, bool]):
        force (Union[Unset, None, bool]):
        ordinal (Union[Unset, None, int]):  Default: 1.
        payment_date (Union[Unset, None, datetime.datetime]):

    Returns:
        Response[BankPaymentInstruction]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        client=client,
        inc_employees=inc_employees,
        inc_hmrc=inc_hmrc,
        inc_pensions=inc_pensions,
        inc_aeos=inc_aeos,
        inc_deductions=inc_deductions,
        force=force,
        ordinal=ordinal,
        payment_date=payment_date,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    id: ExternalDataProviderId,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    inc_employees: Union[Unset, None, bool] = UNSET,
    inc_hmrc: Union[Unset, None, bool] = UNSET,
    inc_pensions: Union[Unset, None, bool] = UNSET,
    inc_aeos: Union[Unset, None, bool] = UNSET,
    inc_deductions: Union[Unset, None, bool] = UNSET,
    force: Union[Unset, None, bool] = UNSET,
    ordinal: Union[Unset, None, int] = 1,
    payment_date: Union[Unset, None, datetime.datetime] = UNSET,
) -> Optional[BankPaymentInstruction]:
    """Post Payments

     Post Payments for a payrun to the ExternalDataProvider
    A 200 response does not mean the payments were necessarily successfully posted.
    The BankPaymentInstruction is returned (without the payments) so that you can inspect the status to
    determine success

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        inc_employees (Union[Unset, None, bool]):
        inc_hmrc (Union[Unset, None, bool]):
        inc_pensions (Union[Unset, None, bool]):
        inc_aeos (Union[Unset, None, bool]):
        inc_deductions (Union[Unset, None, bool]):
        force (Union[Unset, None, bool]):
        ordinal (Union[Unset, None, int]):  Default: 1.
        payment_date (Union[Unset, None, datetime.datetime]):

    Returns:
        Response[BankPaymentInstruction]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            id=id,
            tax_year=tax_year,
            pay_period=pay_period,
            period_number=period_number,
            client=client,
            inc_employees=inc_employees,
            inc_hmrc=inc_hmrc,
            inc_pensions=inc_pensions,
            inc_aeos=inc_aeos,
            inc_deductions=inc_deductions,
            force=force,
            ordinal=ordinal,
            payment_date=payment_date,
        )
    ).parsed
