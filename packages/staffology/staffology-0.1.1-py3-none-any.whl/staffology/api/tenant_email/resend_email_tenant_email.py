from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.tenant_email import TenantEmail
from ...types import Response


def _get_kwargs(
    id: str,
    email_id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/tenants/{id}/email/{emailId}".format(
        client.base_url, id=id, emailId=email_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[TenantEmail]:
    if response.status_code == 200:
        response_200 = TenantEmail.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[TenantEmail]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    id: str,
    email_id: str,
    *,
    client: Client,
) -> Response[TenantEmail]:
    """Re-send Email

     Re-sends an existing email.

    Args:
        id (str):
        email_id (str):

    Returns:
        Response[TenantEmail]
    """

    kwargs = _get_kwargs(
        id=id,
        email_id=email_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    id: str,
    email_id: str,
    *,
    client: Client,
) -> Optional[TenantEmail]:
    """Re-send Email

     Re-sends an existing email.

    Args:
        id (str):
        email_id (str):

    Returns:
        Response[TenantEmail]
    """

    return sync_detailed(
        id=id,
        email_id=email_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: str,
    email_id: str,
    *,
    client: Client,
) -> Response[TenantEmail]:
    """Re-send Email

     Re-sends an existing email.

    Args:
        id (str):
        email_id (str):

    Returns:
        Response[TenantEmail]
    """

    kwargs = _get_kwargs(
        id=id,
        email_id=email_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    id: str,
    email_id: str,
    *,
    client: Client,
) -> Optional[TenantEmail]:
    """Re-send Email

     Re-sends an existing email.

    Args:
        id (str):
        email_id (str):

    Returns:
        Response[TenantEmail]
    """

    return (
        await asyncio_detailed(
            id=id,
            email_id=email_id,
            client=client,
        )
    ).parsed
