from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.employer_group import EmployerGroup
from ...types import Response


def _get_kwargs(
    code: str,
    *,
    client: Client,
    json_body: EmployerGroup,
) -> Dict[str, Any]:
    url = "{}/employers/groups/{code}".format(client.base_url, code=code)

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


def _parse_response(*, response: httpx.Response) -> Optional[EmployerGroup]:
    if response.status_code == 200:
        response_200 = EmployerGroup.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[EmployerGroup]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    code: str,
    *,
    client: Client,
    json_body: EmployerGroup,
) -> Response[EmployerGroup]:
    """Update EmployerGroup

     Updates a EmployerGroup for the user.

    Args:
        code (str):
        json_body (EmployerGroup):

    Returns:
        Response[EmployerGroup]
    """

    kwargs = _get_kwargs(
        code=code,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    code: str,
    *,
    client: Client,
    json_body: EmployerGroup,
) -> Optional[EmployerGroup]:
    """Update EmployerGroup

     Updates a EmployerGroup for the user.

    Args:
        code (str):
        json_body (EmployerGroup):

    Returns:
        Response[EmployerGroup]
    """

    return sync_detailed(
        code=code,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    code: str,
    *,
    client: Client,
    json_body: EmployerGroup,
) -> Response[EmployerGroup]:
    """Update EmployerGroup

     Updates a EmployerGroup for the user.

    Args:
        code (str):
        json_body (EmployerGroup):

    Returns:
        Response[EmployerGroup]
    """

    kwargs = _get_kwargs(
        code=code,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    code: str,
    *,
    client: Client,
    json_body: EmployerGroup,
) -> Optional[EmployerGroup]:
    """Update EmployerGroup

     Updates a EmployerGroup for the user.

    Args:
        code (str):
        json_body (EmployerGroup):

    Returns:
        Response[EmployerGroup]
    """

    return (
        await asyncio_detailed(
            code=code,
            client=client,
            json_body=json_body,
        )
    ).parsed
