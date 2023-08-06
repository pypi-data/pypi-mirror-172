from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...models.external_data_provider_id import ExternalDataProviderId
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    id: ExternalDataProviderId,
    *,
    client: Client,
    employee_id: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/external-data/{id}/p45".format(
        client.base_url, employerId=employer_id, id=id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["employeeId"] = employee_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
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
    id: ExternalDataProviderId,
    *,
    client: Client,
    employee_id: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """Push P45

     Push a P45 to the ExternalDataProvider.

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        employee_id (Union[Unset, None, str]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        client=client,
        employee_id=employee_id,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    employer_id: str,
    id: ExternalDataProviderId,
    *,
    client: Client,
    employee_id: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """Push P45

     Push a P45 to the ExternalDataProvider.

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        employee_id (Union[Unset, None, str]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        client=client,
        employee_id=employee_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
