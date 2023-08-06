from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.pay_periods import PayPeriods
from ...models.pay_run_journal import PayRunJournal
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
    dept_breakdown: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/payrun/{taxYear}/{payPeriod}/{periodNumber}/journal".format(
        client.base_url,
        employerId=employer_id,
        taxYear=tax_year,
        payPeriod=pay_period,
        periodNumber=period_number,
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["ordinal"] = ordinal

    params["deptBreakdown"] = dept_breakdown

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[PayRunJournal]:
    if response.status_code == 200:
        response_200 = PayRunJournal.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[PayRunJournal]:
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
    dept_breakdown: Union[Unset, None, bool] = False,
) -> Response[PayRunJournal]:
    """Get Journal for PayRun

     Returns values that can be used to create accounting entries for this PayRun.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):  Default: 1.
        dept_breakdown (Union[Unset, None, bool]):

    Returns:
        Response[PayRunJournal]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        client=client,
        ordinal=ordinal,
        dept_breakdown=dept_breakdown,
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
    dept_breakdown: Union[Unset, None, bool] = False,
) -> Optional[PayRunJournal]:
    """Get Journal for PayRun

     Returns values that can be used to create accounting entries for this PayRun.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):  Default: 1.
        dept_breakdown (Union[Unset, None, bool]):

    Returns:
        Response[PayRunJournal]
    """

    return sync_detailed(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        client=client,
        ordinal=ordinal,
        dept_breakdown=dept_breakdown,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    ordinal: Union[Unset, None, int] = 1,
    dept_breakdown: Union[Unset, None, bool] = False,
) -> Response[PayRunJournal]:
    """Get Journal for PayRun

     Returns values that can be used to create accounting entries for this PayRun.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):  Default: 1.
        dept_breakdown (Union[Unset, None, bool]):

    Returns:
        Response[PayRunJournal]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        client=client,
        ordinal=ordinal,
        dept_breakdown=dept_breakdown,
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
    dept_breakdown: Union[Unset, None, bool] = False,
) -> Optional[PayRunJournal]:
    """Get Journal for PayRun

     Returns values that can be used to create accounting entries for this PayRun.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):  Default: 1.
        dept_breakdown (Union[Unset, None, bool]):

    Returns:
        Response[PayRunJournal]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            tax_year=tax_year,
            pay_period=pay_period,
            period_number=period_number,
            client=client,
            ordinal=ordinal,
            dept_breakdown=dept_breakdown,
        )
    ).parsed
