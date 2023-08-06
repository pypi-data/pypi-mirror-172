from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import Client
from ...models.item import Item
from ...types import Response


def _get_kwargs(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/employees/{employeeId}/posts".format(
        client.base_url, employerId=employer_id, employeeId=employee_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, List[Item]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, List[Item]]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
) -> Response[Union[Any, List[Item]]]:
    """List Posts

     Lists all Posts for an Employee.
    You must have the multi-post feature enabled.
    This endpoint is currently being beta tested and subject to un-announced breaking changes.

    Args:
        employer_id (str):
        employee_id (str):

    Returns:
        Response[Union[Any, List[Item]]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
) -> Optional[Union[Any, List[Item]]]:
    """List Posts

     Lists all Posts for an Employee.
    You must have the multi-post feature enabled.
    This endpoint is currently being beta tested and subject to un-announced breaking changes.

    Args:
        employer_id (str):
        employee_id (str):

    Returns:
        Response[Union[Any, List[Item]]]
    """

    return sync_detailed(
        employer_id=employer_id,
        employee_id=employee_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
) -> Response[Union[Any, List[Item]]]:
    """List Posts

     Lists all Posts for an Employee.
    You must have the multi-post feature enabled.
    This endpoint is currently being beta tested and subject to un-announced breaking changes.

    Args:
        employer_id (str):
        employee_id (str):

    Returns:
        Response[Union[Any, List[Item]]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
) -> Optional[Union[Any, List[Item]]]:
    """List Posts

     Lists all Posts for an Employee.
    You must have the multi-post feature enabled.
    This endpoint is currently being beta tested and subject to un-announced breaking changes.

    Args:
        employer_id (str):
        employee_id (str):

    Returns:
        Response[Union[Any, List[Item]]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            employee_id=employee_id,
            client=client,
        )
    ).parsed
