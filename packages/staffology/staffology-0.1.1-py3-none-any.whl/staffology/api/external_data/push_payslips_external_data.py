from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...models.external_data_provider_id import ExternalDataProviderId
from ...models.pay_periods import PayPeriods
from ...models.tax_year import TaxYear
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    id: ExternalDataProviderId,
    *,
    client: Client,
    pay_period: Union[Unset, None, PayPeriods] = UNSET,
    period_number: Union[Unset, None, int] = UNSET,
    tax_year: Union[Unset, None, TaxYear] = UNSET,
    force: Union[Unset, None, bool] = UNSET,
    ordinal: Union[Unset, None, int] = 1,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/external-data/{id}/payslips".format(
        client.base_url, employerId=employer_id, id=id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_pay_period: Union[Unset, None, str] = UNSET
    if not isinstance(pay_period, Unset):
        json_pay_period = pay_period.value if pay_period else None

    params["payPeriod"] = json_pay_period

    params["periodNumber"] = period_number

    json_tax_year: Union[Unset, None, str] = UNSET
    if not isinstance(tax_year, Unset):
        json_tax_year = tax_year.value if tax_year else None

    params["taxYear"] = json_tax_year

    params["force"] = force

    params["ordinal"] = ordinal

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
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
    id: ExternalDataProviderId,
    *,
    client: Client,
    pay_period: Union[Unset, None, PayPeriods] = UNSET,
    period_number: Union[Unset, None, int] = UNSET,
    tax_year: Union[Unset, None, TaxYear] = UNSET,
    force: Union[Unset, None, bool] = UNSET,
    ordinal: Union[Unset, None, int] = 1,
) -> Response[Any]:
    """Push Payslips

     Push payslips to the ExternalDataProvider.

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        pay_period (Union[Unset, None, PayPeriods]):
        period_number (Union[Unset, None, int]):
        tax_year (Union[Unset, None, TaxYear]):
        force (Union[Unset, None, bool]):
        ordinal (Union[Unset, None, int]):  Default: 1.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        client=client,
        pay_period=pay_period,
        period_number=period_number,
        tax_year=tax_year,
        force=force,
        ordinal=ordinal,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    employer_id: str,
    id: ExternalDataProviderId,
    *,
    client: Client,
    pay_period: Union[Unset, None, PayPeriods] = UNSET,
    period_number: Union[Unset, None, int] = UNSET,
    tax_year: Union[Unset, None, TaxYear] = UNSET,
    force: Union[Unset, None, bool] = UNSET,
    ordinal: Union[Unset, None, int] = 1,
) -> Response[Any]:
    """Push Payslips

     Push payslips to the ExternalDataProvider.

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        pay_period (Union[Unset, None, PayPeriods]):
        period_number (Union[Unset, None, int]):
        tax_year (Union[Unset, None, TaxYear]):
        force (Union[Unset, None, bool]):
        ordinal (Union[Unset, None, int]):  Default: 1.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        client=client,
        pay_period=pay_period,
        period_number=period_number,
        tax_year=tax_year,
        force=force,
        ordinal=ordinal,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
