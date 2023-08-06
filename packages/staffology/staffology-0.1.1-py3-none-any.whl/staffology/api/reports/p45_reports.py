from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.report_response import ReportResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    *,
    client: Client,
    employee_id: Union[Unset, None, str] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/reports/p45".format(
        client.base_url, employerId=employer_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(accept, Unset):
        headers["accept"] = accept

    params: Dict[str, Any] = {}
    params["employeeId"] = employee_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[ReportResponse]:
    if response.status_code == 200:
        response_200 = ReportResponse.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[ReportResponse]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    *,
    client: Client,
    employee_id: Union[Unset, None, str] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Response[ReportResponse]:
    """P45 For Employee

     Get a P45 for an Employee you've marked as a leaver

    Args:
        employer_id (str):
        employee_id (Union[Unset, None, str]):
        accept (Union[Unset, str]):

    Returns:
        Response[ReportResponse]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        employee_id=employee_id,
        accept=accept,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    employer_id: str,
    *,
    client: Client,
    employee_id: Union[Unset, None, str] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Optional[ReportResponse]:
    """P45 For Employee

     Get a P45 for an Employee you've marked as a leaver

    Args:
        employer_id (str):
        employee_id (Union[Unset, None, str]):
        accept (Union[Unset, str]):

    Returns:
        Response[ReportResponse]
    """

    return sync_detailed(
        employer_id=employer_id,
        client=client,
        employee_id=employee_id,
        accept=accept,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    *,
    client: Client,
    employee_id: Union[Unset, None, str] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Response[ReportResponse]:
    """P45 For Employee

     Get a P45 for an Employee you've marked as a leaver

    Args:
        employer_id (str):
        employee_id (Union[Unset, None, str]):
        accept (Union[Unset, str]):

    Returns:
        Response[ReportResponse]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        employee_id=employee_id,
        accept=accept,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    *,
    client: Client,
    employee_id: Union[Unset, None, str] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Optional[ReportResponse]:
    """P45 For Employee

     Get a P45 for an Employee you've marked as a leaver

    Args:
        employer_id (str):
        employee_id (Union[Unset, None, str]):
        accept (Union[Unset, str]):

    Returns:
        Response[ReportResponse]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            client=client,
            employee_id=employee_id,
            accept=accept,
        )
    ).parsed
