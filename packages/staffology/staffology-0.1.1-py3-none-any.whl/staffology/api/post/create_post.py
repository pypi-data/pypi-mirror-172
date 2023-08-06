from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.post import Post
from ...types import Response


def _get_kwargs(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
    json_body: Post,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/employees/{employeeId}/posts".format(
        client.base_url, employerId=employer_id, employeeId=employee_id
    )

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, Post]]:
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 403:
        response_403 = cast(Any, None)
        return response_403
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == 201:
        response_201 = Post.from_dict(response.json())

        return response_201
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
    *,
    client: Client,
    json_body: Post,
) -> Response[Union[Any, Post]]:
    """Create Post

     Creates a new Post for the Employee.
    You must have the multi-post feature enabled.
    This endpoint is currently being beta tested and subject to un-announced breaking changes.

    Args:
        employer_id (str):
        employee_id (str):
        json_body (Post):

    Returns:
        Response[Union[Any, Post]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        client=client,
        json_body=json_body,
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
    json_body: Post,
) -> Optional[Union[Any, Post]]:
    """Create Post

     Creates a new Post for the Employee.
    You must have the multi-post feature enabled.
    This endpoint is currently being beta tested and subject to un-announced breaking changes.

    Args:
        employer_id (str):
        employee_id (str):
        json_body (Post):

    Returns:
        Response[Union[Any, Post]]
    """

    return sync_detailed(
        employer_id=employer_id,
        employee_id=employee_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
    json_body: Post,
) -> Response[Union[Any, Post]]:
    """Create Post

     Creates a new Post for the Employee.
    You must have the multi-post feature enabled.
    This endpoint is currently being beta tested and subject to un-announced breaking changes.

    Args:
        employer_id (str):
        employee_id (str):
        json_body (Post):

    Returns:
        Response[Union[Any, Post]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
    json_body: Post,
) -> Optional[Union[Any, Post]]:
    """Create Post

     Creates a new Post for the Employee.
    You must have the multi-post feature enabled.
    This endpoint is currently being beta tested and subject to un-announced breaking changes.

    Args:
        employer_id (str):
        employee_id (str):
        json_body (Post):

    Returns:
        Response[Union[Any, Post]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            employee_id=employee_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
