from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.pay_run_entry import PayRunEntry
from ...types import Response


def _get_kwargs(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/payrun/employees/{employeeId}/Last".format(
        client.base_url, employerId=employer_id, employeeId=employee_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[PayRunEntry]:
    if response.status_code == 200:
        response_200 = PayRunEntry.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[PayRunEntry]:
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
) -> Response[PayRunEntry]:
    """Gets the last closed pay run entry for an employee.

    Args:
        employer_id (str):
        employee_id (str):

    Returns:
        Response[PayRunEntry]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        client=client,
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
) -> Optional[PayRunEntry]:
    """Gets the last closed pay run entry for an employee.

    Args:
        employer_id (str):
        employee_id (str):

    Returns:
        Response[PayRunEntry]
    """

    return sync_detailed(
        employer_id=employer_id,
        employee_id=employee_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
) -> Response[PayRunEntry]:
    """Gets the last closed pay run entry for an employee.

    Args:
        employer_id (str):
        employee_id (str):

    Returns:
        Response[PayRunEntry]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
) -> Optional[PayRunEntry]:
    """Gets the last closed pay run entry for an employee.

    Args:
        employer_id (str):
        employee_id (str):

    Returns:
        Response[PayRunEntry]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            employee_id=employee_id,
            client=client,
        )
    ).parsed
