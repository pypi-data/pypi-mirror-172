from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    u: Union[Unset, None, str] = UNSET,
    k: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/account/verify/respond".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["u"] = u

    params["k"] = k

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[bool]:
    if response.status_code == 200:
        response_200 = cast(bool, response.json())
        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[bool]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    u: Union[Unset, None, str] = UNSET,
    k: Union[Unset, None, str] = UNSET,
) -> Response[bool]:
    """Verify Email Address

     Used to process the link sent in an email to verify an email address.

    Args:
        u (Union[Unset, None, str]):
        k (Union[Unset, None, str]):

    Returns:
        Response[bool]
    """

    kwargs = _get_kwargs(
        client=client,
        u=u,
        k=k,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    u: Union[Unset, None, str] = UNSET,
    k: Union[Unset, None, str] = UNSET,
) -> Optional[bool]:
    """Verify Email Address

     Used to process the link sent in an email to verify an email address.

    Args:
        u (Union[Unset, None, str]):
        k (Union[Unset, None, str]):

    Returns:
        Response[bool]
    """

    return sync_detailed(
        client=client,
        u=u,
        k=k,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    u: Union[Unset, None, str] = UNSET,
    k: Union[Unset, None, str] = UNSET,
) -> Response[bool]:
    """Verify Email Address

     Used to process the link sent in an email to verify an email address.

    Args:
        u (Union[Unset, None, str]):
        k (Union[Unset, None, str]):

    Returns:
        Response[bool]
    """

    kwargs = _get_kwargs(
        client=client,
        u=u,
        k=k,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    u: Union[Unset, None, str] = UNSET,
    k: Union[Unset, None, str] = UNSET,
) -> Optional[bool]:
    """Verify Email Address

     Used to process the link sent in an email to verify an email address.

    Args:
        u (Union[Unset, None, str]):
        k (Union[Unset, None, str]):

    Returns:
        Response[bool]
    """

    return (
        await asyncio_detailed(
            client=client,
            u=u,
            k=k,
        )
    ).parsed
