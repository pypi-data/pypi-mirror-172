import datetime
from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.bank_payment_instruction_report_response import (
    BankPaymentInstructionReportResponse,
)
from ...models.pay_periods import PayPeriods
from ...models.tax_year import TaxYear
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    payment_date: Union[Unset, None, datetime.datetime] = UNSET,
    ordinal: Union[Unset, None, int] = 1,
    inc_pensions: Union[Unset, None, bool] = False,
    inc_hmrc: Union[Unset, None, bool] = False,
    inc_aeos: Union[Unset, None, bool] = False,
    inc_deductions: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/reports/{taxYear}/{payPeriod}/{periodNumber}/payments/employee/credit".format(
        client.base_url,
        employerId=employer_id,
        taxYear=tax_year,
        payPeriod=pay_period,
        periodNumber=period_number,
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(accept, Unset):
        headers["accept"] = accept

    params: Dict[str, Any] = {}
    json_payment_date: Union[Unset, None, str] = UNSET
    if not isinstance(payment_date, Unset):
        json_payment_date = payment_date.isoformat() if payment_date else None

    params["paymentDate"] = json_payment_date

    params["ordinal"] = ordinal

    params["incPensions"] = inc_pensions

    params["incHmrc"] = inc_hmrc

    params["incAeos"] = inc_aeos

    params["incDeductions"] = inc_deductions

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[BankPaymentInstructionReportResponse]:
    if response.status_code == 200:
        response_200 = BankPaymentInstructionReportResponse.from_dict(response.json())

        return response_200
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[BankPaymentInstructionReportResponse]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    payment_date: Union[Unset, None, datetime.datetime] = UNSET,
    ordinal: Union[Unset, None, int] = 1,
    inc_pensions: Union[Unset, None, bool] = False,
    inc_hmrc: Union[Unset, None, bool] = False,
    inc_aeos: Union[Unset, None, bool] = False,
    inc_deductions: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,
) -> Response[BankPaymentInstructionReportResponse]:
    """Bank Payment Instructions

     Returns a list of bank payments that need to be made to employees as a result of a Payrun.
    You can optionally provide a PaymentDate and only payments for that date will be returned.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        payment_date (Union[Unset, None, datetime.datetime]):
        ordinal (Union[Unset, None, int]):  Default: 1.
        inc_pensions (Union[Unset, None, bool]):
        inc_hmrc (Union[Unset, None, bool]):
        inc_aeos (Union[Unset, None, bool]):
        inc_deductions (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[BankPaymentInstructionReportResponse]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        client=client,
        payment_date=payment_date,
        ordinal=ordinal,
        inc_pensions=inc_pensions,
        inc_hmrc=inc_hmrc,
        inc_aeos=inc_aeos,
        inc_deductions=inc_deductions,
        accept=accept,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    payment_date: Union[Unset, None, datetime.datetime] = UNSET,
    ordinal: Union[Unset, None, int] = 1,
    inc_pensions: Union[Unset, None, bool] = False,
    inc_hmrc: Union[Unset, None, bool] = False,
    inc_aeos: Union[Unset, None, bool] = False,
    inc_deductions: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,
) -> Optional[BankPaymentInstructionReportResponse]:
    """Bank Payment Instructions

     Returns a list of bank payments that need to be made to employees as a result of a Payrun.
    You can optionally provide a PaymentDate and only payments for that date will be returned.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        payment_date (Union[Unset, None, datetime.datetime]):
        ordinal (Union[Unset, None, int]):  Default: 1.
        inc_pensions (Union[Unset, None, bool]):
        inc_hmrc (Union[Unset, None, bool]):
        inc_aeos (Union[Unset, None, bool]):
        inc_deductions (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[BankPaymentInstructionReportResponse]
    """

    return sync_detailed(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        client=client,
        payment_date=payment_date,
        ordinal=ordinal,
        inc_pensions=inc_pensions,
        inc_hmrc=inc_hmrc,
        inc_aeos=inc_aeos,
        inc_deductions=inc_deductions,
        accept=accept,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    payment_date: Union[Unset, None, datetime.datetime] = UNSET,
    ordinal: Union[Unset, None, int] = 1,
    inc_pensions: Union[Unset, None, bool] = False,
    inc_hmrc: Union[Unset, None, bool] = False,
    inc_aeos: Union[Unset, None, bool] = False,
    inc_deductions: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,
) -> Response[BankPaymentInstructionReportResponse]:
    """Bank Payment Instructions

     Returns a list of bank payments that need to be made to employees as a result of a Payrun.
    You can optionally provide a PaymentDate and only payments for that date will be returned.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        payment_date (Union[Unset, None, datetime.datetime]):
        ordinal (Union[Unset, None, int]):  Default: 1.
        inc_pensions (Union[Unset, None, bool]):
        inc_hmrc (Union[Unset, None, bool]):
        inc_aeos (Union[Unset, None, bool]):
        inc_deductions (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[BankPaymentInstructionReportResponse]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        client=client,
        payment_date=payment_date,
        ordinal=ordinal,
        inc_pensions=inc_pensions,
        inc_hmrc=inc_hmrc,
        inc_aeos=inc_aeos,
        inc_deductions=inc_deductions,
        accept=accept,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    payment_date: Union[Unset, None, datetime.datetime] = UNSET,
    ordinal: Union[Unset, None, int] = 1,
    inc_pensions: Union[Unset, None, bool] = False,
    inc_hmrc: Union[Unset, None, bool] = False,
    inc_aeos: Union[Unset, None, bool] = False,
    inc_deductions: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,
) -> Optional[BankPaymentInstructionReportResponse]:
    """Bank Payment Instructions

     Returns a list of bank payments that need to be made to employees as a result of a Payrun.
    You can optionally provide a PaymentDate and only payments for that date will be returned.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        payment_date (Union[Unset, None, datetime.datetime]):
        ordinal (Union[Unset, None, int]):  Default: 1.
        inc_pensions (Union[Unset, None, bool]):
        inc_hmrc (Union[Unset, None, bool]):
        inc_aeos (Union[Unset, None, bool]):
        inc_deductions (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[BankPaymentInstructionReportResponse]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            tax_year=tax_year,
            pay_period=pay_period,
            period_number=period_number,
            client=client,
            payment_date=payment_date,
            ordinal=ordinal,
            inc_pensions=inc_pensions,
            inc_hmrc=inc_hmrc,
            inc_aeos=inc_aeos,
            inc_deductions=inc_deductions,
            accept=accept,
        )
    ).parsed
