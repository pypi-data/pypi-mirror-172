from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.tenant import Tenant
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    client: Client,
    json_body: Tenant,
) -> Dict[str, Any]:
    url = "{}/tenants/{id}".format(client.base_url, id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, Tenant]]:
    if response.status_code == 200:
        response_200 = Tenant.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, Tenant]]:
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
    json_body: Tenant,
) -> Response[Union[Any, Tenant]]:
    """Update a Tenant

     If you are an administrator for a Tenant then you can update the settings for it using this API call

    Args:
        id (str):
        json_body (Tenant): The Tenant model represents the brand that provides the account.
            This is used by our White Label partners to manage and brand their user accounts.
            Unless you are an admin for a White Label account you'll have no interest in this model.

    Returns:
        Response[Union[Any, Tenant]]
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


def sync(
    id: str,
    *,
    client: Client,
    json_body: Tenant,
) -> Optional[Union[Any, Tenant]]:
    """Update a Tenant

     If you are an administrator for a Tenant then you can update the settings for it using this API call

    Args:
        id (str):
        json_body (Tenant): The Tenant model represents the brand that provides the account.
            This is used by our White Label partners to manage and brand their user accounts.
            Unless you are an admin for a White Label account you'll have no interest in this model.

    Returns:
        Response[Union[Any, Tenant]]
    """

    return sync_detailed(
        id=id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Client,
    json_body: Tenant,
) -> Response[Union[Any, Tenant]]:
    """Update a Tenant

     If you are an administrator for a Tenant then you can update the settings for it using this API call

    Args:
        id (str):
        json_body (Tenant): The Tenant model represents the brand that provides the account.
            This is used by our White Label partners to manage and brand their user accounts.
            Unless you are an admin for a White Label account you'll have no interest in this model.

    Returns:
        Response[Union[Any, Tenant]]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    id: str,
    *,
    client: Client,
    json_body: Tenant,
) -> Optional[Union[Any, Tenant]]:
    """Update a Tenant

     If you are an administrator for a Tenant then you can update the settings for it using this API call

    Args:
        id (str):
        json_body (Tenant): The Tenant model represents the brand that provides the account.
            This is used by our White Label partners to manage and brand their user accounts.
            Unless you are an admin for a White Label account you'll have no interest in this model.

    Returns:
        Response[Union[Any, Tenant]]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            json_body=json_body,
        )
    ).parsed
