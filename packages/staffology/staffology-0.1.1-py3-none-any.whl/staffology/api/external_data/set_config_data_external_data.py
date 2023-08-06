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
    json_body: Any,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/external-data/{id}/config".format(
        client.base_url, employerId=employer_id, id=id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
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
    json_body: Any,
) -> Response[Any]:
    """Set Config Data

     Sets the additional configuration data for the connection to the ExternalDataProvider.
    Only the value set in the userData field is updated

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        json_body (Any):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        client=client,
        json_body=json_body,
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
    json_body: Any,
) -> Response[Any]:
    """Set Config Data

     Sets the additional configuration data for the connection to the ExternalDataProvider.
    Only the value set in the userData field is updated

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        json_body (Any):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
