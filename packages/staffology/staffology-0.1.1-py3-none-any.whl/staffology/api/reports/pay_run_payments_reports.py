from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.pay_periods import PayPeriods
from ...models.payrun_payments_report_report_response import (
    PayrunPaymentsReportReportResponse,
)
from ...models.tax_year import TaxYear
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    ordinal: Union[Unset, None, int] = 1,
    include_non_employee_payments: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/reports/{taxYear}/{payPeriod}/{periodNumber}/payments/employee".format(
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
    params["ordinal"] = ordinal

    params["includeNonEmployeePayments"] = include_non_employee_payments

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
) -> Optional[PayrunPaymentsReportReportResponse]:
    if response.status_code == 200:
        response_200 = PayrunPaymentsReportReportResponse.from_dict(response.json())

        return response_200
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[PayrunPaymentsReportReportResponse]:
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
    ordinal: Union[Unset, None, int] = 1,
    include_non_employee_payments: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,
) -> Response[PayrunPaymentsReportReportResponse]:
    """PayRun Payments

     Returns a list of all employee payments that need to be made as a result of a Payrun.
    If you specifically want just bank payments (employees where PayMethod is Credit) then you
    may find the Bank Payment Instructions API call more useful

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):  Default: 1.
        include_non_employee_payments (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[PayrunPaymentsReportReportResponse]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        client=client,
        ordinal=ordinal,
        include_non_employee_payments=include_non_employee_payments,
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
    ordinal: Union[Unset, None, int] = 1,
    include_non_employee_payments: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,
) -> Optional[PayrunPaymentsReportReportResponse]:
    """PayRun Payments

     Returns a list of all employee payments that need to be made as a result of a Payrun.
    If you specifically want just bank payments (employees where PayMethod is Credit) then you
    may find the Bank Payment Instructions API call more useful

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):  Default: 1.
        include_non_employee_payments (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[PayrunPaymentsReportReportResponse]
    """

    return sync_detailed(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        client=client,
        ordinal=ordinal,
        include_non_employee_payments=include_non_employee_payments,
        accept=accept,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    ordinal: Union[Unset, None, int] = 1,
    include_non_employee_payments: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,
) -> Response[PayrunPaymentsReportReportResponse]:
    """PayRun Payments

     Returns a list of all employee payments that need to be made as a result of a Payrun.
    If you specifically want just bank payments (employees where PayMethod is Credit) then you
    may find the Bank Payment Instructions API call more useful

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):  Default: 1.
        include_non_employee_payments (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[PayrunPaymentsReportReportResponse]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        client=client,
        ordinal=ordinal,
        include_non_employee_payments=include_non_employee_payments,
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
    ordinal: Union[Unset, None, int] = 1,
    include_non_employee_payments: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,
) -> Optional[PayrunPaymentsReportReportResponse]:
    """PayRun Payments

     Returns a list of all employee payments that need to be made as a result of a Payrun.
    If you specifically want just bank payments (employees where PayMethod is Credit) then you
    may find the Bank Payment Instructions API call more useful

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):  Default: 1.
        include_non_employee_payments (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[PayrunPaymentsReportReportResponse]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            tax_year=tax_year,
            pay_period=pay_period,
            period_number=period_number,
            client=client,
            ordinal=ordinal,
            include_non_employee_payments=include_non_employee_payments,
            accept=accept,
        )
    ).parsed
