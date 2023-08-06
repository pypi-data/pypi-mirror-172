from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.report_response import ReportResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    client: Client,
    month: Union[Unset, None, int] = UNSET,
    year: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    url = "{}/tenants/{id}/reports/users/nobillableactivity".format(
        client.base_url, id=id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["month"] = month

    params["year"] = year

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
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
    month: Union[Unset, None, int] = UNSET,
    year: Union[Unset, None, int] = UNSET,
) -> Response[ReportResponse]:
    """Get Users with no Billable Activity.

     Returns a .csv file containing users created in or before the given month that do not have billable
    activity.

    Args:
        id (str):
        month (Union[Unset, None, int]):
        year (Union[Unset, None, int]):

    Returns:
        Response[ReportResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        month=month,
        year=year,
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
    month: Union[Unset, None, int] = UNSET,
    year: Union[Unset, None, int] = UNSET,
) -> Optional[ReportResponse]:
    """Get Users with no Billable Activity.

     Returns a .csv file containing users created in or before the given month that do not have billable
    activity.

    Args:
        id (str):
        month (Union[Unset, None, int]):
        year (Union[Unset, None, int]):

    Returns:
        Response[ReportResponse]
    """

    return sync_detailed(
        id=id,
        client=client,
        month=month,
        year=year,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Client,
    month: Union[Unset, None, int] = UNSET,
    year: Union[Unset, None, int] = UNSET,
) -> Response[ReportResponse]:
    """Get Users with no Billable Activity.

     Returns a .csv file containing users created in or before the given month that do not have billable
    activity.

    Args:
        id (str):
        month (Union[Unset, None, int]):
        year (Union[Unset, None, int]):

    Returns:
        Response[ReportResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        month=month,
        year=year,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    id: str,
    *,
    client: Client,
    month: Union[Unset, None, int] = UNSET,
    year: Union[Unset, None, int] = UNSET,
) -> Optional[ReportResponse]:
    """Get Users with no Billable Activity.

     Returns a .csv file containing users created in or before the given month that do not have billable
    activity.

    Args:
        id (str):
        month (Union[Unset, None, int]):
        year (Union[Unset, None, int]):

    Returns:
        Response[ReportResponse]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            month=month,
            year=year,
        )
    ).parsed
