from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.tenant import Tenant
from ...types import Response


def _get_kwargs(
    brand_code: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/engine/branding/{brandCode}".format(client.base_url, brandCode=brand_code)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
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
    brand_code: str,
    *,
    client: Client,
) -> Response[Tenant]:
    """Tenant Branding

     Returns Tenant Branding. Not for public use, will return 401

    Args:
        brand_code (str):

    Returns:
        Response[Tenant]
    """

    kwargs = _get_kwargs(
        brand_code=brand_code,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    brand_code: str,
    *,
    client: Client,
) -> Optional[Tenant]:
    """Tenant Branding

     Returns Tenant Branding. Not for public use, will return 401

    Args:
        brand_code (str):

    Returns:
        Response[Tenant]
    """

    return sync_detailed(
        brand_code=brand_code,
        client=client,
    ).parsed


async def asyncio_detailed(
    brand_code: str,
    *,
    client: Client,
) -> Response[Tenant]:
    """Tenant Branding

     Returns Tenant Branding. Not for public use, will return 401

    Args:
        brand_code (str):

    Returns:
        Response[Tenant]
    """

    kwargs = _get_kwargs(
        brand_code=brand_code,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    brand_code: str,
    *,
    client: Client,
) -> Optional[Tenant]:
    """Tenant Branding

     Returns Tenant Branding. Not for public use, will return 401

    Args:
        brand_code (str):

    Returns:
        Response[Tenant]
    """

    return (
        await asyncio_detailed(
            brand_code=brand_code,
            client=client,
        )
    ).parsed
