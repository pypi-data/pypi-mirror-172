import datetime
from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.tax_year import TaxYear
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    id: str,
    tax_year: TaxYear,
    *,
    client: Client,
    date: Union[Unset, None, datetime.datetime] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/employees/{id}/{taxYear}/minimum-wage".format(
        client.base_url, employerId=employer_id, id=id, taxYear=tax_year
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_date: Union[Unset, None, str] = UNSET
    if not isinstance(date, Unset):
        json_date = date.isoformat() if date else None

    params["date"] = json_date

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
    employer_id: str,
    id: str,
    tax_year: TaxYear,
    *,
    client: Client,
    date: Union[Unset, None, datetime.datetime] = UNSET,
) -> Response[float]:
    """Minimum Wage

     Calculates the National Minimum Wage for this employee for the given TaxYear and based on
    their age at the given date

    Args:
        employer_id (str):
        id (str):
        tax_year (TaxYear):
        date (Union[Unset, None, datetime.datetime]):

    Returns:
        Response[float]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        tax_year=tax_year,
        client=client,
        date=date,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    employer_id: str,
    id: str,
    tax_year: TaxYear,
    *,
    client: Client,
    date: Union[Unset, None, datetime.datetime] = UNSET,
) -> Optional[float]:
    """Minimum Wage

     Calculates the National Minimum Wage for this employee for the given TaxYear and based on
    their age at the given date

    Args:
        employer_id (str):
        id (str):
        tax_year (TaxYear):
        date (Union[Unset, None, datetime.datetime]):

    Returns:
        Response[float]
    """

    return sync_detailed(
        employer_id=employer_id,
        id=id,
        tax_year=tax_year,
        client=client,
        date=date,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    id: str,
    tax_year: TaxYear,
    *,
    client: Client,
    date: Union[Unset, None, datetime.datetime] = UNSET,
) -> Response[float]:
    """Minimum Wage

     Calculates the National Minimum Wage for this employee for the given TaxYear and based on
    their age at the given date

    Args:
        employer_id (str):
        id (str):
        tax_year (TaxYear):
        date (Union[Unset, None, datetime.datetime]):

    Returns:
        Response[float]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        tax_year=tax_year,
        client=client,
        date=date,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    id: str,
    tax_year: TaxYear,
    *,
    client: Client,
    date: Union[Unset, None, datetime.datetime] = UNSET,
) -> Optional[float]:
    """Minimum Wage

     Calculates the National Minimum Wage for this employee for the given TaxYear and based on
    their age at the given date

    Args:
        employer_id (str):
        id (str):
        tax_year (TaxYear):
        date (Union[Unset, None, datetime.datetime]):

    Returns:
        Response[float]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            id=id,
            tax_year=tax_year,
            client=client,
            date=date,
        )
    ).parsed
