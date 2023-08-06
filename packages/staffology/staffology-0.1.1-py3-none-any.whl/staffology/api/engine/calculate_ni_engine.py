from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.national_insurance_calculation import NationalInsuranceCalculation
from ...models.pay_periods import PayPeriods
from ...models.tax_year import TaxYear
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    tax_year: Union[Unset, None, TaxYear] = UNSET,
    gross: Union[Unset, None, float] = UNSET,
    ni_category: Union[Unset, None, str] = UNSET,
    pay_period: Union[Unset, None, PayPeriods] = UNSET,
) -> Dict[str, Any]:
    url = "{}/engine/ni".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_tax_year: Union[Unset, None, str] = UNSET
    if not isinstance(tax_year, Unset):
        json_tax_year = tax_year.value if tax_year else None

    params["taxYear"] = json_tax_year

    params["gross"] = gross

    params["niCategory"] = ni_category

    json_pay_period: Union[Unset, None, str] = UNSET
    if not isinstance(pay_period, Unset):
        json_pay_period = pay_period.value if pay_period else None

    params["payPeriod"] = json_pay_period

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
) -> Optional[NationalInsuranceCalculation]:
    if response.status_code == 200:
        response_200 = NationalInsuranceCalculation.from_dict(response.json())

        return response_200
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[NationalInsuranceCalculation]:
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
    gross: Union[Unset, None, float] = UNSET,
    ni_category: Union[Unset, None, str] = UNSET,
    pay_period: Union[Unset, None, PayPeriods] = UNSET,
) -> Response[NationalInsuranceCalculation]:
    """Calculate NI due.

     Calculates National Insurance Contributions due given the values specified.
    You would never need to use this API call in practice. It is provided just for information and
    testing purposes.
    Access is limited so you'll probably receive a 401 response if you try to use it.

    Args:
        tax_year (Union[Unset, None, TaxYear]):
        gross (Union[Unset, None, float]):
        ni_category (Union[Unset, None, str]):
        pay_period (Union[Unset, None, PayPeriods]):

    Returns:
        Response[NationalInsuranceCalculation]
    """

    kwargs = _get_kwargs(
        client=client,
        tax_year=tax_year,
        gross=gross,
        ni_category=ni_category,
        pay_period=pay_period,
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
    gross: Union[Unset, None, float] = UNSET,
    ni_category: Union[Unset, None, str] = UNSET,
    pay_period: Union[Unset, None, PayPeriods] = UNSET,
) -> Optional[NationalInsuranceCalculation]:
    """Calculate NI due.

     Calculates National Insurance Contributions due given the values specified.
    You would never need to use this API call in practice. It is provided just for information and
    testing purposes.
    Access is limited so you'll probably receive a 401 response if you try to use it.

    Args:
        tax_year (Union[Unset, None, TaxYear]):
        gross (Union[Unset, None, float]):
        ni_category (Union[Unset, None, str]):
        pay_period (Union[Unset, None, PayPeriods]):

    Returns:
        Response[NationalInsuranceCalculation]
    """

    return sync_detailed(
        client=client,
        tax_year=tax_year,
        gross=gross,
        ni_category=ni_category,
        pay_period=pay_period,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    tax_year: Union[Unset, None, TaxYear] = UNSET,
    gross: Union[Unset, None, float] = UNSET,
    ni_category: Union[Unset, None, str] = UNSET,
    pay_period: Union[Unset, None, PayPeriods] = UNSET,
) -> Response[NationalInsuranceCalculation]:
    """Calculate NI due.

     Calculates National Insurance Contributions due given the values specified.
    You would never need to use this API call in practice. It is provided just for information and
    testing purposes.
    Access is limited so you'll probably receive a 401 response if you try to use it.

    Args:
        tax_year (Union[Unset, None, TaxYear]):
        gross (Union[Unset, None, float]):
        ni_category (Union[Unset, None, str]):
        pay_period (Union[Unset, None, PayPeriods]):

    Returns:
        Response[NationalInsuranceCalculation]
    """

    kwargs = _get_kwargs(
        client=client,
        tax_year=tax_year,
        gross=gross,
        ni_category=ni_category,
        pay_period=pay_period,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    tax_year: Union[Unset, None, TaxYear] = UNSET,
    gross: Union[Unset, None, float] = UNSET,
    ni_category: Union[Unset, None, str] = UNSET,
    pay_period: Union[Unset, None, PayPeriods] = UNSET,
) -> Optional[NationalInsuranceCalculation]:
    """Calculate NI due.

     Calculates National Insurance Contributions due given the values specified.
    You would never need to use this API call in practice. It is provided just for information and
    testing purposes.
    Access is limited so you'll probably receive a 401 response if you try to use it.

    Args:
        tax_year (Union[Unset, None, TaxYear]):
        gross (Union[Unset, None, float]):
        ni_category (Union[Unset, None, str]):
        pay_period (Union[Unset, None, PayPeriods]):

    Returns:
        Response[NationalInsuranceCalculation]
    """

    return (
        await asyncio_detailed(
            client=client,
            tax_year=tax_year,
            gross=gross,
            ni_category=ni_category,
            pay_period=pay_period,
        )
    ).parsed
