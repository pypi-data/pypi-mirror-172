from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.pension import Pension
from ...types import Response


def _get_kwargs(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
    json_body: Pension,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/employees/{employeeId}/pension".format(
        client.base_url, employerId=employer_id, employeeId=employee_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, Pension]]:
    if response.status_code == 200:
        response_200 = Pension.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, Pension]]:
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
    json_body: Pension,
) -> Response[Union[Any, Pension]]:
    """Update Pension

     Updates the Pension for an Employee.

    Args:
        employer_id (str):
        employee_id (str):
        json_body (Pension):

    Returns:
        Response[Union[Any, Pension]]
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


def sync(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
    json_body: Pension,
) -> Optional[Union[Any, Pension]]:
    """Update Pension

     Updates the Pension for an Employee.

    Args:
        employer_id (str):
        employee_id (str):
        json_body (Pension):

    Returns:
        Response[Union[Any, Pension]]
    """

    return sync_detailed(
        employer_id=employer_id,
        employee_id=employee_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
    json_body: Pension,
) -> Response[Union[Any, Pension]]:
    """Update Pension

     Updates the Pension for an Employee.

    Args:
        employer_id (str):
        employee_id (str):
        json_body (Pension):

    Returns:
        Response[Union[Any, Pension]]
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


async def asyncio(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
    json_body: Pension,
) -> Optional[Union[Any, Pension]]:
    """Update Pension

     Updates the Pension for an Employee.

    Args:
        employer_id (str):
        employee_id (str):
        json_body (Pension):

    Returns:
        Response[Union[Any, Pension]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            employee_id=employee_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
