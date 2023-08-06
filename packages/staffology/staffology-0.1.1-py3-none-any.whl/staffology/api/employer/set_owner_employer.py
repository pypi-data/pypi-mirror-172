from typing import Any, Dict

import httpx

from ...client import Client
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    client: Client,
    json_body: str,
) -> Dict[str, Any]:
    url = "{}/employers/{id}/users/owner".format(client.base_url, id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
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
    *,
    client: Client,
    json_body: str,
) -> Response[Any]:
    """Set Owner

     Sets the owner for the employer. You must be the owner of the Employer to set this value.
    The user you are setting as the owner must already have the role Admin.
    You can get a list of users from the ListUsers endpoint.

    Args:
        id (str):
        json_body (str):

    Returns:
        Response[Any]
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


async def asyncio_detailed(
    id: str,
    *,
    client: Client,
    json_body: str,
) -> Response[Any]:
    """Set Owner

     Sets the owner for the employer. You must be the owner of the Employer to set this value.
    The user you are setting as the owner must already have the role Admin.
    You can get a list of users from the ListUsers endpoint.

    Args:
        id (str):
        json_body (str):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
