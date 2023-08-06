import datetime
from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.hmrc_liability import HmrcLiability
from ...models.tax_year import TaxYear
from ...types import Response


def _get_kwargs(
    employer_id: str,
    tax_year: TaxYear,
    period_ending: datetime.datetime,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/hmrcpayment/{taxYear}/{periodEnding}".format(
        client.base_url,
        employerId=employer_id,
        taxYear=tax_year,
        periodEnding=period_ending,
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[HmrcLiability]:
    if response.status_code == 200:
        response_200 = HmrcLiability.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[HmrcLiability]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    tax_year: TaxYear,
    period_ending: datetime.datetime,
    *,
    client: Client,
) -> Response[HmrcLiability]:
    """Get HmrcLiability

     Gets the HmrcLiability record for the period ending on the date specified.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        period_ending (datetime.datetime):

    Returns:
        Response[HmrcLiability]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        period_ending=period_ending,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    employer_id: str,
    tax_year: TaxYear,
    period_ending: datetime.datetime,
    *,
    client: Client,
) -> Optional[HmrcLiability]:
    """Get HmrcLiability

     Gets the HmrcLiability record for the period ending on the date specified.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        period_ending (datetime.datetime):

    Returns:
        Response[HmrcLiability]
    """

    return sync_detailed(
        employer_id=employer_id,
        tax_year=tax_year,
        period_ending=period_ending,
        client=client,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    tax_year: TaxYear,
    period_ending: datetime.datetime,
    *,
    client: Client,
) -> Response[HmrcLiability]:
    """Get HmrcLiability

     Gets the HmrcLiability record for the period ending on the date specified.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        period_ending (datetime.datetime):

    Returns:
        Response[HmrcLiability]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        period_ending=period_ending,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    tax_year: TaxYear,
    period_ending: datetime.datetime,
    *,
    client: Client,
) -> Optional[HmrcLiability]:
    """Get HmrcLiability

     Gets the HmrcLiability record for the period ending on the date specified.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        period_ending (datetime.datetime):

    Returns:
        Response[HmrcLiability]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            tax_year=tax_year,
            period_ending=period_ending,
            client=client,
        )
    ).parsed
