from typing import Any, Dict, Optional, Union, cast

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
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, PaySchedule]]:
    if response.status_code == 200:
        response_200 = PaySchedule.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, PaySchedule]]:
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
    *,
    client: Client,
    json_body: PaySchedule,
    ordinal: Union[Unset, None, int] = UNSET,
) -> Response[Union[Any, PaySchedule]]:
    """Update PaySchedule (deprecated)

     Update PaySchedule for the PayPeriod and TaxYear specified (and an optional ordinal. 1 will be used
    if ordinal is not provided).

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        ordinal (Union[Unset, None, int]):
        json_body (PaySchedule):

    Returns:
        Response[Union[Any, PaySchedule]]
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


def sync(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    *,
    client: Client,
    json_body: PaySchedule,
    ordinal: Union[Unset, None, int] = UNSET,
) -> Optional[Union[Any, PaySchedule]]:
    """Update PaySchedule (deprecated)

     Update PaySchedule for the PayPeriod and TaxYear specified (and an optional ordinal. 1 will be used
    if ordinal is not provided).

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        ordinal (Union[Unset, None, int]):
        json_body (PaySchedule):

    Returns:
        Response[Union[Any, PaySchedule]]
    """

    return sync_detailed(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        client=client,
        json_body=json_body,
        ordinal=ordinal,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    *,
    client: Client,
    json_body: PaySchedule,
    ordinal: Union[Unset, None, int] = UNSET,
) -> Response[Union[Any, PaySchedule]]:
    """Update PaySchedule (deprecated)

     Update PaySchedule for the PayPeriod and TaxYear specified (and an optional ordinal. 1 will be used
    if ordinal is not provided).

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        ordinal (Union[Unset, None, int]):
        json_body (PaySchedule):

    Returns:
        Response[Union[Any, PaySchedule]]
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


async def asyncio(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    *,
    client: Client,
    json_body: PaySchedule,
    ordinal: Union[Unset, None, int] = UNSET,
) -> Optional[Union[Any, PaySchedule]]:
    """Update PaySchedule (deprecated)

     Update PaySchedule for the PayPeriod and TaxYear specified (and an optional ordinal. 1 will be used
    if ordinal is not provided).

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        ordinal (Union[Unset, None, int]):
        json_body (PaySchedule):

    Returns:
        Response[Union[Any, PaySchedule]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            tax_year=tax_year,
            pay_period=pay_period,
            client=client,
            json_body=json_body,
            ordinal=ordinal,
        )
    ).parsed
