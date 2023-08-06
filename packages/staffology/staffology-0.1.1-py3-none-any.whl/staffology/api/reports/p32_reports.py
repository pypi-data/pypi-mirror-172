from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.p32_report_response import P32ReportResponse
from ...models.tax_year import TaxYear
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    tax_year: TaxYear,
    *,
    client: Client,
    accept: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/reports/{taxYear}/p32".format(
        client.base_url, employerId=employer_id, taxYear=tax_year
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(accept, Unset):
        headers["accept"] = accept

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[P32ReportResponse]:
    if response.status_code == 200:
        response_200 = P32ReportResponse.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[P32ReportResponse]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    tax_year: TaxYear,
    *,
    client: Client,
    accept: Union[Unset, str] = UNSET,
) -> Response[P32ReportResponse]:
    """P32

     Returns a P32 Report detailing the employers HMRC liabilities for the year.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        accept (Union[Unset, str]):

    Returns:
        Response[P32ReportResponse]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        client=client,
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
    *,
    client: Client,
    accept: Union[Unset, str] = UNSET,
) -> Optional[P32ReportResponse]:
    """P32

     Returns a P32 Report detailing the employers HMRC liabilities for the year.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        accept (Union[Unset, str]):

    Returns:
        Response[P32ReportResponse]
    """

    return sync_detailed(
        employer_id=employer_id,
        tax_year=tax_year,
        client=client,
        accept=accept,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    tax_year: TaxYear,
    *,
    client: Client,
    accept: Union[Unset, str] = UNSET,
) -> Response[P32ReportResponse]:
    """P32

     Returns a P32 Report detailing the employers HMRC liabilities for the year.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        accept (Union[Unset, str]):

    Returns:
        Response[P32ReportResponse]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        client=client,
        accept=accept,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    tax_year: TaxYear,
    *,
    client: Client,
    accept: Union[Unset, str] = UNSET,
) -> Optional[P32ReportResponse]:
    """P32

     Returns a P32 Report detailing the employers HMRC liabilities for the year.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        accept (Union[Unset, str]):

    Returns:
        Response[P32ReportResponse]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            tax_year=tax_year,
            client=client,
            accept=accept,
        )
    ).parsed
