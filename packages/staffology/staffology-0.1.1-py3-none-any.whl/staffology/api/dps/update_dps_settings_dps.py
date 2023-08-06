from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.dps_settings import DpsSettings
from ...types import Response


def _get_kwargs(
    employer_id: str,
    *,
    client: Client,
    json_body: DpsSettings,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/dps/settings".format(
        client.base_url, employerId=employer_id
    )

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


def _parse_response(*, response: httpx.Response) -> Optional[DpsSettings]:
    if response.status_code == 200:
        response_200 = DpsSettings.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[DpsSettings]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    *,
    client: Client,
    json_body: DpsSettings,
) -> Response[DpsSettings]:
    """Update DPS Settings

     Updates the DpsSettings for the Employer

    Args:
        employer_id (str):
        json_body (DpsSettings): This model is used to set an employers settings for HMRCs Data
            Provisioning Service

    Returns:
        Response[DpsSettings]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
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
    *,
    client: Client,
    json_body: DpsSettings,
) -> Optional[DpsSettings]:
    """Update DPS Settings

     Updates the DpsSettings for the Employer

    Args:
        employer_id (str):
        json_body (DpsSettings): This model is used to set an employers settings for HMRCs Data
            Provisioning Service

    Returns:
        Response[DpsSettings]
    """

    return sync_detailed(
        employer_id=employer_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    *,
    client: Client,
    json_body: DpsSettings,
) -> Response[DpsSettings]:
    """Update DPS Settings

     Updates the DpsSettings for the Employer

    Args:
        employer_id (str):
        json_body (DpsSettings): This model is used to set an employers settings for HMRCs Data
            Provisioning Service

    Returns:
        Response[DpsSettings]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    *,
    client: Client,
    json_body: DpsSettings,
) -> Optional[DpsSettings]:
    """Update DPS Settings

     Updates the DpsSettings for the Employer

    Args:
        employer_id (str):
        json_body (DpsSettings): This model is used to set an employers settings for HMRCs Data
            Provisioning Service

    Returns:
        Response[DpsSettings]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
