from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.user import User
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    defaults: Union[Unset, None, str] = UNSET,
    defaults_key: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/account".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["defaults"] = defaults

    params["defaultsKey"] = defaults_key

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[User]:
    if response.status_code == 200:
        response_200 = User.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[User]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    defaults: Union[Unset, None, str] = UNSET,
    defaults_key: Union[Unset, None, str] = UNSET,
) -> Response[User]:
    """Get Account Details

     Returns the details for the authorised account.

    Args:
        defaults (Union[Unset, None, str]):
        defaults_key (Union[Unset, None, str]):

    Returns:
        Response[User]
    """

    kwargs = _get_kwargs(
        client=client,
        defaults=defaults,
        defaults_key=defaults_key,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    defaults: Union[Unset, None, str] = UNSET,
    defaults_key: Union[Unset, None, str] = UNSET,
) -> Optional[User]:
    """Get Account Details

     Returns the details for the authorised account.

    Args:
        defaults (Union[Unset, None, str]):
        defaults_key (Union[Unset, None, str]):

    Returns:
        Response[User]
    """

    return sync_detailed(
        client=client,
        defaults=defaults,
        defaults_key=defaults_key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    defaults: Union[Unset, None, str] = UNSET,
    defaults_key: Union[Unset, None, str] = UNSET,
) -> Response[User]:
    """Get Account Details

     Returns the details for the authorised account.

    Args:
        defaults (Union[Unset, None, str]):
        defaults_key (Union[Unset, None, str]):

    Returns:
        Response[User]
    """

    kwargs = _get_kwargs(
        client=client,
        defaults=defaults,
        defaults_key=defaults_key,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    defaults: Union[Unset, None, str] = UNSET,
    defaults_key: Union[Unset, None, str] = UNSET,
) -> Optional[User]:
    """Get Account Details

     Returns the details for the authorised account.

    Args:
        defaults (Union[Unset, None, str]):
        defaults_key (Union[Unset, None, str]):

    Returns:
        Response[User]
    """

    return (
        await asyncio_detailed(
            client=client,
            defaults=defaults,
            defaults_key=defaults_key,
        )
    ).parsed
