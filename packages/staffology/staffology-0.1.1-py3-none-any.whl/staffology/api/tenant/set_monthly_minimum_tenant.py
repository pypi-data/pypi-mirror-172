from typing import Any, Dict

import httpx

from ...client import Client
from ...models.monthly_minimum import MonthlyMinimum
from ...types import Response


def _get_kwargs(
    id: str,
    user_id: str,
    *,
    client: Client,
    json_body: MonthlyMinimum,
) -> Dict[str, Any]:
    url = "{}/tenants/{id}/users/{userId}/monthlyminimum".format(
        client.base_url, id=id, userId=user_id
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


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    id: str,
    user_id: str,
    *,
    client: Client,
    json_body: MonthlyMinimum,
) -> Response[Any]:
    """Set Monthly Minimum

     Updates the MonthlyMinimum subscrition charge for a user

    Args:
        id (str):
        user_id (str):
        json_body (MonthlyMinimum):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        user_id=user_id,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    id: str,
    user_id: str,
    *,
    client: Client,
    json_body: MonthlyMinimum,
) -> Response[Any]:
    """Set Monthly Minimum

     Updates the MonthlyMinimum subscrition charge for a user

    Args:
        id (str):
        user_id (str):
        json_body (MonthlyMinimum):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        id=id,
        user_id=user_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
