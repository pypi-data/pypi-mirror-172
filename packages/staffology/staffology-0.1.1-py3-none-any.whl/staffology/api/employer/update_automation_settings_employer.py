from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.automation_settings import AutomationSettings
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    client: Client,
    json_body: AutomationSettings,
) -> Dict[str, Any]:
    url = "{}/employers/{id}/automation".format(client.base_url, id=id)

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


def _parse_response(*, response: httpx.Response) -> Optional[AutomationSettings]:
    if response.status_code == 200:
        response_200 = AutomationSettings.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[AutomationSettings]:
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
    json_body: AutomationSettings,
) -> Response[AutomationSettings]:
    """Update Automation Settings

     Updates the AutomationSettings for the Employer

    Args:
        id (str):
        json_body (AutomationSettings): Configures various automation settings for an Employer

    Returns:
        Response[AutomationSettings]
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
    json_body: AutomationSettings,
) -> Optional[AutomationSettings]:
    """Update Automation Settings

     Updates the AutomationSettings for the Employer

    Args:
        id (str):
        json_body (AutomationSettings): Configures various automation settings for an Employer

    Returns:
        Response[AutomationSettings]
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
    json_body: AutomationSettings,
) -> Response[AutomationSettings]:
    """Update Automation Settings

     Updates the AutomationSettings for the Employer

    Args:
        id (str):
        json_body (AutomationSettings): Configures various automation settings for an Employer

    Returns:
        Response[AutomationSettings]
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
    json_body: AutomationSettings,
) -> Optional[AutomationSettings]:
    """Update Automation Settings

     Updates the AutomationSettings for the Employer

    Args:
        id (str):
        json_body (AutomationSettings): Configures various automation settings for an Employer

    Returns:
        Response[AutomationSettings]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            json_body=json_body,
        )
    ).parsed
