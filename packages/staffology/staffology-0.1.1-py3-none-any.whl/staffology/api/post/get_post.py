from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.post import Post
from ...types import Response


def _get_kwargs(
    employer_id: str,
    employee_id: str,
    id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/employees/{employeeId}/posts/{id}".format(
        client.base_url, employerId=employer_id, employeeId=employee_id, id=id
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, Post]]:
    if response.status_code == 200:
        response_200 = Post.from_dict(response.json())

        return response_200
    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, Post]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    employee_id: str,
    id: str,
    *,
    client: Client,
) -> Response[Union[Any, Post]]:
    """Get Post

     Gets the Post specified.
    You must have the multi-post feature enabled.
    This endpoint is currently being beta tested and subject to un-announced breaking changes.

    Args:
        employer_id (str):
        employee_id (str):
        id (str):

    Returns:
        Response[Union[Any, Post]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        id=id,
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
    id: str,
    *,
    client: Client,
) -> Optional[Union[Any, Post]]:
    """Get Post

     Gets the Post specified.
    You must have the multi-post feature enabled.
    This endpoint is currently being beta tested and subject to un-announced breaking changes.

    Args:
        employer_id (str):
        employee_id (str):
        id (str):

    Returns:
        Response[Union[Any, Post]]
    """

    return sync_detailed(
        employer_id=employer_id,
        employee_id=employee_id,
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    employee_id: str,
    id: str,
    *,
    client: Client,
) -> Response[Union[Any, Post]]:
    """Get Post

     Gets the Post specified.
    You must have the multi-post feature enabled.
    This endpoint is currently being beta tested and subject to un-announced breaking changes.

    Args:
        employer_id (str):
        employee_id (str):
        id (str):

    Returns:
        Response[Union[Any, Post]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        id=id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    employee_id: str,
    id: str,
    *,
    client: Client,
) -> Optional[Union[Any, Post]]:
    """Get Post

     Gets the Post specified.
    You must have the multi-post feature enabled.
    This endpoint is currently being beta tested and subject to un-announced breaking changes.

    Args:
        employer_id (str):
        employee_id (str):
        id (str):

    Returns:
        Response[Union[Any, Post]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            employee_id=employee_id,
            id=id,
            client=client,
        )
    ).parsed
