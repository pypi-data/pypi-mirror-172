from typing import Any, Dict

import httpx

from ...client import Client
from ...models.external_data_provider_id import ExternalDataProviderId
from ...types import Response


def _get_kwargs(
    employer_id: str,
    id: ExternalDataProviderId,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/external-data/{id}/config".format(
        client.base_url, employerId=employer_id, id=id
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
) -> Response[Any]:
    """Get Config Data

     Returns any additional configuration data for the connection to the ExternalDataProvider.

    Args:
        employer_id (str):
        id (ExternalDataProviderId):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        client=client,
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
) -> Response[Any]:
    """Get Config Data

     Returns any additional configuration data for the connection to the ExternalDataProvider.

    Args:
        employer_id (str):
        id (ExternalDataProviderId):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
