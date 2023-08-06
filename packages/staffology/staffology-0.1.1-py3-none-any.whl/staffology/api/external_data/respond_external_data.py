from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...models.external_data_provider_id import ExternalDataProviderId
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: ExternalDataProviderId,
    *,
    client: Client,
    error: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/external-data/{id}/respond".format(client.base_url, id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["error"] = error

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
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
    id: ExternalDataProviderId,
    *,
    client: Client,
    error: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """3rd Party Response

     This endpoint is used by third parties to respond to an oAuth authorization request. You do not need
    to use this

    Args:
        id (ExternalDataProviderId):
        error (Union[Unset, None, str]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        error=error,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    id: ExternalDataProviderId,
    *,
    client: Client,
    error: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """3rd Party Response

     This endpoint is used by third parties to respond to an oAuth authorization request. You do not need
    to use this

    Args:
        id (ExternalDataProviderId):
        error (Union[Unset, None, str]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        error=error,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
