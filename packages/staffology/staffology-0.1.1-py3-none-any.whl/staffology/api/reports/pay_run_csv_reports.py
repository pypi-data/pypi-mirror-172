from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.pay_periods import PayPeriods
from ...models.report_response import ReportResponse
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
    summary: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/reports/{taxYear}/{payPeriod}/{periodNumber}/payrun-csv".format(
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

    params["summary"] = summary

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[ReportResponse]:
    if response.status_code == 200:
        response_200 = ReportResponse.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[ReportResponse]:
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
    summary: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,
) -> Response[ReportResponse]:
    """PayRun CSV (deprecated)

     Download the lines of a PayRun to a CSV file.
    Please use Get PayRun CSV that now accepts a parameter for CSV type

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):  Default: 1.
        summary (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[ReportResponse]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        client=client,
        ordinal=ordinal,
        summary=summary,
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
    summary: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,
) -> Optional[ReportResponse]:
    """PayRun CSV (deprecated)

     Download the lines of a PayRun to a CSV file.
    Please use Get PayRun CSV that now accepts a parameter for CSV type

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):  Default: 1.
        summary (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[ReportResponse]
    """

    return sync_detailed(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        client=client,
        ordinal=ordinal,
        summary=summary,
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
    summary: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,
) -> Response[ReportResponse]:
    """PayRun CSV (deprecated)

     Download the lines of a PayRun to a CSV file.
    Please use Get PayRun CSV that now accepts a parameter for CSV type

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):  Default: 1.
        summary (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[ReportResponse]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        client=client,
        ordinal=ordinal,
        summary=summary,
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
    summary: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,
) -> Optional[ReportResponse]:
    """PayRun CSV (deprecated)

     Download the lines of a PayRun to a CSV file.
    Please use Get PayRun CSV that now accepts a parameter for CSV type

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):  Default: 1.
        summary (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[ReportResponse]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            tax_year=tax_year,
            pay_period=pay_period,
            period_number=period_number,
            client=client,
            ordinal=ordinal,
            summary=summary,
            accept=accept,
        )
    ).parsed
