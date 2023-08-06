from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.pension import Pension
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
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[Pension]:
    if response.status_code == 200:
        response_200 = Pension.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Pension]:
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
) -> Response[Pension]:
    """Get Pension

     Returns the Pension, if any, for an Employee

    Args:
        employer_id (str):
        employee_id (str):

    Returns:
        Response[Pension]
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
) -> Optional[Pension]:
    """Get Pension

     Returns the Pension, if any, for an Employee

    Args:
        employer_id (str):
        employee_id (str):

    Returns:
        Response[Pension]
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
) -> Response[Pension]:
    """Get Pension

     Returns the Pension, if any, for an Employee

    Args:
        employer_id (str):
        employee_id (str):

    Returns:
        Response[Pension]
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
) -> Optional[Pension]:
    """Get Pension

     Returns the Pension, if any, for an Employee

    Args:
        employer_id (str):
        employee_id (str):

    Returns:
        Response[Pension]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            employee_id=employee_id,
            client=client,
        )
    ).parsed
