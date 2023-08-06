from typing import Any, Dict

import httpx

from ...client import Client
from ...types import Response


def _get_kwargs(
    id: str,
    user_id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/employers/{id}/users/{userId}".format(
        client.base_url, id=id, userId=user_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "delete",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    id: str,
    user_id: str,
    *,
    client: Client,
) -> Response[Any]:
    """Remove User

     Removes a User from an Employer.
    You cannot remove Users that are marked as the owner of the Employer.
    You must be the owner of the Employer in order to remove other Users.

    Args:
        id (str):
        user_id (str):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        user_id=user_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    id: str,
    user_id: str,
    *,
    client: Client,
) -> Response[Any]:
    """Remove User

     Removes a User from an Employer.
    You cannot remove Users that are marked as the owner of the Employer.
    You must be the owner of the Employer in order to remove other Users.

    Args:
        id (str):
        user_id (str):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        user_id=user_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
