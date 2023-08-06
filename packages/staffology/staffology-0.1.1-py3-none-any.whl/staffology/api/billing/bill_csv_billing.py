from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.report_response import ReportResponse
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/billing/bill/{id}/csv".format(client.base_url, id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[ReportResponse]:
    if response.status_code == 200:
        response_200 = ReportResponse.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[ReportResponse]:
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
) -> Response[ReportResponse]:
    """Get Bill CSV

     Returns the specified UsageBill as a CSV file

    Args:
        id (str):

    Returns:
        Response[ReportResponse]
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
) -> Optional[ReportResponse]:
    """Get Bill CSV

     Returns the specified UsageBill as a CSV file

    Args:
        id (str):

    Returns:
        Response[ReportResponse]
    """

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Client,
) -> Response[ReportResponse]:
    """Get Bill CSV

     Returns the specified UsageBill as a CSV file

    Args:
        id (str):

    Returns:
        Response[ReportResponse]
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
) -> Optional[ReportResponse]:
    """Get Bill CSV

     Returns the specified UsageBill as a CSV file

    Args:
        id (str):

    Returns:
        Response[ReportResponse]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
