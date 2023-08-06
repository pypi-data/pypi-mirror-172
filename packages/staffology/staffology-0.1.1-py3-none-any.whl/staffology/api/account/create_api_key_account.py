from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.item import Item
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: Item,
) -> Dict[str, Any]:
    url = "{}/account/keys".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Item]:
    if response.status_code == 201:
        response_201 = Item.from_dict(response.json())

        return response_201
    return None


def _build_response(*, response: httpx.Response) -> Response[Item]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: Item,
) -> Response[Item]:
    """Create ApiKey

     Creates a new APIKey. The only property that's required or used is Name.
    A new ApiKey will be generated and returned to you.

    Args:
        json_body (Item):

    Returns:
        Response[Item]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    json_body: Item,
) -> Optional[Item]:
    """Create ApiKey

     Creates a new APIKey. The only property that's required or used is Name.
    A new ApiKey will be generated and returned to you.

    Args:
        json_body (Item):

    Returns:
        Response[Item]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: Item,
) -> Response[Item]:
    """Create ApiKey

     Creates a new APIKey. The only property that's required or used is Name.
    A new ApiKey will be generated and returned to you.

    Args:
        json_body (Item):

    Returns:
        Response[Item]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    json_body: Item,
) -> Optional[Item]:
    """Create ApiKey

     Creates a new APIKey. The only property that's required or used is Name.
    A new ApiKey will be generated and returned to you.

    Args:
        json_body (Item):

    Returns:
        Response[Item]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
