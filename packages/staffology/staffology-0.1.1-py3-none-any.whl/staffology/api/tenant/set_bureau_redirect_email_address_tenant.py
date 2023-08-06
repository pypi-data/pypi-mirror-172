from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    user_id: str,
    *,
    client: Client,
    email_address: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/tenants/{id}/users/{userId}/bureauredir".format(
        client.base_url, id=id, userId=user_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["emailAddress"] = email_address

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
    email_address: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """Set Bureau Redirect

     Sets or removes the redirect email address for a users Bureau-related notifications

    Args:
        id (str):
        user_id (str):
        email_address (Union[Unset, None, str]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        user_id=user_id,
        client=client,
        email_address=email_address,
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
    email_address: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """Set Bureau Redirect

     Sets or removes the redirect email address for a users Bureau-related notifications

    Args:
        id (str):
        user_id (str):
        email_address (Union[Unset, None, str]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        user_id=user_id,
        client=client,
        email_address=email_address,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
