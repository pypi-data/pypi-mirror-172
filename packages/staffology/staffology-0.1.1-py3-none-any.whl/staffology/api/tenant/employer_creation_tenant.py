from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    user_id: str,
    *,
    client: Client,
    enabled: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    url = "{}/tenants/{id}/users/{userId}/employercreation".format(
        client.base_url, id=id, userId=user_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["enabled"] = enabled

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "put",
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
    id: str,
    user_id: str,
    *,
    client: Client,
    enabled: Union[Unset, None, bool] = UNSET,
) -> Response[Any]:
    """Enable Employer Creation

     Enable (or disable) a user accounts ability to create new employers

    Args:
        id (str):
        user_id (str):
        enabled (Union[Unset, None, bool]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        user_id=user_id,
        client=client,
        enabled=enabled,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    id: str,
    user_id: str,
    *,
    client: Client,
    enabled: Union[Unset, None, bool] = UNSET,
) -> Response[Any]:
    """Enable Employer Creation

     Enable (or disable) a user accounts ability to create new employers

    Args:
        id (str):
        user_id (str):
        enabled (Union[Unset, None, bool]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        user_id=user_id,
        client=client,
        enabled=enabled,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
