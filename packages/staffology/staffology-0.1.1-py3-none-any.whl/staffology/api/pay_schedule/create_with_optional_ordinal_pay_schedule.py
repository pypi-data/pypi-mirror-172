from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...models.pay_periods import PayPeriods
from ...models.pay_schedule import PaySchedule
from ...models.tax_year import TaxYear
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    *,
    client: Client,
    json_body: PaySchedule,
    ordinal: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/schedules/{taxYear}/{payPeriod}".format(
        client.base_url, employerId=employer_id, taxYear=tax_year, payPeriod=pay_period
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["ordinal"] = ordinal

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
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
    *,
    client: Client,
    json_body: PaySchedule,
    ordinal: Union[Unset, None, int] = UNSET,
) -> Response[Any]:
    """Create a PaySchedule (deprecated)

     Create PaySchedule using a certain pay frequency and TaxYear specified (and an optional ordinal. 1
    will be used if ordinal is not provided).

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        ordinal (Union[Unset, None, int]):
        json_body (PaySchedule):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        client=client,
        json_body=json_body,
        ordinal=ordinal,
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
    *,
    client: Client,
    json_body: PaySchedule,
    ordinal: Union[Unset, None, int] = UNSET,
) -> Response[Any]:
    """Create a PaySchedule (deprecated)

     Create PaySchedule using a certain pay frequency and TaxYear specified (and an optional ordinal. 1
    will be used if ordinal is not provided).

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        ordinal (Union[Unset, None, int]):
        json_body (PaySchedule):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        client=client,
        json_body=json_body,
        ordinal=ordinal,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
