from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.tenant import Tenant
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    tenant_id: Union[Unset, None, str] = UNSET,
    key: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/account/Tenant".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["tenantId"] = tenant_id

    params["key"] = key

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Tenant]:
    if response.status_code == 200:
        response_200 = Tenant.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Tenant]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    tenant_id: Union[Unset, None, str] = UNSET,
    key: Union[Unset, None, str] = UNSET,
) -> Response[Tenant]:
    """Get Tenant

     Returns branding details for the specified tenant. This is used by the web app and is unlikely to be
    used by third-parties.

    Args:
        tenant_id (Union[Unset, None, str]):
        key (Union[Unset, None, str]):

    Returns:
        Response[Tenant]
    """

    kwargs = _get_kwargs(
        client=client,
        tenant_id=tenant_id,
        key=key,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    tenant_id: Union[Unset, None, str] = UNSET,
    key: Union[Unset, None, str] = UNSET,
) -> Optional[Tenant]:
    """Get Tenant

     Returns branding details for the specified tenant. This is used by the web app and is unlikely to be
    used by third-parties.

    Args:
        tenant_id (Union[Unset, None, str]):
        key (Union[Unset, None, str]):

    Returns:
        Response[Tenant]
    """

    return sync_detailed(
        client=client,
        tenant_id=tenant_id,
        key=key,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    tenant_id: Union[Unset, None, str] = UNSET,
    key: Union[Unset, None, str] = UNSET,
) -> Response[Tenant]:
    """Get Tenant

     Returns branding details for the specified tenant. This is used by the web app and is unlikely to be
    used by third-parties.

    Args:
        tenant_id (Union[Unset, None, str]):
        key (Union[Unset, None, str]):

    Returns:
        Response[Tenant]
    """

    kwargs = _get_kwargs(
        client=client,
        tenant_id=tenant_id,
        key=key,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    tenant_id: Union[Unset, None, str] = UNSET,
    key: Union[Unset, None, str] = UNSET,
) -> Optional[Tenant]:
    """Get Tenant

     Returns branding details for the specified tenant. This is used by the web app and is unlikely to be
    used by third-parties.

    Args:
        tenant_id (Union[Unset, None, str]):
        key (Union[Unset, None, str]):

    Returns:
        Response[Tenant]
    """

    return (
        await asyncio_detailed(
            client=client,
            tenant_id=tenant_id,
            key=key,
        )
    ).parsed
