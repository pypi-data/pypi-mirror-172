import datetime
from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.report_response import ReportResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    id: str,
    *,
    client: Client,
    from_date: Union[Unset, None, datetime.datetime] = UNSET,
    to_date: Union[Unset, None, datetime.datetime] = UNSET,
    all_tenants: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/tenants/{id}/reports/weeklyactivity".format(client.base_url, id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(accept, Unset):
        headers["accept"] = accept

    params: Dict[str, Any] = {}
    json_from_date: Union[Unset, None, str] = UNSET
    if not isinstance(from_date, Unset):
        json_from_date = from_date.isoformat() if from_date else None

    params["fromDate"] = json_from_date

    json_to_date: Union[Unset, None, str] = UNSET
    if not isinstance(to_date, Unset):
        json_to_date = to_date.isoformat() if to_date else None

    params["toDate"] = json_to_date

    params["allTenants"] = all_tenants

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
    from_date: Union[Unset, None, datetime.datetime] = UNSET,
    to_date: Union[Unset, None, datetime.datetime] = UNSET,
    all_tenants: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,
) -> Response[ReportResponse]:
    """Weekly Activity Report

     Returns a report detailing User activity, summarised by week, for the given date range

    Args:
        id (str):
        from_date (Union[Unset, None, datetime.datetime]):
        to_date (Union[Unset, None, datetime.datetime]):
        all_tenants (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[ReportResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        from_date=from_date,
        to_date=to_date,
        all_tenants=all_tenants,
        accept=accept,
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
    from_date: Union[Unset, None, datetime.datetime] = UNSET,
    to_date: Union[Unset, None, datetime.datetime] = UNSET,
    all_tenants: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,
) -> Optional[ReportResponse]:
    """Weekly Activity Report

     Returns a report detailing User activity, summarised by week, for the given date range

    Args:
        id (str):
        from_date (Union[Unset, None, datetime.datetime]):
        to_date (Union[Unset, None, datetime.datetime]):
        all_tenants (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[ReportResponse]
    """

    return sync_detailed(
        id=id,
        client=client,
        from_date=from_date,
        to_date=to_date,
        all_tenants=all_tenants,
        accept=accept,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Client,
    from_date: Union[Unset, None, datetime.datetime] = UNSET,
    to_date: Union[Unset, None, datetime.datetime] = UNSET,
    all_tenants: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,
) -> Response[ReportResponse]:
    """Weekly Activity Report

     Returns a report detailing User activity, summarised by week, for the given date range

    Args:
        id (str):
        from_date (Union[Unset, None, datetime.datetime]):
        to_date (Union[Unset, None, datetime.datetime]):
        all_tenants (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[ReportResponse]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        from_date=from_date,
        to_date=to_date,
        all_tenants=all_tenants,
        accept=accept,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    id: str,
    *,
    client: Client,
    from_date: Union[Unset, None, datetime.datetime] = UNSET,
    to_date: Union[Unset, None, datetime.datetime] = UNSET,
    all_tenants: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,
) -> Optional[ReportResponse]:
    """Weekly Activity Report

     Returns a report detailing User activity, summarised by week, for the given date range

    Args:
        id (str):
        from_date (Union[Unset, None, datetime.datetime]):
        to_date (Union[Unset, None, datetime.datetime]):
        all_tenants (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[ReportResponse]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            from_date=from_date,
            to_date=to_date,
            all_tenants=all_tenants,
            accept=accept,
        )
    ).parsed
