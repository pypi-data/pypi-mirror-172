import datetime
from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.national_insurance_calculation_period_values import (
    NationalInsuranceCalculationPeriodValues,
)
from ...models.pay_periods import PayPeriods
from ...models.tax_year import TaxYear
from ...types import UNSET, Response, Unset


def _get_kwargs(
    tax_year: TaxYear,
    pay_period: PayPeriods,
    *,
    client: Client,
    period_start: Union[Unset, None, datetime.datetime] = UNSET,
    period_end: Union[Unset, None, datetime.datetime] = UNSET,
    effective_date: Union[Unset, None, datetime.datetime] = UNSET,
) -> Dict[str, Any]:
    url = "{}/engine/config/{taxYear}/ni/{payPeriod}".format(
        client.base_url, taxYear=tax_year, payPeriod=pay_period
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_period_start: Union[Unset, None, str] = UNSET
    if not isinstance(period_start, Unset):
        json_period_start = period_start.isoformat() if period_start else None

    params["periodStart"] = json_period_start

    json_period_end: Union[Unset, None, str] = UNSET
    if not isinstance(period_end, Unset):
        json_period_end = period_end.isoformat() if period_end else None

    params["periodEnd"] = json_period_end

    json_effective_date: Union[Unset, None, str] = UNSET
    if not isinstance(effective_date, Unset):
        json_effective_date = effective_date.isoformat() if effective_date else None

    params["effectiveDate"] = json_effective_date

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
) -> Optional[NationalInsuranceCalculationPeriodValues]:
    if response.status_code == 200:
        response_200 = NationalInsuranceCalculationPeriodValues.from_dict(
            response.json()
        )

        return response_200
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[NationalInsuranceCalculationPeriodValues]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    tax_year: TaxYear,
    pay_period: PayPeriods,
    *,
    client: Client,
    period_start: Union[Unset, None, datetime.datetime] = UNSET,
    period_end: Union[Unset, None, datetime.datetime] = UNSET,
    effective_date: Union[Unset, None, datetime.datetime] = UNSET,
) -> Response[NationalInsuranceCalculationPeriodValues]:
    """Get National Insurance Thresholds

     Returns the National Insurance thresholds for the given PayPeriod

    Args:
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_start (Union[Unset, None, datetime.datetime]):
        period_end (Union[Unset, None, datetime.datetime]):
        effective_date (Union[Unset, None, datetime.datetime]):

    Returns:
        Response[NationalInsuranceCalculationPeriodValues]
    """

    kwargs = _get_kwargs(
        tax_year=tax_year,
        pay_period=pay_period,
        client=client,
        period_start=period_start,
        period_end=period_end,
        effective_date=effective_date,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    tax_year: TaxYear,
    pay_period: PayPeriods,
    *,
    client: Client,
    period_start: Union[Unset, None, datetime.datetime] = UNSET,
    period_end: Union[Unset, None, datetime.datetime] = UNSET,
    effective_date: Union[Unset, None, datetime.datetime] = UNSET,
) -> Optional[NationalInsuranceCalculationPeriodValues]:
    """Get National Insurance Thresholds

     Returns the National Insurance thresholds for the given PayPeriod

    Args:
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_start (Union[Unset, None, datetime.datetime]):
        period_end (Union[Unset, None, datetime.datetime]):
        effective_date (Union[Unset, None, datetime.datetime]):

    Returns:
        Response[NationalInsuranceCalculationPeriodValues]
    """

    return sync_detailed(
        tax_year=tax_year,
        pay_period=pay_period,
        client=client,
        period_start=period_start,
        period_end=period_end,
        effective_date=effective_date,
    ).parsed


async def asyncio_detailed(
    tax_year: TaxYear,
    pay_period: PayPeriods,
    *,
    client: Client,
    period_start: Union[Unset, None, datetime.datetime] = UNSET,
    period_end: Union[Unset, None, datetime.datetime] = UNSET,
    effective_date: Union[Unset, None, datetime.datetime] = UNSET,
) -> Response[NationalInsuranceCalculationPeriodValues]:
    """Get National Insurance Thresholds

     Returns the National Insurance thresholds for the given PayPeriod

    Args:
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_start (Union[Unset, None, datetime.datetime]):
        period_end (Union[Unset, None, datetime.datetime]):
        effective_date (Union[Unset, None, datetime.datetime]):

    Returns:
        Response[NationalInsuranceCalculationPeriodValues]
    """

    kwargs = _get_kwargs(
        tax_year=tax_year,
        pay_period=pay_period,
        client=client,
        period_start=period_start,
        period_end=period_end,
        effective_date=effective_date,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    tax_year: TaxYear,
    pay_period: PayPeriods,
    *,
    client: Client,
    period_start: Union[Unset, None, datetime.datetime] = UNSET,
    period_end: Union[Unset, None, datetime.datetime] = UNSET,
    effective_date: Union[Unset, None, datetime.datetime] = UNSET,
) -> Optional[NationalInsuranceCalculationPeriodValues]:
    """Get National Insurance Thresholds

     Returns the National Insurance thresholds for the given PayPeriod

    Args:
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_start (Union[Unset, None, datetime.datetime]):
        period_end (Union[Unset, None, datetime.datetime]):
        effective_date (Union[Unset, None, datetime.datetime]):

    Returns:
        Response[NationalInsuranceCalculationPeriodValues]
    """

    return (
        await asyncio_detailed(
            tax_year=tax_year,
            pay_period=pay_period,
            client=client,
            period_start=period_start,
            period_end=period_end,
            effective_date=effective_date,
        )
    ).parsed
