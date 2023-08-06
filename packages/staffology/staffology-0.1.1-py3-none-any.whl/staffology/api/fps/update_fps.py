from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.fps import Fps
from ...models.tax_year import TaxYear
from ...types import Response


def _get_kwargs(
    employer_id: str,
    tax_year: TaxYear,
    id: str,
    *,
    client: Client,
    json_body: Fps,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/rti/fps/{taxYear}/{id}".format(
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


def _parse_response(*, response: httpx.Response) -> Optional[Fps]:
    if response.status_code == 200:
        response_200 = Fps.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Fps]:
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
    json_body: Fps,
) -> Response[Fps]:
    """Update FPS

     Updates an existing Full Payment Submission.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        id (str):
        json_body (Fps):

    Returns:
        Response[Fps]
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
    json_body: Fps,
) -> Optional[Fps]:
    """Update FPS

     Updates an existing Full Payment Submission.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        id (str):
        json_body (Fps):

    Returns:
        Response[Fps]
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
    json_body: Fps,
) -> Response[Fps]:
    """Update FPS

     Updates an existing Full Payment Submission.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        id (str):
        json_body (Fps):

    Returns:
        Response[Fps]
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
    json_body: Fps,
) -> Optional[Fps]:
    """Update FPS

     Updates an existing Full Payment Submission.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        id (str):
        json_body (Fps):

    Returns:
        Response[Fps]
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
