from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.employer_opening_balances import EmployerOpeningBalances
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    client: Client,
    json_body: EmployerOpeningBalances,
) -> Dict[str, Any]:
    url = "{}/employers/{id}/openingbalances".format(client.base_url, id=id)

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


def _parse_response(*, response: httpx.Response) -> Optional[EmployerOpeningBalances]:
    if response.status_code == 200:
        response_200 = EmployerOpeningBalances.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[EmployerOpeningBalances]:
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
    json_body: EmployerOpeningBalances,
) -> Response[EmployerOpeningBalances]:
    """Update EmployerOpeningBalances

     Updates the EmployerOpeningBalances for the Employer for their StartYear

    Args:
        id (str):
        json_body (EmployerOpeningBalances):

    Returns:
        Response[EmployerOpeningBalances]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        json_body=json_body,
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
    json_body: EmployerOpeningBalances,
) -> Optional[EmployerOpeningBalances]:
    """Update EmployerOpeningBalances

     Updates the EmployerOpeningBalances for the Employer for their StartYear

    Args:
        id (str):
        json_body (EmployerOpeningBalances):

    Returns:
        Response[EmployerOpeningBalances]
    """

    return sync_detailed(
        id=id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Client,
    json_body: EmployerOpeningBalances,
) -> Response[EmployerOpeningBalances]:
    """Update EmployerOpeningBalances

     Updates the EmployerOpeningBalances for the Employer for their StartYear

    Args:
        id (str):
        json_body (EmployerOpeningBalances):

    Returns:
        Response[EmployerOpeningBalances]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    id: str,
    *,
    client: Client,
    json_body: EmployerOpeningBalances,
) -> Optional[EmployerOpeningBalances]:
    """Update EmployerOpeningBalances

     Updates the EmployerOpeningBalances for the Employer for their StartYear

    Args:
        id (str):
        json_body (EmployerOpeningBalances):

    Returns:
        Response[EmployerOpeningBalances]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            json_body=json_body,
        )
    ).parsed
