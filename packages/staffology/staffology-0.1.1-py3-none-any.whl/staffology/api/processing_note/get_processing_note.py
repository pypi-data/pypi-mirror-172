from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.pay_periods import PayPeriods
from ...models.processing_note import ProcessingNote
from ...models.tax_year import TaxYear
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    id: str,
    *,
    client: Client,
    ordinal: Union[Unset, None, int] = 1,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/payrun/{taxYear}/{payPeriod}/{periodNumber}/processingnotes/{id}".format(
        client.base_url,
        employerId=employer_id,
        taxYear=tax_year,
        payPeriod=pay_period,
        periodNumber=period_number,
        id=id,
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
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


def _parse_response(*, response: httpx.Response) -> Optional[ProcessingNote]:
    if response.status_code == 200:
        response_200 = ProcessingNote.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[ProcessingNote]:
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
    period_number: int,
    id: str,
    *,
    client: Client,
    ordinal: Union[Unset, None, int] = 1,
) -> Response[ProcessingNote]:
    """Get a ProcessingNote

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        id (str):
        ordinal (Union[Unset, None, int]):  Default: 1.

    Returns:
        Response[ProcessingNote]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        id=id,
        client=client,
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
    period_number: int,
    id: str,
    *,
    client: Client,
    ordinal: Union[Unset, None, int] = 1,
) -> Optional[ProcessingNote]:
    """Get a ProcessingNote

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        id (str):
        ordinal (Union[Unset, None, int]):  Default: 1.

    Returns:
        Response[ProcessingNote]
    """

    return sync_detailed(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        id=id,
        client=client,
        ordinal=ordinal,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    id: str,
    *,
    client: Client,
    ordinal: Union[Unset, None, int] = 1,
) -> Response[ProcessingNote]:
    """Get a ProcessingNote

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        id (str):
        ordinal (Union[Unset, None, int]):  Default: 1.

    Returns:
        Response[ProcessingNote]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        id=id,
        client=client,
        ordinal=ordinal,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    id: str,
    *,
    client: Client,
    ordinal: Union[Unset, None, int] = 1,
) -> Optional[ProcessingNote]:
    """Get a ProcessingNote

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        id (str):
        ordinal (Union[Unset, None, int]):  Default: 1.

    Returns:
        Response[ProcessingNote]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            tax_year=tax_year,
            pay_period=pay_period,
            period_number=period_number,
            id=id,
            client=client,
            ordinal=ordinal,
        )
    ).parsed
