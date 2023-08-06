from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.external_data_provider_id import ExternalDataProviderId
from ...models.item import Item
from ...types import Response


def _get_kwargs(
    employer_id: str,
    id: ExternalDataProviderId,
    employee_id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/external-data/{id}/employees/{employeeId}/sync".format(
        client.base_url, employerId=employer_id, id=id, employeeId=employee_id
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, Item]]:
    if response.status_code == 200:
        response_200 = Item.from_dict(response.json())

        return response_200
    if response.status_code == 409:
        response_409 = cast(Any, None)
        return response_409
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, Item]]:
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
) -> Response[Union[Any, Item]]:
    """Sync Employee

     Syncs data from the ExternalDataProvider to update the specified mapped employee.
    Any changes made as a result of the sync are show in the metadata.logs property.

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        employee_id (str):

    Returns:
        Response[Union[Any, Item]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
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
    id: ExternalDataProviderId,
    employee_id: str,
    *,
    client: Client,
) -> Optional[Union[Any, Item]]:
    """Sync Employee

     Syncs data from the ExternalDataProvider to update the specified mapped employee.
    Any changes made as a result of the sync are show in the metadata.logs property.

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        employee_id (str):

    Returns:
        Response[Union[Any, Item]]
    """

    return sync_detailed(
        employer_id=employer_id,
        id=id,
        employee_id=employee_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    id: ExternalDataProviderId,
    employee_id: str,
    *,
    client: Client,
) -> Response[Union[Any, Item]]:
    """Sync Employee

     Syncs data from the ExternalDataProvider to update the specified mapped employee.
    Any changes made as a result of the sync are show in the metadata.logs property.

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        employee_id (str):

    Returns:
        Response[Union[Any, Item]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        employee_id=employee_id,
        client=client,
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
) -> Optional[Union[Any, Item]]:
    """Sync Employee

     Syncs data from the ExternalDataProvider to update the specified mapped employee.
    Any changes made as a result of the sync are show in the metadata.logs property.

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        employee_id (str):

    Returns:
        Response[Union[Any, Item]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            id=id,
            employee_id=employee_id,
            client=client,
        )
    ).parsed
