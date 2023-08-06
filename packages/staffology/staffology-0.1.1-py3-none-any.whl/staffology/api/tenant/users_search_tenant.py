from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.item import Item
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    client: Client,
    q: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/tenants/{id}/users/search".format(client.base_url, id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["q"] = q

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[List[Item]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[List[Item]]:
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
    q: Union[Unset, None, str] = UNSET,
) -> Response[List[Item]]:
    """Search Users

     Returns a list of users for the Tenant that match the search

    Args:
        id (str):
        q (Union[Unset, None, str]):

    Returns:
        Response[List[Item]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        q=q,
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
    q: Union[Unset, None, str] = UNSET,
) -> Optional[List[Item]]:
    """Search Users

     Returns a list of users for the Tenant that match the search

    Args:
        id (str):
        q (Union[Unset, None, str]):

    Returns:
        Response[List[Item]]
    """

    return sync_detailed(
        id=id,
        client=client,
        q=q,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Client,
    q: Union[Unset, None, str] = UNSET,
) -> Response[List[Item]]:
    """Search Users

     Returns a list of users for the Tenant that match the search

    Args:
        id (str):
        q (Union[Unset, None, str]):

    Returns:
        Response[List[Item]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        q=q,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    id: str,
    *,
    client: Client,
    q: Union[Unset, None, str] = UNSET,
) -> Optional[List[Item]]:
    """Search Users

     Returns a list of users for the Tenant that match the search

    Args:
        id (str):
        q (Union[Unset, None, str]):

    Returns:
        Response[List[Item]]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            q=q,
        )
    ).parsed
