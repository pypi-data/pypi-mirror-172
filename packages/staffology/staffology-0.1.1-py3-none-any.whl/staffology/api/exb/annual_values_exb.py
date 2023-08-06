from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.exb import Exb
from ...models.tax_year import TaxYear
from ...types import Response


def _get_kwargs(
    employer_id: str,
    tax_year: TaxYear,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/rti/exb/{taxYear}/values".format(
        client.base_url, employerId=employer_id, taxYear=tax_year
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Exb]:
    if response.status_code == 200:
        response_200 = Exb.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Exb]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    tax_year: TaxYear,
    *,
    client: Client,
) -> Response[Exb]:
    """Annual Values

     Returns an empty Exb showing the number of employees and total benefits for the year provided

    Args:
        employer_id (str):
        tax_year (TaxYear):

    Returns:
        Response[Exb]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    employer_id: str,
    tax_year: TaxYear,
    *,
    client: Client,
) -> Optional[Exb]:
    """Annual Values

     Returns an empty Exb showing the number of employees and total benefits for the year provided

    Args:
        employer_id (str):
        tax_year (TaxYear):

    Returns:
        Response[Exb]
    """

    return sync_detailed(
        employer_id=employer_id,
        tax_year=tax_year,
        client=client,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    tax_year: TaxYear,
    *,
    client: Client,
) -> Response[Exb]:
    """Annual Values

     Returns an empty Exb showing the number of employees and total benefits for the year provided

    Args:
        employer_id (str):
        tax_year (TaxYear):

    Returns:
        Response[Exb]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    tax_year: TaxYear,
    *,
    client: Client,
) -> Optional[Exb]:
    """Annual Values

     Returns an empty Exb showing the number of employees and total benefits for the year provided

    Args:
        employer_id (str):
        tax_year (TaxYear):

    Returns:
        Response[Exb]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            tax_year=tax_year,
            client=client,
        )
    ).parsed
