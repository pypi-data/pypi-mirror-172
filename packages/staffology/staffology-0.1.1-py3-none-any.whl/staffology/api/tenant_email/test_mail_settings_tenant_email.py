from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.employer_email import EmployerEmail
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    client: Client,
    email: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/tenants/{id}/email/settings/test".format(client.base_url, id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["email"] = email

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[EmployerEmail]:
    if response.status_code == 201:
        response_201 = EmployerEmail.from_dict(response.json())

        return response_201
    return None


def _build_response(*, response: httpx.Response) -> Response[EmployerEmail]:
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
    email: Union[Unset, None, str] = UNSET,
) -> Response[EmployerEmail]:
    """Send test email

     This API call will generate a test email based on your MailSettings.

    Args:
        id (str):
        email (Union[Unset, None, str]):

    Returns:
        Response[EmployerEmail]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        email=email,
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
    email: Union[Unset, None, str] = UNSET,
) -> Optional[EmployerEmail]:
    """Send test email

     This API call will generate a test email based on your MailSettings.

    Args:
        id (str):
        email (Union[Unset, None, str]):

    Returns:
        Response[EmployerEmail]
    """

    return sync_detailed(
        id=id,
        client=client,
        email=email,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Client,
    email: Union[Unset, None, str] = UNSET,
) -> Response[EmployerEmail]:
    """Send test email

     This API call will generate a test email based on your MailSettings.

    Args:
        id (str):
        email (Union[Unset, None, str]):

    Returns:
        Response[EmployerEmail]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        email=email,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    id: str,
    *,
    client: Client,
    email: Union[Unset, None, str] = UNSET,
) -> Optional[EmployerEmail]:
    """Send test email

     This API call will generate a test email based on your MailSettings.

    Args:
        id (str):
        email (Union[Unset, None, str]):

    Returns:
        Response[EmployerEmail]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            email=email,
        )
    ).parsed
