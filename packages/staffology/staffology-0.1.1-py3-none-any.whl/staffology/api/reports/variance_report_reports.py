from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.pay_periods import PayPeriods
from ...models.tax_year import TaxYear
from ...models.variance_report_report_response import VarianceReportReportResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    *,
    client: Client,
    ordinal: Union[Unset, None, int] = UNSET,
    from_period: Union[Unset, None, int] = UNSET,
    to_period: Union[Unset, None, int] = UNSET,
    pay_period_compare: Union[Unset, None, PayPeriods] = UNSET,
    ordinal_compare: Union[Unset, None, int] = UNSET,
    tax_year_compare: Union[Unset, None, TaxYear] = UNSET,
    from_period_compare: Union[Unset, None, int] = UNSET,
    to_period_compare: Union[Unset, None, int] = UNSET,
    show_percentage: Union[Unset, None, bool] = UNSET,
    min_change: Union[Unset, None, float] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/reports/{taxYear}/{payPeriod}/variance".format(
        client.base_url, employerId=employer_id, taxYear=tax_year, payPeriod=pay_period
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(accept, Unset):
        headers["accept"] = accept

    params: Dict[str, Any] = {}
    params["ordinal"] = ordinal

    params["fromPeriod"] = from_period

    params["toPeriod"] = to_period

    json_pay_period_compare: Union[Unset, None, str] = UNSET
    if not isinstance(pay_period_compare, Unset):
        json_pay_period_compare = (
            pay_period_compare.value if pay_period_compare else None
        )

    params["payPeriodCompare"] = json_pay_period_compare

    params["ordinalCompare"] = ordinal_compare

    json_tax_year_compare: Union[Unset, None, str] = UNSET
    if not isinstance(tax_year_compare, Unset):
        json_tax_year_compare = tax_year_compare.value if tax_year_compare else None

    params["taxYearCompare"] = json_tax_year_compare

    params["fromPeriodCompare"] = from_period_compare

    params["toPeriodCompare"] = to_period_compare

    params["showPercentage"] = show_percentage

    params["minChange"] = min_change

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
) -> Optional[VarianceReportReportResponse]:
    if response.status_code == 200:
        response_200 = VarianceReportReportResponse.from_dict(response.json())

        return response_200
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[VarianceReportReportResponse]:
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
    ordinal: Union[Unset, None, int] = UNSET,
    from_period: Union[Unset, None, int] = UNSET,
    to_period: Union[Unset, None, int] = UNSET,
    pay_period_compare: Union[Unset, None, PayPeriods] = UNSET,
    ordinal_compare: Union[Unset, None, int] = UNSET,
    tax_year_compare: Union[Unset, None, TaxYear] = UNSET,
    from_period_compare: Union[Unset, None, int] = UNSET,
    to_period_compare: Union[Unset, None, int] = UNSET,
    show_percentage: Union[Unset, None, bool] = UNSET,
    min_change: Union[Unset, None, float] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Response[VarianceReportReportResponse]:
    """Variance Report

     Returns a report comparing two pay periods or two ranges of payperiods.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        ordinal (Union[Unset, None, int]):
        from_period (Union[Unset, None, int]):
        to_period (Union[Unset, None, int]):
        pay_period_compare (Union[Unset, None, PayPeriods]):
        ordinal_compare (Union[Unset, None, int]):
        tax_year_compare (Union[Unset, None, TaxYear]):
        from_period_compare (Union[Unset, None, int]):
        to_period_compare (Union[Unset, None, int]):
        show_percentage (Union[Unset, None, bool]):
        min_change (Union[Unset, None, float]):
        accept (Union[Unset, str]):

    Returns:
        Response[VarianceReportReportResponse]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        client=client,
        ordinal=ordinal,
        from_period=from_period,
        to_period=to_period,
        pay_period_compare=pay_period_compare,
        ordinal_compare=ordinal_compare,
        tax_year_compare=tax_year_compare,
        from_period_compare=from_period_compare,
        to_period_compare=to_period_compare,
        show_percentage=show_percentage,
        min_change=min_change,
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
    pay_period: PayPeriods,
    *,
    client: Client,
    ordinal: Union[Unset, None, int] = UNSET,
    from_period: Union[Unset, None, int] = UNSET,
    to_period: Union[Unset, None, int] = UNSET,
    pay_period_compare: Union[Unset, None, PayPeriods] = UNSET,
    ordinal_compare: Union[Unset, None, int] = UNSET,
    tax_year_compare: Union[Unset, None, TaxYear] = UNSET,
    from_period_compare: Union[Unset, None, int] = UNSET,
    to_period_compare: Union[Unset, None, int] = UNSET,
    show_percentage: Union[Unset, None, bool] = UNSET,
    min_change: Union[Unset, None, float] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Optional[VarianceReportReportResponse]:
    """Variance Report

     Returns a report comparing two pay periods or two ranges of payperiods.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        ordinal (Union[Unset, None, int]):
        from_period (Union[Unset, None, int]):
        to_period (Union[Unset, None, int]):
        pay_period_compare (Union[Unset, None, PayPeriods]):
        ordinal_compare (Union[Unset, None, int]):
        tax_year_compare (Union[Unset, None, TaxYear]):
        from_period_compare (Union[Unset, None, int]):
        to_period_compare (Union[Unset, None, int]):
        show_percentage (Union[Unset, None, bool]):
        min_change (Union[Unset, None, float]):
        accept (Union[Unset, str]):

    Returns:
        Response[VarianceReportReportResponse]
    """

    return sync_detailed(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        client=client,
        ordinal=ordinal,
        from_period=from_period,
        to_period=to_period,
        pay_period_compare=pay_period_compare,
        ordinal_compare=ordinal_compare,
        tax_year_compare=tax_year_compare,
        from_period_compare=from_period_compare,
        to_period_compare=to_period_compare,
        show_percentage=show_percentage,
        min_change=min_change,
        accept=accept,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    *,
    client: Client,
    ordinal: Union[Unset, None, int] = UNSET,
    from_period: Union[Unset, None, int] = UNSET,
    to_period: Union[Unset, None, int] = UNSET,
    pay_period_compare: Union[Unset, None, PayPeriods] = UNSET,
    ordinal_compare: Union[Unset, None, int] = UNSET,
    tax_year_compare: Union[Unset, None, TaxYear] = UNSET,
    from_period_compare: Union[Unset, None, int] = UNSET,
    to_period_compare: Union[Unset, None, int] = UNSET,
    show_percentage: Union[Unset, None, bool] = UNSET,
    min_change: Union[Unset, None, float] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Response[VarianceReportReportResponse]:
    """Variance Report

     Returns a report comparing two pay periods or two ranges of payperiods.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        ordinal (Union[Unset, None, int]):
        from_period (Union[Unset, None, int]):
        to_period (Union[Unset, None, int]):
        pay_period_compare (Union[Unset, None, PayPeriods]):
        ordinal_compare (Union[Unset, None, int]):
        tax_year_compare (Union[Unset, None, TaxYear]):
        from_period_compare (Union[Unset, None, int]):
        to_period_compare (Union[Unset, None, int]):
        show_percentage (Union[Unset, None, bool]):
        min_change (Union[Unset, None, float]):
        accept (Union[Unset, str]):

    Returns:
        Response[VarianceReportReportResponse]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        client=client,
        ordinal=ordinal,
        from_period=from_period,
        to_period=to_period,
        pay_period_compare=pay_period_compare,
        ordinal_compare=ordinal_compare,
        tax_year_compare=tax_year_compare,
        from_period_compare=from_period_compare,
        to_period_compare=to_period_compare,
        show_percentage=show_percentage,
        min_change=min_change,
        accept=accept,
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
    ordinal: Union[Unset, None, int] = UNSET,
    from_period: Union[Unset, None, int] = UNSET,
    to_period: Union[Unset, None, int] = UNSET,
    pay_period_compare: Union[Unset, None, PayPeriods] = UNSET,
    ordinal_compare: Union[Unset, None, int] = UNSET,
    tax_year_compare: Union[Unset, None, TaxYear] = UNSET,
    from_period_compare: Union[Unset, None, int] = UNSET,
    to_period_compare: Union[Unset, None, int] = UNSET,
    show_percentage: Union[Unset, None, bool] = UNSET,
    min_change: Union[Unset, None, float] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Optional[VarianceReportReportResponse]:
    """Variance Report

     Returns a report comparing two pay periods or two ranges of payperiods.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        ordinal (Union[Unset, None, int]):
        from_period (Union[Unset, None, int]):
        to_period (Union[Unset, None, int]):
        pay_period_compare (Union[Unset, None, PayPeriods]):
        ordinal_compare (Union[Unset, None, int]):
        tax_year_compare (Union[Unset, None, TaxYear]):
        from_period_compare (Union[Unset, None, int]):
        to_period_compare (Union[Unset, None, int]):
        show_percentage (Union[Unset, None, bool]):
        min_change (Union[Unset, None, float]):
        accept (Union[Unset, str]):

    Returns:
        Response[VarianceReportReportResponse]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            tax_year=tax_year,
            pay_period=pay_period,
            client=client,
            ordinal=ordinal,
            from_period=from_period,
            to_period=to_period,
            pay_period_compare=pay_period_compare,
            ordinal_compare=ordinal_compare,
            tax_year_compare=tax_year_compare,
            from_period_compare=from_period_compare,
            to_period_compare=to_period_compare,
            show_percentage=show_percentage,
            min_change=min_change,
            accept=accept,
        )
    ).parsed
