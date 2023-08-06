from typing import Any, Dict

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
    json_body: PaySchedule,
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

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    ordinal: int = 1,
    *,
    client: Client,
    json_body: PaySchedule,
) -> Response[Any]:
    """Create a PaySchedule

     Create PaySchedule using a certain pay frequency.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        ordinal (int):  Default: 1.
        json_body (PaySchedule):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        ordinal=ordinal,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    ordinal: int = 1,
    *,
    client: Client,
    json_body: PaySchedule,
) -> Response[Any]:
    """Create a PaySchedule

     Create PaySchedule using a certain pay frequency.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        ordinal (int):  Default: 1.
        json_body (PaySchedule):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        ordinal=ordinal,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
