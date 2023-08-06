import datetime
from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.pay_periods import PayPeriods
from ...models.tax_year import TaxYear
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    tax_year: Union[Unset, None, TaxYear] = UNSET,
    tax_code: Union[Unset, None, str] = UNSET,
    gross: Union[Unset, None, float] = UNSET,
    period_start: Union[Unset, None, datetime.datetime] = UNSET,
    period_end: Union[Unset, None, datetime.datetime] = UNSET,
    pay_period: Union[Unset, None, PayPeriods] = UNSET,
    period: Union[Unset, None, int] = 1,
    week1: Union[Unset, None, bool] = False,
    gross_to_date: Union[Unset, None, float] = 0.0,
    tax_to_date: Union[Unset, None, float] = 0.0,
) -> Dict[str, Any]:
    url = "{}/engine/tax".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_tax_year: Union[Unset, None, str] = UNSET
    if not isinstance(tax_year, Unset):
        json_tax_year = tax_year.value if tax_year else None

    params["taxYear"] = json_tax_year

    params["taxCode"] = tax_code

    params["gross"] = gross

    json_period_start: Union[Unset, None, str] = UNSET
    if not isinstance(period_start, Unset):
        json_period_start = period_start.isoformat() if period_start else None

    params["periodStart"] = json_period_start

    json_period_end: Union[Unset, None, str] = UNSET
    if not isinstance(period_end, Unset):
        json_period_end = period_end.isoformat() if period_end else None

    params["periodEnd"] = json_period_end

    json_pay_period: Union[Unset, None, str] = UNSET
    if not isinstance(pay_period, Unset):
        json_pay_period = pay_period.value if pay_period else None

    params["payPeriod"] = json_pay_period

    params["period"] = period

    params["week1"] = week1

    params["grossToDate"] = gross_to_date

    params["taxToDate"] = tax_to_date

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[float]:
    if response.status_code == 200:
        response_200 = cast(float, response.json())
        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[float]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    tax_year: Union[Unset, None, TaxYear] = UNSET,
    tax_code: Union[Unset, None, str] = UNSET,
    gross: Union[Unset, None, float] = UNSET,
    period_start: Union[Unset, None, datetime.datetime] = UNSET,
    period_end: Union[Unset, None, datetime.datetime] = UNSET,
    pay_period: Union[Unset, None, PayPeriods] = UNSET,
    period: Union[Unset, None, int] = 1,
    week1: Union[Unset, None, bool] = False,
    gross_to_date: Union[Unset, None, float] = 0.0,
    tax_to_date: Union[Unset, None, float] = 0.0,
) -> Response[float]:
    """Calculate Tax due

     Calculates tax amount due, given the values specified.
    You would never need to use this API call. It is provided just for information and testing purposes.
    Access is limited so you'll probably receive a 401 response if you try to use it.

    Args:
        tax_year (Union[Unset, None, TaxYear]):
        tax_code (Union[Unset, None, str]):
        gross (Union[Unset, None, float]):
        period_start (Union[Unset, None, datetime.datetime]):
        period_end (Union[Unset, None, datetime.datetime]):
        pay_period (Union[Unset, None, PayPeriods]):
        period (Union[Unset, None, int]):  Default: 1.
        week1 (Union[Unset, None, bool]):
        gross_to_date (Union[Unset, None, float]):
        tax_to_date (Union[Unset, None, float]):

    Returns:
        Response[float]
    """

    kwargs = _get_kwargs(
        client=client,
        tax_year=tax_year,
        tax_code=tax_code,
        gross=gross,
        period_start=period_start,
        period_end=period_end,
        pay_period=pay_period,
        period=period,
        week1=week1,
        gross_to_date=gross_to_date,
        tax_to_date=tax_to_date,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    tax_year: Union[Unset, None, TaxYear] = UNSET,
    tax_code: Union[Unset, None, str] = UNSET,
    gross: Union[Unset, None, float] = UNSET,
    period_start: Union[Unset, None, datetime.datetime] = UNSET,
    period_end: Union[Unset, None, datetime.datetime] = UNSET,
    pay_period: Union[Unset, None, PayPeriods] = UNSET,
    period: Union[Unset, None, int] = 1,
    week1: Union[Unset, None, bool] = False,
    gross_to_date: Union[Unset, None, float] = 0.0,
    tax_to_date: Union[Unset, None, float] = 0.0,
) -> Optional[float]:
    """Calculate Tax due

     Calculates tax amount due, given the values specified.
    You would never need to use this API call. It is provided just for information and testing purposes.
    Access is limited so you'll probably receive a 401 response if you try to use it.

    Args:
        tax_year (Union[Unset, None, TaxYear]):
        tax_code (Union[Unset, None, str]):
        gross (Union[Unset, None, float]):
        period_start (Union[Unset, None, datetime.datetime]):
        period_end (Union[Unset, None, datetime.datetime]):
        pay_period (Union[Unset, None, PayPeriods]):
        period (Union[Unset, None, int]):  Default: 1.
        week1 (Union[Unset, None, bool]):
        gross_to_date (Union[Unset, None, float]):
        tax_to_date (Union[Unset, None, float]):

    Returns:
        Response[float]
    """

    return sync_detailed(
        client=client,
        tax_year=tax_year,
        tax_code=tax_code,
        gross=gross,
        period_start=period_start,
        period_end=period_end,
        pay_period=pay_period,
        period=period,
        week1=week1,
        gross_to_date=gross_to_date,
        tax_to_date=tax_to_date,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    tax_year: Union[Unset, None, TaxYear] = UNSET,
    tax_code: Union[Unset, None, str] = UNSET,
    gross: Union[Unset, None, float] = UNSET,
    period_start: Union[Unset, None, datetime.datetime] = UNSET,
    period_end: Union[Unset, None, datetime.datetime] = UNSET,
    pay_period: Union[Unset, None, PayPeriods] = UNSET,
    period: Union[Unset, None, int] = 1,
    week1: Union[Unset, None, bool] = False,
    gross_to_date: Union[Unset, None, float] = 0.0,
    tax_to_date: Union[Unset, None, float] = 0.0,
) -> Response[float]:
    """Calculate Tax due

     Calculates tax amount due, given the values specified.
    You would never need to use this API call. It is provided just for information and testing purposes.
    Access is limited so you'll probably receive a 401 response if you try to use it.

    Args:
        tax_year (Union[Unset, None, TaxYear]):
        tax_code (Union[Unset, None, str]):
        gross (Union[Unset, None, float]):
        period_start (Union[Unset, None, datetime.datetime]):
        period_end (Union[Unset, None, datetime.datetime]):
        pay_period (Union[Unset, None, PayPeriods]):
        period (Union[Unset, None, int]):  Default: 1.
        week1 (Union[Unset, None, bool]):
        gross_to_date (Union[Unset, None, float]):
        tax_to_date (Union[Unset, None, float]):

    Returns:
        Response[float]
    """

    kwargs = _get_kwargs(
        client=client,
        tax_year=tax_year,
        tax_code=tax_code,
        gross=gross,
        period_start=period_start,
        period_end=period_end,
        pay_period=pay_period,
        period=period,
        week1=week1,
        gross_to_date=gross_to_date,
        tax_to_date=tax_to_date,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    tax_year: Union[Unset, None, TaxYear] = UNSET,
    tax_code: Union[Unset, None, str] = UNSET,
    gross: Union[Unset, None, float] = UNSET,
    period_start: Union[Unset, None, datetime.datetime] = UNSET,
    period_end: Union[Unset, None, datetime.datetime] = UNSET,
    pay_period: Union[Unset, None, PayPeriods] = UNSET,
    period: Union[Unset, None, int] = 1,
    week1: Union[Unset, None, bool] = False,
    gross_to_date: Union[Unset, None, float] = 0.0,
    tax_to_date: Union[Unset, None, float] = 0.0,
) -> Optional[float]:
    """Calculate Tax due

     Calculates tax amount due, given the values specified.
    You would never need to use this API call. It is provided just for information and testing purposes.
    Access is limited so you'll probably receive a 401 response if you try to use it.

    Args:
        tax_year (Union[Unset, None, TaxYear]):
        tax_code (Union[Unset, None, str]):
        gross (Union[Unset, None, float]):
        period_start (Union[Unset, None, datetime.datetime]):
        period_end (Union[Unset, None, datetime.datetime]):
        pay_period (Union[Unset, None, PayPeriods]):
        period (Union[Unset, None, int]):  Default: 1.
        week1 (Union[Unset, None, bool]):
        gross_to_date (Union[Unset, None, float]):
        tax_to_date (Union[Unset, None, float]):

    Returns:
        Response[float]
    """

    return (
        await asyncio_detailed(
            client=client,
            tax_year=tax_year,
            tax_code=tax_code,
            gross=gross,
            period_start=period_start,
            period_end=period_end,
            pay_period=pay_period,
            period=period,
            week1=week1,
            gross_to_date=gross_to_date,
            tax_to_date=tax_to_date,
        )
    ).parsed
