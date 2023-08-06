from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import Client
from ...models.item import Item
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    month: Union[Unset, None, int] = UNSET,
    year: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    url = "{}/tenants/bills".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["month"] = month

    params["year"] = year

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, List[Item]]]:
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 401:
        response_401 = cast(Any, None)
        return response_401
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, List[Item]]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    month: Union[Unset, None, int] = UNSET,
    year: Union[Unset, None, int] = UNSET,
) -> Response[Union[Any, List[Item]]]:
    """Create Bills for Period

     Generates usage and creates bills for all Tenants
    Only available to SuperAdmins

    Args:
        month (Union[Unset, None, int]):
        year (Union[Unset, None, int]):

    Returns:
        Response[Union[Any, List[Item]]]
    """

    kwargs = _get_kwargs(
        client=client,
        month=month,
        year=year,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    month: Union[Unset, None, int] = UNSET,
    year: Union[Unset, None, int] = UNSET,
) -> Optional[Union[Any, List[Item]]]:
    """Create Bills for Period

     Generates usage and creates bills for all Tenants
    Only available to SuperAdmins

    Args:
        month (Union[Unset, None, int]):
        year (Union[Unset, None, int]):

    Returns:
        Response[Union[Any, List[Item]]]
    """

    return sync_detailed(
        client=client,
        month=month,
        year=year,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    month: Union[Unset, None, int] = UNSET,
    year: Union[Unset, None, int] = UNSET,
) -> Response[Union[Any, List[Item]]]:
    """Create Bills for Period

     Generates usage and creates bills for all Tenants
    Only available to SuperAdmins

    Args:
        month (Union[Unset, None, int]):
        year (Union[Unset, None, int]):

    Returns:
        Response[Union[Any, List[Item]]]
    """

    kwargs = _get_kwargs(
        client=client,
        month=month,
        year=year,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    month: Union[Unset, None, int] = UNSET,
    year: Union[Unset, None, int] = UNSET,
) -> Optional[Union[Any, List[Item]]]:
    """Create Bills for Period

     Generates usage and creates bills for all Tenants
    Only available to SuperAdmins

    Args:
        month (Union[Unset, None, int]):
        year (Union[Unset, None, int]):

    Returns:
        Response[Union[Any, List[Item]]]
    """

    return (
        await asyncio_detailed(
            client=client,
            month=month,
            year=year,
        )
    ).parsed
