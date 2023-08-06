from typing import Any, Dict, List, Optional

import httpx

from ...client import Client
from ...models.string_string_key_value_pair import StringStringKeyValuePair
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    client: Client,
    json_body: List[StringStringKeyValuePair],
) -> Dict[str, Any]:
    url = "{}/tenants/{id}/css/colors".format(client.base_url, id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = []
    for json_body_item_data in json_body:
        json_body_item = json_body_item_data.to_dict()

        json_json_body.append(json_body_item)

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[List[StringStringKeyValuePair]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = StringStringKeyValuePair.from_dict(
                response_200_item_data
            )

            response_200.append(response_200_item)

        return response_200
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[List[StringStringKeyValuePair]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: Client,
    json_body: List[StringStringKeyValuePair],
) -> Response[List[StringStringKeyValuePair]]:
    """Update CSS Colors

     Update the colors for a Tenant

    Args:
        id (str):
        json_body (List[StringStringKeyValuePair]):

    Returns:
        Response[List[StringStringKeyValuePair]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    id: str,
    *,
    client: Client,
    json_body: List[StringStringKeyValuePair],
) -> Optional[List[StringStringKeyValuePair]]:
    """Update CSS Colors

     Update the colors for a Tenant

    Args:
        id (str):
        json_body (List[StringStringKeyValuePair]):

    Returns:
        Response[List[StringStringKeyValuePair]]
    """

    return sync_detailed(
        id=id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Client,
    json_body: List[StringStringKeyValuePair],
) -> Response[List[StringStringKeyValuePair]]:
    """Update CSS Colors

     Update the colors for a Tenant

    Args:
        id (str):
        json_body (List[StringStringKeyValuePair]):

    Returns:
        Response[List[StringStringKeyValuePair]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    id: str,
    *,
    client: Client,
    json_body: List[StringStringKeyValuePair],
) -> Optional[List[StringStringKeyValuePair]]:
    """Update CSS Colors

     Update the colors for a Tenant

    Args:
        id (str):
        json_body (List[StringStringKeyValuePair]):

    Returns:
        Response[List[StringStringKeyValuePair]]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            json_body=json_body,
        )
    ).parsed
