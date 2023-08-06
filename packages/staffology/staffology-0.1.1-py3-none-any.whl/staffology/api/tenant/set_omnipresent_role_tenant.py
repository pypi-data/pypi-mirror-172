from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...models.role import Role
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    user_id: str,
    *,
    client: Client,
    role: Union[Unset, None, Role] = UNSET,
) -> Dict[str, Any]:
    url = "{}/tenants/{id}/users/{userId}/omnipresentrole".format(
        client.base_url, id=id, userId=user_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_role: Union[Unset, None, str] = UNSET
    if not isinstance(role, Unset):
        json_role = role.value if role else None

    params["role"] = json_role

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
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
    role: Union[Unset, None, Role] = UNSET,
) -> Response[Any]:
    """Set Omnipresent Role

     If the Tenant has EnableOmnipresentUsers enabled then they have the ability to make users have
    automatic access to all employers on that tenant with the specified Role.
    This end point updates the Omnipresent Role of the user.

    Args:
        id (str):
        user_id (str):
        role (Union[Unset, None, Role]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        user_id=user_id,
        client=client,
        role=role,
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
    role: Union[Unset, None, Role] = UNSET,
) -> Response[Any]:
    """Set Omnipresent Role

     If the Tenant has EnableOmnipresentUsers enabled then they have the ability to make users have
    automatic access to all employers on that tenant with the specified Role.
    This end point updates the Omnipresent Role of the user.

    Args:
        id (str):
        user_id (str):
        role (Union[Unset, None, Role]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        user_id=user_id,
        client=client,
        role=role,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
