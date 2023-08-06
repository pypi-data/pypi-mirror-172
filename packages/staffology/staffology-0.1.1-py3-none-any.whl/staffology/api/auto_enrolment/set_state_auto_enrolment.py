import datetime
from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.ae_assessment import AeAssessment
from ...models.ae_employee_state import AeEmployeeState
from ...models.ae_status import AeStatus
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
    state: Union[Unset, None, AeEmployeeState] = UNSET,
    status: Union[Unset, None, AeStatus] = UNSET,
    state_date: Union[Unset, None, datetime.datetime] = UNSET,
    pension_id: Union[Unset, None, str] = UNSET,
    worker_group_id: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/employees/{employeeId}/autoenrolment/state".format(
        client.base_url, employerId=employer_id, employeeId=employee_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_state: Union[Unset, None, str] = UNSET
    if not isinstance(state, Unset):
        json_state = state.value if state else None

    params["state"] = json_state

    json_status: Union[Unset, None, str] = UNSET
    if not isinstance(status, Unset):
        json_status = status.value if status else None

    params["status"] = json_status

    json_state_date: Union[Unset, None, str] = UNSET
    if not isinstance(state_date, Unset):
        json_state_date = state_date.isoformat() if state_date else None

    params["stateDate"] = json_state_date

    params["pensionId"] = pension_id

    params["workerGroupId"] = worker_group_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[AeAssessment, Any]]:
    if response.status_code == 201:
        response_201 = AeAssessment.from_dict(response.json())

        return response_201
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[AeAssessment, Any]]:
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
    state: Union[Unset, None, AeEmployeeState] = UNSET,
    status: Union[Unset, None, AeStatus] = UNSET,
    state_date: Union[Unset, None, datetime.datetime] = UNSET,
    pension_id: Union[Unset, None, str] = UNSET,
    worker_group_id: Union[Unset, None, str] = UNSET,
) -> Response[Union[AeAssessment, Any]]:
    """Update State

     Updates the AutoEnrolment state for an Employee.
    You would use this API call to process notices such as Opt Out, Opt In, etc.
    A new assessment is returned showing the result of the state change.

    Args:
        employer_id (str):
        employee_id (str):
        state (Union[Unset, None, AeEmployeeState]):
        status (Union[Unset, None, AeStatus]):
        state_date (Union[Unset, None, datetime.datetime]):
        pension_id (Union[Unset, None, str]):
        worker_group_id (Union[Unset, None, str]):

    Returns:
        Response[Union[AeAssessment, Any]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        client=client,
        state=state,
        status=status,
        state_date=state_date,
        pension_id=pension_id,
        worker_group_id=worker_group_id,
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
    state: Union[Unset, None, AeEmployeeState] = UNSET,
    status: Union[Unset, None, AeStatus] = UNSET,
    state_date: Union[Unset, None, datetime.datetime] = UNSET,
    pension_id: Union[Unset, None, str] = UNSET,
    worker_group_id: Union[Unset, None, str] = UNSET,
) -> Optional[Union[AeAssessment, Any]]:
    """Update State

     Updates the AutoEnrolment state for an Employee.
    You would use this API call to process notices such as Opt Out, Opt In, etc.
    A new assessment is returned showing the result of the state change.

    Args:
        employer_id (str):
        employee_id (str):
        state (Union[Unset, None, AeEmployeeState]):
        status (Union[Unset, None, AeStatus]):
        state_date (Union[Unset, None, datetime.datetime]):
        pension_id (Union[Unset, None, str]):
        worker_group_id (Union[Unset, None, str]):

    Returns:
        Response[Union[AeAssessment, Any]]
    """

    return sync_detailed(
        employer_id=employer_id,
        employee_id=employee_id,
        client=client,
        state=state,
        status=status,
        state_date=state_date,
        pension_id=pension_id,
        worker_group_id=worker_group_id,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
    state: Union[Unset, None, AeEmployeeState] = UNSET,
    status: Union[Unset, None, AeStatus] = UNSET,
    state_date: Union[Unset, None, datetime.datetime] = UNSET,
    pension_id: Union[Unset, None, str] = UNSET,
    worker_group_id: Union[Unset, None, str] = UNSET,
) -> Response[Union[AeAssessment, Any]]:
    """Update State

     Updates the AutoEnrolment state for an Employee.
    You would use this API call to process notices such as Opt Out, Opt In, etc.
    A new assessment is returned showing the result of the state change.

    Args:
        employer_id (str):
        employee_id (str):
        state (Union[Unset, None, AeEmployeeState]):
        status (Union[Unset, None, AeStatus]):
        state_date (Union[Unset, None, datetime.datetime]):
        pension_id (Union[Unset, None, str]):
        worker_group_id (Union[Unset, None, str]):

    Returns:
        Response[Union[AeAssessment, Any]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        client=client,
        state=state,
        status=status,
        state_date=state_date,
        pension_id=pension_id,
        worker_group_id=worker_group_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
    state: Union[Unset, None, AeEmployeeState] = UNSET,
    status: Union[Unset, None, AeStatus] = UNSET,
    state_date: Union[Unset, None, datetime.datetime] = UNSET,
    pension_id: Union[Unset, None, str] = UNSET,
    worker_group_id: Union[Unset, None, str] = UNSET,
) -> Optional[Union[AeAssessment, Any]]:
    """Update State

     Updates the AutoEnrolment state for an Employee.
    You would use this API call to process notices such as Opt Out, Opt In, etc.
    A new assessment is returned showing the result of the state change.

    Args:
        employer_id (str):
        employee_id (str):
        state (Union[Unset, None, AeEmployeeState]):
        status (Union[Unset, None, AeStatus]):
        state_date (Union[Unset, None, datetime.datetime]):
        pension_id (Union[Unset, None, str]):
        worker_group_id (Union[Unset, None, str]):

    Returns:
        Response[Union[AeAssessment, Any]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            employee_id=employee_id,
            client=client,
            state=state,
            status=status,
            state_date=state_date,
            pension_id=pension_id,
            worker_group_id=worker_group_id,
        )
    ).parsed
