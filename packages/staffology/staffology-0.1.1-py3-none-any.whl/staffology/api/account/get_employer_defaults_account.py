from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.employer_defaults import EmployerDefaults
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/account/employerdefaults".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[EmployerDefaults]:
    if response.status_code == 200:
        response_200 = EmployerDefaults.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[EmployerDefaults]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
) -> Response[EmployerDefaults]:
    """Get EmployerDefaults

     Get the EmployerDefaults for the currently authorised User.

    Returns:
        Response[EmployerDefaults]
    """

    kwargs = _get_kwargs(
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
) -> Optional[EmployerDefaults]:
    """Get EmployerDefaults

     Get the EmployerDefaults for the currently authorised User.

    Returns:
        Response[EmployerDefaults]
    """

    return sync_detailed(
        client=client,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
) -> Response[EmployerDefaults]:
    """Get EmployerDefaults

     Get the EmployerDefaults for the currently authorised User.

    Returns:
        Response[EmployerDefaults]
    """

    kwargs = _get_kwargs(
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
) -> Optional[EmployerDefaults]:
    """Get EmployerDefaults

     Get the EmployerDefaults for the currently authorised User.

    Returns:
        Response[EmployerDefaults]
    """

    return (
        await asyncio_detailed(
            client=client,
        )
    ).parsed
