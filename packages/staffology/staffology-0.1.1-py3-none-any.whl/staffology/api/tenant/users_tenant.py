from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.item import Item
from ...models.user_category import UserCategory
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    client: Client,
    page_num: Union[Unset, None, int] = UNSET,
    page_size: Union[Unset, None, int] = UNSET,
    sort_by_last_login: Union[Unset, None, bool] = False,
    category: Union[Unset, None, UserCategory] = UNSET,
) -> Dict[str, Any]:
    url = "{}/tenants/{id}/users".format(client.base_url, id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["pageNum"] = page_num

    params["pageSize"] = page_size

    params["sortByLastLogin"] = sort_by_last_login

    json_category: Union[Unset, None, str] = UNSET
    if not isinstance(category, Unset):
        json_category = category.value if category else None

    params["category"] = json_category

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
    page_num: Union[Unset, None, int] = UNSET,
    page_size: Union[Unset, None, int] = UNSET,
    sort_by_last_login: Union[Unset, None, bool] = False,
    category: Union[Unset, None, UserCategory] = UNSET,
) -> Response[List[Item]]:
    """List Users

     Returns a list of users for the Tenant

    Args:
        id (str):
        page_num (Union[Unset, None, int]):
        page_size (Union[Unset, None, int]):
        sort_by_last_login (Union[Unset, None, bool]):
        category (Union[Unset, None, UserCategory]):

    Returns:
        Response[List[Item]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        page_num=page_num,
        page_size=page_size,
        sort_by_last_login=sort_by_last_login,
        category=category,
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
    page_num: Union[Unset, None, int] = UNSET,
    page_size: Union[Unset, None, int] = UNSET,
    sort_by_last_login: Union[Unset, None, bool] = False,
    category: Union[Unset, None, UserCategory] = UNSET,
) -> Optional[List[Item]]:
    """List Users

     Returns a list of users for the Tenant

    Args:
        id (str):
        page_num (Union[Unset, None, int]):
        page_size (Union[Unset, None, int]):
        sort_by_last_login (Union[Unset, None, bool]):
        category (Union[Unset, None, UserCategory]):

    Returns:
        Response[List[Item]]
    """

    return sync_detailed(
        id=id,
        client=client,
        page_num=page_num,
        page_size=page_size,
        sort_by_last_login=sort_by_last_login,
        category=category,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Client,
    page_num: Union[Unset, None, int] = UNSET,
    page_size: Union[Unset, None, int] = UNSET,
    sort_by_last_login: Union[Unset, None, bool] = False,
    category: Union[Unset, None, UserCategory] = UNSET,
) -> Response[List[Item]]:
    """List Users

     Returns a list of users for the Tenant

    Args:
        id (str):
        page_num (Union[Unset, None, int]):
        page_size (Union[Unset, None, int]):
        sort_by_last_login (Union[Unset, None, bool]):
        category (Union[Unset, None, UserCategory]):

    Returns:
        Response[List[Item]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        page_num=page_num,
        page_size=page_size,
        sort_by_last_login=sort_by_last_login,
        category=category,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    id: str,
    *,
    client: Client,
    page_num: Union[Unset, None, int] = UNSET,
    page_size: Union[Unset, None, int] = UNSET,
    sort_by_last_login: Union[Unset, None, bool] = False,
    category: Union[Unset, None, UserCategory] = UNSET,
) -> Optional[List[Item]]:
    """List Users

     Returns a list of users for the Tenant

    Args:
        id (str):
        page_num (Union[Unset, None, int]):
        page_size (Union[Unset, None, int]):
        sort_by_last_login (Union[Unset, None, bool]):
        category (Union[Unset, None, UserCategory]):

    Returns:
        Response[List[Item]]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            page_num=page_num,
            page_size=page_size,
            sort_by_last_login=sort_by_last_login,
            category=category,
        )
    ).parsed
