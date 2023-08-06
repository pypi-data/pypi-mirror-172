from typing import Any, Dict

import httpx

from ...client import Client
from ...types import Response


def _get_kwargs(
    employer_id: str,
    code: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/departments/{code}".format(
        client.base_url, employerId=employer_id, code=code
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "delete",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    employer_id: str,
    code: str,
    *,
    client: Client,
) -> Response[Any]:
    """Delete Department

     Deletes the specified Department.

    Args:
        employer_id (str):
        code (str):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        code=code,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    employer_id: str,
    code: str,
    *,
    client: Client,
) -> Response[Any]:
    """Delete Department

     Deletes the specified Department.

    Args:
        employer_id (str):
        code (str):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        code=code,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
