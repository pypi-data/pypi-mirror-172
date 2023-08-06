from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.external_data_provider_id import ExternalDataProviderId
from ...models.external_employee_mapping import ExternalEmployeeMapping
from ...types import Response


def _get_kwargs(
    employer_id: str,
    id: ExternalDataProviderId,
    employee_id: str,
    *,
    client: Client,
    json_body: ExternalEmployeeMapping,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/external-data/{id}/employees/{employeeId}".format(
        client.base_url, employerId=employer_id, id=id, employeeId=employee_id
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


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[Any, ExternalEmployeeMapping]]:
    if response.status_code == 200:
        response_200 = ExternalEmployeeMapping.from_dict(response.json())

        return response_200
    if response.status_code == 409:
        response_409 = cast(Any, None)
        return response_409
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[Any, ExternalEmployeeMapping]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    id: ExternalDataProviderId,
    employee_id: str,
    *,
    client: Client,
    json_body: ExternalEmployeeMapping,
) -> Response[Union[Any, ExternalEmployeeMapping]]:
    """Update Employee

     Update an ExternalEmployeeMapping to map/unmap/import/ignore an employee from an external data
    provider

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        employee_id (str):
        json_body (ExternalEmployeeMapping): Used to represent details of an employee from an
            ExternalDataProvider, along with mapping information to an employee in the payroll system

    Returns:
        Response[Union[Any, ExternalEmployeeMapping]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
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
    id: ExternalDataProviderId,
    employee_id: str,
    *,
    client: Client,
    json_body: ExternalEmployeeMapping,
) -> Optional[Union[Any, ExternalEmployeeMapping]]:
    """Update Employee

     Update an ExternalEmployeeMapping to map/unmap/import/ignore an employee from an external data
    provider

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        employee_id (str):
        json_body (ExternalEmployeeMapping): Used to represent details of an employee from an
            ExternalDataProvider, along with mapping information to an employee in the payroll system

    Returns:
        Response[Union[Any, ExternalEmployeeMapping]]
    """

    return sync_detailed(
        employer_id=employer_id,
        id=id,
        employee_id=employee_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    id: ExternalDataProviderId,
    employee_id: str,
    *,
    client: Client,
    json_body: ExternalEmployeeMapping,
) -> Response[Union[Any, ExternalEmployeeMapping]]:
    """Update Employee

     Update an ExternalEmployeeMapping to map/unmap/import/ignore an employee from an external data
    provider

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        employee_id (str):
        json_body (ExternalEmployeeMapping): Used to represent details of an employee from an
            ExternalDataProvider, along with mapping information to an employee in the payroll system

    Returns:
        Response[Union[Any, ExternalEmployeeMapping]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        employee_id=employee_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    id: ExternalDataProviderId,
    employee_id: str,
    *,
    client: Client,
    json_body: ExternalEmployeeMapping,
) -> Optional[Union[Any, ExternalEmployeeMapping]]:
    """Update Employee

     Update an ExternalEmployeeMapping to map/unmap/import/ignore an employee from an external data
    provider

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        employee_id (str):
        json_body (ExternalEmployeeMapping): Used to represent details of an employee from an
            ExternalDataProvider, along with mapping information to an employee in the payroll system

    Returns:
        Response[Union[Any, ExternalEmployeeMapping]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            id=id,
            employee_id=employee_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
