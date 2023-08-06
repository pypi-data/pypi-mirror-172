from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.cis_300 import Cis300
from ...models.tax_year import TaxYear
from ...types import Response


def _get_kwargs(
    employer_id: str,
    tax_year: TaxYear,
    id: str,
    *,
    client: Client,
    json_body: Cis300,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/rti/cis300/{taxYear}/{id}".format(
        client.base_url, employerId=employer_id, taxYear=tax_year, id=id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Cis300]:
    if response.status_code == 200:
        response_200 = Cis300.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Cis300]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    tax_year: TaxYear,
    id: str,
    *,
    client: Client,
    json_body: Cis300,
) -> Response[Cis300]:
    """Update Cis300

     Updates an existing Cis300.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        id (str):
        json_body (Cis300):

    Returns:
        Response[Cis300]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        id=id,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    employer_id: str,
    tax_year: TaxYear,
    id: str,
    *,
    client: Client,
    json_body: Cis300,
) -> Optional[Cis300]:
    """Update Cis300

     Updates an existing Cis300.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        id (str):
        json_body (Cis300):

    Returns:
        Response[Cis300]
    """

    return sync_detailed(
        employer_id=employer_id,
        tax_year=tax_year,
        id=id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    tax_year: TaxYear,
    id: str,
    *,
    client: Client,
    json_body: Cis300,
) -> Response[Cis300]:
    """Update Cis300

     Updates an existing Cis300.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        id (str):
        json_body (Cis300):

    Returns:
        Response[Cis300]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        id=id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    tax_year: TaxYear,
    id: str,
    *,
    client: Client,
    json_body: Cis300,
) -> Optional[Cis300]:
    """Update Cis300

     Updates an existing Cis300.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        id (str):
        json_body (Cis300):

    Returns:
        Response[Cis300]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            tax_year=tax_year,
            id=id,
            client=client,
            json_body=json_body,
        )
    ).parsed
