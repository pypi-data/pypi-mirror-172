from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.bureau_settings import BureauSettings
from ...types import Response


def _get_kwargs(
    employer_id: str,
    *,
    client: Client,
    json_body: BureauSettings,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/bureau/settings".format(
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


def _parse_response(*, response: httpx.Response) -> Optional[BureauSettings]:
    if response.status_code == 200:
        response_200 = BureauSettings.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[BureauSettings]:
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
    json_body: BureauSettings,
) -> Response[BureauSettings]:
    """Update BureauSettings

     Updates the BureaSettings for the Employer

    Args:
        employer_id (str):
        json_body (BureauSettings): Represents the BureauSettings for an Employer.

    Returns:
        Response[BureauSettings]
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
    json_body: BureauSettings,
) -> Optional[BureauSettings]:
    """Update BureauSettings

     Updates the BureaSettings for the Employer

    Args:
        employer_id (str):
        json_body (BureauSettings): Represents the BureauSettings for an Employer.

    Returns:
        Response[BureauSettings]
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
    json_body: BureauSettings,
) -> Response[BureauSettings]:
    """Update BureauSettings

     Updates the BureaSettings for the Employer

    Args:
        employer_id (str):
        json_body (BureauSettings): Represents the BureauSettings for an Employer.

    Returns:
        Response[BureauSettings]
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
    json_body: BureauSettings,
) -> Optional[BureauSettings]:
    """Update BureauSettings

     Updates the BureaSettings for the Employer

    Args:
        employer_id (str):
        json_body (BureauSettings): Represents the BureauSettings for an Employer.

    Returns:
        Response[BureauSettings]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
