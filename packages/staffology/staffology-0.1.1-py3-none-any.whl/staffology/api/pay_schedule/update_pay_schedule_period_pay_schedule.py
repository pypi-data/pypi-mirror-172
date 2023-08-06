from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.pay_periods import PayPeriods
from ...models.pay_schedule_period import PaySchedulePeriod
from ...models.tax_year import TaxYear
from ...types import Response


def _get_kwargs(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    ordinal: int,
    period_number: int,
    *,
    client: Client,
    json_body: PaySchedulePeriod,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/schedules/{taxYear}/{payPeriod}/{ordinal}/periods/{periodNumber}".format(
        client.base_url,
        employerId=employer_id,
        taxYear=tax_year,
        payPeriod=pay_period,
        ordinal=ordinal,
        periodNumber=period_number,
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[Any, PaySchedulePeriod]]:
    if response.status_code == 200:
        response_200 = PaySchedulePeriod.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[Any, PaySchedulePeriod]]:
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
    ordinal: int,
    period_number: int,
    *,
    client: Client,
    json_body: PaySchedulePeriod,
) -> Response[Union[Any, PaySchedulePeriod]]:
    """Update PaySchedulePeriod

     Update the PaymentDate for a PaySchedulePeriod.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        ordinal (int):
        period_number (int):
        json_body (PaySchedulePeriod):

    Returns:
        Response[Union[Any, PaySchedulePeriod]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        ordinal=ordinal,
        period_number=period_number,
        client=client,
        json_body=json_body,
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
    ordinal: int,
    period_number: int,
    *,
    client: Client,
    json_body: PaySchedulePeriod,
) -> Optional[Union[Any, PaySchedulePeriod]]:
    """Update PaySchedulePeriod

     Update the PaymentDate for a PaySchedulePeriod.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        ordinal (int):
        period_number (int):
        json_body (PaySchedulePeriod):

    Returns:
        Response[Union[Any, PaySchedulePeriod]]
    """

    return sync_detailed(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        ordinal=ordinal,
        period_number=period_number,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    ordinal: int,
    period_number: int,
    *,
    client: Client,
    json_body: PaySchedulePeriod,
) -> Response[Union[Any, PaySchedulePeriod]]:
    """Update PaySchedulePeriod

     Update the PaymentDate for a PaySchedulePeriod.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        ordinal (int):
        period_number (int):
        json_body (PaySchedulePeriod):

    Returns:
        Response[Union[Any, PaySchedulePeriod]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        ordinal=ordinal,
        period_number=period_number,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    ordinal: int,
    period_number: int,
    *,
    client: Client,
    json_body: PaySchedulePeriod,
) -> Optional[Union[Any, PaySchedulePeriod]]:
    """Update PaySchedulePeriod

     Update the PaymentDate for a PaySchedulePeriod.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        ordinal (int):
        period_number (int):
        json_body (PaySchedulePeriod):

    Returns:
        Response[Union[Any, PaySchedulePeriod]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            tax_year=tax_year,
            pay_period=pay_period,
            ordinal=ordinal,
            period_number=period_number,
            client=client,
            json_body=json_body,
        )
    ).parsed
