from typing import Any, Dict, List, Union

import httpx

from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    *,
    client: Client,
    json_body: List[str],
    on_hold: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/employees/onhold".format(
        client.base_url, employerId=employer_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["onHold"] = on_hold

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
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
    on_hold: Union[Unset, None, bool] = UNSET,
) -> Response[Any]:
    """Mark as On Hold

     Used to mark multiple employees as On Hold or not On Hold.
    The body should contain an array of Ids to identify the employees to update.

    Args:
        employer_id (str):
        on_hold (Union[Unset, None, bool]):
        json_body (List[str]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        json_body=json_body,
        on_hold=on_hold,
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
    on_hold: Union[Unset, None, bool] = UNSET,
) -> Response[Any]:
    """Mark as On Hold

     Used to mark multiple employees as On Hold or not On Hold.
    The body should contain an array of Ids to identify the employees to update.

    Args:
        employer_id (str):
        on_hold (Union[Unset, None, bool]):
        json_body (List[str]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        json_body=json_body,
        on_hold=on_hold,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
