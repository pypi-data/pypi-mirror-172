from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.tenant import Tenant
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: Tenant,
) -> Dict[str, Any]:
    url = "{}/tenants".format(client.base_url)

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


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, Tenant]]:
    if response.status_code == 201:
        response_201 = Tenant.from_dict(response.json())

        return response_201
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, Tenant]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: Tenant,
) -> Response[Union[Any, Tenant]]:
    """Create a Tenant

     Use this method to create a new Tenant
    Only available to SuperAdmins

    Args:
        json_body (Tenant): The Tenant model represents the brand that provides the account.
            This is used by our White Label partners to manage and brand their user accounts.
            Unless you are an admin for a White Label account you'll have no interest in this model.

    Returns:
        Response[Union[Any, Tenant]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    json_body: Tenant,
) -> Optional[Union[Any, Tenant]]:
    """Create a Tenant

     Use this method to create a new Tenant
    Only available to SuperAdmins

    Args:
        json_body (Tenant): The Tenant model represents the brand that provides the account.
            This is used by our White Label partners to manage and brand their user accounts.
            Unless you are an admin for a White Label account you'll have no interest in this model.

    Returns:
        Response[Union[Any, Tenant]]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: Tenant,
) -> Response[Union[Any, Tenant]]:
    """Create a Tenant

     Use this method to create a new Tenant
    Only available to SuperAdmins

    Args:
        json_body (Tenant): The Tenant model represents the brand that provides the account.
            This is used by our White Label partners to manage and brand their user accounts.
            Unless you are an admin for a White Label account you'll have no interest in this model.

    Returns:
        Response[Union[Any, Tenant]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    json_body: Tenant,
) -> Optional[Union[Any, Tenant]]:
    """Create a Tenant

     Use this method to create a new Tenant
    Only available to SuperAdmins

    Args:
        json_body (Tenant): The Tenant model represents the brand that provides the account.
            This is used by our White Label partners to manage and brand their user accounts.
            Unless you are an admin for a White Label account you'll have no interest in this model.

    Returns:
        Response[Union[Any, Tenant]]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
