from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.cookie_preference import CookiePreference
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: CookiePreference,
) -> Dict[str, Any]:
    url = "{}/account/cookiepreferences".format(client.base_url)

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


def _parse_response(*, response: httpx.Response) -> Optional[CookiePreference]:
    if response.status_code == 200:
        response_200 = CookiePreference.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[CookiePreference]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: CookiePreference,
) -> Response[CookiePreference]:
    """Update Cookie Preferences

     Updates cookie preferences for your account.

    Args:
        json_body (CookiePreference):

    Returns:
        Response[CookiePreference]
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
    json_body: CookiePreference,
) -> Optional[CookiePreference]:
    """Update Cookie Preferences

     Updates cookie preferences for your account.

    Args:
        json_body (CookiePreference):

    Returns:
        Response[CookiePreference]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: CookiePreference,
) -> Response[CookiePreference]:
    """Update Cookie Preferences

     Updates cookie preferences for your account.

    Args:
        json_body (CookiePreference):

    Returns:
        Response[CookiePreference]
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
    json_body: CookiePreference,
) -> Optional[CookiePreference]:
    """Update Cookie Preferences

     Updates cookie preferences for your account.

    Args:
        json_body (CookiePreference):

    Returns:
        Response[CookiePreference]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
