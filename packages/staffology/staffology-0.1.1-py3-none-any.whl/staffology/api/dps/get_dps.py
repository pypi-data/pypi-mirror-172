from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.dps_notice import DpsNotice
from ...types import Response


def _get_kwargs(
    employer_id: str,
    id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/dps/notices/{id}".format(
        client.base_url, employerId=employer_id, id=id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[DpsNotice]:
    if response.status_code == 200:
        response_200 = DpsNotice.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[DpsNotice]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    id: str,
    *,
    client: Client,
) -> Response[DpsNotice]:
    """Get Notice

     Returns the specified DPS Notice.

    Args:
        employer_id (str):
        id (str):

    Returns:
        Response[DpsNotice]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    employer_id: str,
    id: str,
    *,
    client: Client,
) -> Optional[DpsNotice]:
    """Get Notice

     Returns the specified DPS Notice.

    Args:
        employer_id (str):
        id (str):

    Returns:
        Response[DpsNotice]
    """

    return sync_detailed(
        employer_id=employer_id,
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    id: str,
    *,
    client: Client,
) -> Response[DpsNotice]:
    """Get Notice

     Returns the specified DPS Notice.

    Args:
        employer_id (str):
        id (str):

    Returns:
        Response[DpsNotice]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    id: str,
    *,
    client: Client,
) -> Optional[DpsNotice]:
    """Get Notice

     Returns the specified DPS Notice.

    Args:
        employer_id (str):
        id (str):

    Returns:
        Response[DpsNotice]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            id=id,
            client=client,
        )
    ).parsed
