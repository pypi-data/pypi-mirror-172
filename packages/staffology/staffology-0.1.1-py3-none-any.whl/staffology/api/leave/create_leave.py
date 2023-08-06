from typing import Any, Dict

import httpx

from ...client import Client
from ...models.leave import Leave
from ...types import Response


def _get_kwargs(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
    json_body: Leave,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/employees/{employeeId}/leave".format(
        client.base_url, employerId=employer_id, employeeId=employee_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
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
    json_body: Leave,
) -> Response[Any]:
    """Create Leave

     Creates Leave for the Employee

    Args:
        employer_id (str):
        employee_id (str):
        json_body (Leave): Used to represent Leave, including Holiday and Statutory leave (such as
            Maternity Leave)

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        client=client,
        json_body=json_body,
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
    json_body: Leave,
) -> Response[Any]:
    """Create Leave

     Creates Leave for the Employee

    Args:
        employer_id (str):
        employee_id (str):
        json_body (Leave): Used to represent Leave, including Holiday and Statutory leave (such as
            Maternity Leave)

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
