from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import Client
from ...models.pay_periods import PayPeriods
from ...models.pay_schedule_period import PaySchedulePeriod
from ...models.tax_year import TaxYear
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    ordinal: int,
    *,
    client: Client,
    period_number: Union[Unset, None, int] = UNSET,
    include_events: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/schedules/{taxYear}/{payPeriod}/{ordinal}/periods".format(
        client.base_url,
        employerId=employer_id,
        taxYear=tax_year,
        payPeriod=pay_period,
        ordinal=ordinal,
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["periodNumber"] = period_number

    params["includeEvents"] = include_events

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
) -> Optional[Union[Any, List[PaySchedulePeriod]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = PaySchedulePeriod.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[Any, List[PaySchedulePeriod]]]:
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
    *,
    client: Client,
    period_number: Union[Unset, None, int] = UNSET,
    include_events: Union[Unset, None, bool] = False,
) -> Response[Union[Any, List[PaySchedulePeriod]]]:
    """Get PaySchedulePeriods

     Get the PaySchedulePeriods for PaySchedule specified.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        ordinal (int):
        period_number (Union[Unset, None, int]):
        include_events (Union[Unset, None, bool]):

    Returns:
        Response[Union[Any, List[PaySchedulePeriod]]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        ordinal=ordinal,
        client=client,
        period_number=period_number,
        include_events=include_events,
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
    *,
    client: Client,
    period_number: Union[Unset, None, int] = UNSET,
    include_events: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, List[PaySchedulePeriod]]]:
    """Get PaySchedulePeriods

     Get the PaySchedulePeriods for PaySchedule specified.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        ordinal (int):
        period_number (Union[Unset, None, int]):
        include_events (Union[Unset, None, bool]):

    Returns:
        Response[Union[Any, List[PaySchedulePeriod]]]
    """

    return sync_detailed(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        ordinal=ordinal,
        client=client,
        period_number=period_number,
        include_events=include_events,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    ordinal: int,
    *,
    client: Client,
    period_number: Union[Unset, None, int] = UNSET,
    include_events: Union[Unset, None, bool] = False,
) -> Response[Union[Any, List[PaySchedulePeriod]]]:
    """Get PaySchedulePeriods

     Get the PaySchedulePeriods for PaySchedule specified.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        ordinal (int):
        period_number (Union[Unset, None, int]):
        include_events (Union[Unset, None, bool]):

    Returns:
        Response[Union[Any, List[PaySchedulePeriod]]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        ordinal=ordinal,
        client=client,
        period_number=period_number,
        include_events=include_events,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    ordinal: int,
    *,
    client: Client,
    period_number: Union[Unset, None, int] = UNSET,
    include_events: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, List[PaySchedulePeriod]]]:
    """Get PaySchedulePeriods

     Get the PaySchedulePeriods for PaySchedule specified.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        ordinal (int):
        period_number (Union[Unset, None, int]):
        include_events (Union[Unset, None, bool]):

    Returns:
        Response[Union[Any, List[PaySchedulePeriod]]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            tax_year=tax_year,
            pay_period=pay_period,
            ordinal=ordinal,
            client=client,
            period_number=period_number,
            include_events=include_events,
        )
    ).parsed
