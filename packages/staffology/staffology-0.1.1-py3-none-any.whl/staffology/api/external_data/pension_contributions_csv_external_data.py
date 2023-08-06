from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.external_data_provider_id import ExternalDataProviderId
from ...models.pay_periods import PayPeriods
from ...models.tax_year import TaxYear
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    id: ExternalDataProviderId,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    scheme_id: Union[Unset, None, str] = UNSET,
    ordinal: Union[Unset, None, int] = 1,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/external-data/{id}/contributions/{taxYear}/{payPeriod}/{periodNumber}".format(
        client.base_url,
        employerId=employer_id,
        id=id,
        taxYear=tax_year,
        payPeriod=pay_period,
        periodNumber=period_number,
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["schemeId"] = scheme_id

    params["ordinal"] = ordinal

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[str]:
    if response.status_code == 200:
        response_200 = cast(str, response.json())
        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[str]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    id: ExternalDataProviderId,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    scheme_id: Union[Unset, None, str] = UNSET,
    ordinal: Union[Unset, None, int] = 1,
) -> Response[str]:
    """Contributions CSV File

     Returns a CSV file containing contributions for the specified payrun in a format specific to the
    ExternalDataProvider

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        scheme_id (Union[Unset, None, str]):
        ordinal (Union[Unset, None, int]):  Default: 1.

    Returns:
        Response[str]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        client=client,
        scheme_id=scheme_id,
        ordinal=ordinal,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    employer_id: str,
    id: ExternalDataProviderId,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    scheme_id: Union[Unset, None, str] = UNSET,
    ordinal: Union[Unset, None, int] = 1,
) -> Optional[str]:
    """Contributions CSV File

     Returns a CSV file containing contributions for the specified payrun in a format specific to the
    ExternalDataProvider

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        scheme_id (Union[Unset, None, str]):
        ordinal (Union[Unset, None, int]):  Default: 1.

    Returns:
        Response[str]
    """

    return sync_detailed(
        employer_id=employer_id,
        id=id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        client=client,
        scheme_id=scheme_id,
        ordinal=ordinal,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    id: ExternalDataProviderId,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    scheme_id: Union[Unset, None, str] = UNSET,
    ordinal: Union[Unset, None, int] = 1,
) -> Response[str]:
    """Contributions CSV File

     Returns a CSV file containing contributions for the specified payrun in a format specific to the
    ExternalDataProvider

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        scheme_id (Union[Unset, None, str]):
        ordinal (Union[Unset, None, int]):  Default: 1.

    Returns:
        Response[str]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        client=client,
        scheme_id=scheme_id,
        ordinal=ordinal,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    id: ExternalDataProviderId,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    scheme_id: Union[Unset, None, str] = UNSET,
    ordinal: Union[Unset, None, int] = 1,
) -> Optional[str]:
    """Contributions CSV File

     Returns a CSV file containing contributions for the specified payrun in a format specific to the
    ExternalDataProvider

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        scheme_id (Union[Unset, None, str]):
        ordinal (Union[Unset, None, int]):  Default: 1.

    Returns:
        Response[str]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            id=id,
            tax_year=tax_year,
            pay_period=pay_period,
            period_number=period_number,
            client=client,
            scheme_id=scheme_id,
            ordinal=ordinal,
        )
    ).parsed
