import datetime
from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.average_weekly_earnings import AverageWeeklyEarnings
from ...models.leave_type import LeaveType
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    id: str,
    *,
    client: Client,
    date: Union[Unset, None, datetime.datetime] = UNSET,
    leave_type: Union[Unset, None, LeaveType] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/employees/{id}/awe".format(
        client.base_url, employerId=employer_id, id=id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_date: Union[Unset, None, str] = UNSET
    if not isinstance(date, Unset):
        json_date = date.isoformat() if date else None

    params["date"] = json_date

    json_leave_type: Union[Unset, None, str] = UNSET
    if not isinstance(leave_type, Unset):
        json_leave_type = leave_type.value if leave_type else None

    params["leaveType"] = json_leave_type

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[AverageWeeklyEarnings]:
    if response.status_code == 200:
        response_200 = AverageWeeklyEarnings.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[AverageWeeklyEarnings]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    id: str,
    *,
    client: Client,
    date: Union[Unset, None, datetime.datetime] = UNSET,
    leave_type: Union[Unset, None, LeaveType] = UNSET,
) -> Response[AverageWeeklyEarnings]:
    """Average Weekly Earnings

     Calculates the Average Weekly Earnings for an Employee at the given date.
    You can optionally include a LeaveType and we'll adjust the given date accordingly
    For example if you specify Maternity then it'll be moved back by 15 weeks

    Args:
        employer_id (str):
        id (str):
        date (Union[Unset, None, datetime.datetime]):
        leave_type (Union[Unset, None, LeaveType]):

    Returns:
        Response[AverageWeeklyEarnings]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        client=client,
        date=date,
        leave_type=leave_type,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    employer_id: str,
    id: str,
    *,
    client: Client,
    date: Union[Unset, None, datetime.datetime] = UNSET,
    leave_type: Union[Unset, None, LeaveType] = UNSET,
) -> Optional[AverageWeeklyEarnings]:
    """Average Weekly Earnings

     Calculates the Average Weekly Earnings for an Employee at the given date.
    You can optionally include a LeaveType and we'll adjust the given date accordingly
    For example if you specify Maternity then it'll be moved back by 15 weeks

    Args:
        employer_id (str):
        id (str):
        date (Union[Unset, None, datetime.datetime]):
        leave_type (Union[Unset, None, LeaveType]):

    Returns:
        Response[AverageWeeklyEarnings]
    """

    return sync_detailed(
        employer_id=employer_id,
        id=id,
        client=client,
        date=date,
        leave_type=leave_type,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    id: str,
    *,
    client: Client,
    date: Union[Unset, None, datetime.datetime] = UNSET,
    leave_type: Union[Unset, None, LeaveType] = UNSET,
) -> Response[AverageWeeklyEarnings]:
    """Average Weekly Earnings

     Calculates the Average Weekly Earnings for an Employee at the given date.
    You can optionally include a LeaveType and we'll adjust the given date accordingly
    For example if you specify Maternity then it'll be moved back by 15 weeks

    Args:
        employer_id (str):
        id (str):
        date (Union[Unset, None, datetime.datetime]):
        leave_type (Union[Unset, None, LeaveType]):

    Returns:
        Response[AverageWeeklyEarnings]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        client=client,
        date=date,
        leave_type=leave_type,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    id: str,
    *,
    client: Client,
    date: Union[Unset, None, datetime.datetime] = UNSET,
    leave_type: Union[Unset, None, LeaveType] = UNSET,
) -> Optional[AverageWeeklyEarnings]:
    """Average Weekly Earnings

     Calculates the Average Weekly Earnings for an Employee at the given date.
    You can optionally include a LeaveType and we'll adjust the given date accordingly
    For example if you specify Maternity then it'll be moved back by 15 weeks

    Args:
        employer_id (str):
        id (str):
        date (Union[Unset, None, datetime.datetime]):
        leave_type (Union[Unset, None, LeaveType]):

    Returns:
        Response[AverageWeeklyEarnings]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            id=id,
            client=client,
            date=date,
            leave_type=leave_type,
        )
    ).parsed
