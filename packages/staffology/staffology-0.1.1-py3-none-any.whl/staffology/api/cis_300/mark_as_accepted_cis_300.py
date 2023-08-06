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
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/rti/cis300/{taxYear}/{id}/markasaccepted".format(
        client.base_url, employerId=employer_id, taxYear=tax_year, id=id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
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
) -> Response[Cis300]:
    """Mark as Sent

     Marks a Cis300 as having been sent to HMRC and accepted by them
    You only use this method if the request has been submitted via an external system.
    It will automatically be updated as Sent and/or Accepted if it's submitted via this API.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        id (str):

    Returns:
        Response[Cis300]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        id=id,
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
    id: str,
    *,
    client: Client,
) -> Optional[Cis300]:
    """Mark as Sent

     Marks a Cis300 as having been sent to HMRC and accepted by them
    You only use this method if the request has been submitted via an external system.
    It will automatically be updated as Sent and/or Accepted if it's submitted via this API.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        id (str):

    Returns:
        Response[Cis300]
    """

    return sync_detailed(
        employer_id=employer_id,
        tax_year=tax_year,
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    tax_year: TaxYear,
    id: str,
    *,
    client: Client,
) -> Response[Cis300]:
    """Mark as Sent

     Marks a Cis300 as having been sent to HMRC and accepted by them
    You only use this method if the request has been submitted via an external system.
    It will automatically be updated as Sent and/or Accepted if it's submitted via this API.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        id (str):

    Returns:
        Response[Cis300]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        id=id,
        client=client,
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
) -> Optional[Cis300]:
    """Mark as Sent

     Marks a Cis300 as having been sent to HMRC and accepted by them
    You only use this method if the request has been submitted via an external system.
    It will automatically be updated as Sent and/or Accepted if it's submitted via this API.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        id (str):

    Returns:
        Response[Cis300]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            tax_year=tax_year,
            id=id,
            client=client,
        )
    ).parsed
