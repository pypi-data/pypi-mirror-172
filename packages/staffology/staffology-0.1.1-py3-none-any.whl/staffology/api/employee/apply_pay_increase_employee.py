from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    *,
    client: Client,
    percentage: Union[Unset, None, float] = UNSET,
    all_employees: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/employees/payincrease".format(
        client.base_url, employerId=employer_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["percentage"] = percentage

    params["allEmployees"] = all_employees

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "put",
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
    *,
    client: Client,
    percentage: Union[Unset, None, float] = UNSET,
    all_employees: Union[Unset, None, bool] = UNSET,
) -> Response[Any]:
    """Apply Pay Increase

     Increases the PayOptions.PayAmount and PayOptions.BaseHourlyRate by the percentage given.

    Args:
        employer_id (str):
        percentage (Union[Unset, None, float]):
        all_employees (Union[Unset, None, bool]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        percentage=percentage,
        all_employees=all_employees,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    employer_id: str,
    *,
    client: Client,
    percentage: Union[Unset, None, float] = UNSET,
    all_employees: Union[Unset, None, bool] = UNSET,
) -> Response[Any]:
    """Apply Pay Increase

     Increases the PayOptions.PayAmount and PayOptions.BaseHourlyRate by the percentage given.

    Args:
        employer_id (str):
        percentage (Union[Unset, None, float]):
        all_employees (Union[Unset, None, bool]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        percentage=percentage,
        all_employees=all_employees,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
