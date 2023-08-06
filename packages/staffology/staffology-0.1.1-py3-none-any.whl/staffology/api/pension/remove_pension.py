from typing import Any, Dict

import httpx

from ...client import Client
from ...types import Response


def _get_kwargs(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/employees/{employeeId}/pension".format(
        client.base_url, employerId=employer_id, employeeId=employee_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "delete",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
) -> Response[Any]:
    """Remove Pension

     Removes the Pension for an Employee.
    For Non-AE Pensions, this is the same as an Update with an empty JSON object.
    For AE Pensions this will remove the employee from the pension and delete any associated
    AeAssessments

    Args:
        employer_id (str):
        employee_id (str):

    Returns:
        Response[Any]
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


async def asyncio_detailed(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
) -> Response[Any]:
    """Remove Pension

     Removes the Pension for an Employee.
    For Non-AE Pensions, this is the same as an Update with an empty JSON object.
    For AE Pensions this will remove the employee from the pension and delete any associated
    AeAssessments

    Args:
        employer_id (str):
        employee_id (str):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
