from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.pay_periods import PayPeriods
from ...models.pay_schedule import PaySchedule
from ...models.tax_year import TaxYear
from ...types import Response


def _get_kwargs(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    ordinal: int = 1,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/schedules/{taxYear}/{payPeriod}/{ordinal}".format(
        client.base_url,
        employerId=employer_id,
        taxYear=tax_year,
        payPeriod=pay_period,
        ordinal=ordinal,
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


def _parse_response(*, response: httpx.Response) -> Optional[PaySchedule]:
    if response.status_code == 200:
        response_200 = PaySchedule.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[PaySchedule]:
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
    ordinal: int = 1,
    *,
    client: Client,
) -> Response[PaySchedule]:
    """Get PaySchedule

     Get the PaySchedule for the PayPeriod and TaxYear specified.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        ordinal (int):  Default: 1.

    Returns:
        Response[PaySchedule]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        ordinal=ordinal,
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
    pay_period: PayPeriods,
    ordinal: int = 1,
    *,
    client: Client,
) -> Optional[PaySchedule]:
    """Get PaySchedule

     Get the PaySchedule for the PayPeriod and TaxYear specified.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        ordinal (int):  Default: 1.

    Returns:
        Response[PaySchedule]
    """

    return sync_detailed(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        ordinal=ordinal,
        client=client,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    ordinal: int = 1,
    *,
    client: Client,
) -> Response[PaySchedule]:
    """Get PaySchedule

     Get the PaySchedule for the PayPeriod and TaxYear specified.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        ordinal (int):  Default: 1.

    Returns:
        Response[PaySchedule]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        ordinal=ordinal,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    ordinal: int = 1,
    *,
    client: Client,
) -> Optional[PaySchedule]:
    """Get PaySchedule

     Get the PaySchedule for the PayPeriod and TaxYear specified.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        ordinal (int):  Default: 1.

    Returns:
        Response[PaySchedule]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            tax_year=tax_year,
            pay_period=pay_period,
            ordinal=ordinal,
            client=client,
        )
    ).parsed
