from typing import Any, Dict, List

import httpx

from ...client import Client
from ...types import Response


def _get_kwargs(
    employer_id: str,
    *,
    client: Client,
    json_body: List[str],
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/employees/delete".format(
        client.base_url, employerId=employer_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
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
    *,
    client: Client,
    json_body: List[str],
) -> Response[Any]:
    """Delete Employees

     Used to delete multiple employees.
    The body should contain an array of Ids to identify the employees to delete.

    Args:
        employer_id (str):
        json_body (List[str]):

    Returns:
        Response[Any]
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


async def asyncio_detailed(
    employer_id: str,
    *,
    client: Client,
    json_body: List[str],
) -> Response[Any]:
    """Delete Employees

     Used to delete multiple employees.
    The body should contain an array of Ids to identify the employees to delete.

    Args:
        employer_id (str):
        json_body (List[str]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
