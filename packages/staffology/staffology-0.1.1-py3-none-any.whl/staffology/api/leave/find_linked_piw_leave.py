import datetime
from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.leave_pay_type import LeavePayType
from ...models.leave_type import LeaveType
from ...models.linked_piw import LinkedPiw
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
    leave_type: Union[Unset, None, LeaveType] = UNSET,
    leave_pay_type: Union[Unset, None, LeavePayType] = UNSET,
    from_: Union[Unset, None, datetime.datetime] = UNSET,
    to: Union[Unset, None, datetime.datetime] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/employees/{employeeId}/leave/findlinkedpiw".format(
        client.base_url, employerId=employer_id, employeeId=employee_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_leave_type: Union[Unset, None, str] = UNSET
    if not isinstance(leave_type, Unset):
        json_leave_type = leave_type.value if leave_type else None

    params["leaveType"] = json_leave_type

    json_leave_pay_type: Union[Unset, None, str] = UNSET
    if not isinstance(leave_pay_type, Unset):
        json_leave_pay_type = leave_pay_type.value if leave_pay_type else None

    params["leavePayType"] = json_leave_pay_type

    json_from_: Union[Unset, None, str] = UNSET
    if not isinstance(from_, Unset):
        json_from_ = from_.isoformat() if from_ else None

    params["from"] = json_from_

    json_to: Union[Unset, None, str] = UNSET
    if not isinstance(to, Unset):
        json_to = to.isoformat() if to else None

    params["to"] = json_to

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[LinkedPiw]:
    if response.status_code == 200:
        response_200 = LinkedPiw.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[LinkedPiw]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
    leave_type: Union[Unset, None, LeaveType] = UNSET,
    leave_pay_type: Union[Unset, None, LeavePayType] = UNSET,
    from_: Union[Unset, None, datetime.datetime] = UNSET,
    to: Union[Unset, None, datetime.datetime] = UNSET,
) -> Response[LinkedPiw]:
    """Find Linked Piw

     Finds the linked piw the supplied leave would linked to, or null if none found

    Args:
        employer_id (str):
        employee_id (str):
        leave_type (Union[Unset, None, LeaveType]):
        leave_pay_type (Union[Unset, None, LeavePayType]):
        from_ (Union[Unset, None, datetime.datetime]):
        to (Union[Unset, None, datetime.datetime]):

    Returns:
        Response[LinkedPiw]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        client=client,
        leave_type=leave_type,
        leave_pay_type=leave_pay_type,
        from_=from_,
        to=to,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
    leave_type: Union[Unset, None, LeaveType] = UNSET,
    leave_pay_type: Union[Unset, None, LeavePayType] = UNSET,
    from_: Union[Unset, None, datetime.datetime] = UNSET,
    to: Union[Unset, None, datetime.datetime] = UNSET,
) -> Optional[LinkedPiw]:
    """Find Linked Piw

     Finds the linked piw the supplied leave would linked to, or null if none found

    Args:
        employer_id (str):
        employee_id (str):
        leave_type (Union[Unset, None, LeaveType]):
        leave_pay_type (Union[Unset, None, LeavePayType]):
        from_ (Union[Unset, None, datetime.datetime]):
        to (Union[Unset, None, datetime.datetime]):

    Returns:
        Response[LinkedPiw]
    """

    return sync_detailed(
        employer_id=employer_id,
        employee_id=employee_id,
        client=client,
        leave_type=leave_type,
        leave_pay_type=leave_pay_type,
        from_=from_,
        to=to,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
    leave_type: Union[Unset, None, LeaveType] = UNSET,
    leave_pay_type: Union[Unset, None, LeavePayType] = UNSET,
    from_: Union[Unset, None, datetime.datetime] = UNSET,
    to: Union[Unset, None, datetime.datetime] = UNSET,
) -> Response[LinkedPiw]:
    """Find Linked Piw

     Finds the linked piw the supplied leave would linked to, or null if none found

    Args:
        employer_id (str):
        employee_id (str):
        leave_type (Union[Unset, None, LeaveType]):
        leave_pay_type (Union[Unset, None, LeavePayType]):
        from_ (Union[Unset, None, datetime.datetime]):
        to (Union[Unset, None, datetime.datetime]):

    Returns:
        Response[LinkedPiw]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        client=client,
        leave_type=leave_type,
        leave_pay_type=leave_pay_type,
        from_=from_,
        to=to,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
    leave_type: Union[Unset, None, LeaveType] = UNSET,
    leave_pay_type: Union[Unset, None, LeavePayType] = UNSET,
    from_: Union[Unset, None, datetime.datetime] = UNSET,
    to: Union[Unset, None, datetime.datetime] = UNSET,
) -> Optional[LinkedPiw]:
    """Find Linked Piw

     Finds the linked piw the supplied leave would linked to, or null if none found

    Args:
        employer_id (str):
        employee_id (str):
        leave_type (Union[Unset, None, LeaveType]):
        leave_pay_type (Union[Unset, None, LeavePayType]):
        from_ (Union[Unset, None, datetime.datetime]):
        to (Union[Unset, None, datetime.datetime]):

    Returns:
        Response[LinkedPiw]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            employee_id=employee_id,
            client=client,
            leave_type=leave_type,
            leave_pay_type=leave_pay_type,
            from_=from_,
            to=to,
        )
    ).parsed
