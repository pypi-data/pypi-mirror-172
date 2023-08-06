from typing import Any, Dict, Optional, cast

import httpx

from ...client import Client
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/employers/{id}/suggestPayrollCode".format(client.base_url, id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[str]:
    if response.status_code == 200:
        response_200 = cast(str, response.json())
        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[str]:
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
) -> Response[str]:
    """Suggest Payroll Code

     This helper method returns a unique code for the next Employee that you create for the specified
    Employer.
    You don't have to use the value provided, you can use any value that is unqiue across Employees for
    the Employer.

    Args:
        id (str):

    Returns:
        Response[str]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
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
) -> Optional[str]:
    """Suggest Payroll Code

     This helper method returns a unique code for the next Employee that you create for the specified
    Employer.
    You don't have to use the value provided, you can use any value that is unqiue across Employees for
    the Employer.

    Args:
        id (str):

    Returns:
        Response[str]
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Client,
) -> Response[str]:
    """Suggest Payroll Code

     This helper method returns a unique code for the next Employee that you create for the specified
    Employer.
    You don't have to use the value provided, you can use any value that is unqiue across Employees for
    the Employer.

    Args:
        id (str):

    Returns:
        Response[str]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    id: str,
    *,
    client: Client,
) -> Optional[str]:
    """Suggest Payroll Code

     This helper method returns a unique code for the next Employee that you create for the specified
    Employer.
    You don't have to use the value provided, you can use any value that is unqiue across Employees for
    the Employer.

    Args:
        id (str):

    Returns:
        Response[str]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
