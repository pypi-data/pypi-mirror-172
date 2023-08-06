from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.holiday_report_report_response import HolidayReportReportResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    *,
    client: Client,
    accruals: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/reports/holiday".format(
        client.base_url, employerId=employer_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(accept, Unset):
        headers["accept"] = accept

    params: Dict[str, Any] = {}
    params["accruals"] = accruals

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[HolidayReportReportResponse]:
    if response.status_code == 200:
        response_200 = HolidayReportReportResponse.from_dict(response.json())

        return response_200
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[HolidayReportReportResponse]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    *,
    client: Client,
    accruals: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,
) -> Response[HolidayReportReportResponse]:
    """Holiday

     Returns a report summarising holiday usage for all employees.

    Args:
        employer_id (str):
        accruals (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[HolidayReportReportResponse]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        accruals=accruals,
        accept=accept,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    employer_id: str,
    *,
    client: Client,
    accruals: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,
) -> Optional[HolidayReportReportResponse]:
    """Holiday

     Returns a report summarising holiday usage for all employees.

    Args:
        employer_id (str):
        accruals (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[HolidayReportReportResponse]
    """

    return sync_detailed(
        employer_id=employer_id,
        client=client,
        accruals=accruals,
        accept=accept,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    *,
    client: Client,
    accruals: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,
) -> Response[HolidayReportReportResponse]:
    """Holiday

     Returns a report summarising holiday usage for all employees.

    Args:
        employer_id (str):
        accruals (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[HolidayReportReportResponse]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        accruals=accruals,
        accept=accept,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    *,
    client: Client,
    accruals: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = UNSET,
) -> Optional[HolidayReportReportResponse]:
    """Holiday

     Returns a report summarising holiday usage for all employees.

    Args:
        employer_id (str):
        accruals (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[HolidayReportReportResponse]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            client=client,
            accruals=accruals,
            accept=accept,
        )
    ).parsed
