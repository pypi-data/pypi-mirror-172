from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.right_to_work_report_report_response import (
    RightToWorkReportReportResponse,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    *,
    client: Client,
    accept: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/reports/right-to-work".format(
        client.base_url, employerId=employer_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(accept, Unset):
        headers["accept"] = accept

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[RightToWorkReportReportResponse]:
    if response.status_code == 200:
        response_200 = RightToWorkReportReportResponse.from_dict(response.json())

        return response_200
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[RightToWorkReportReportResponse]:
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
    accept: Union[Unset, str] = UNSET,
) -> Response[RightToWorkReportReportResponse]:
    """RightToWork

     Returns a report summarising RightToWork information for all employees.

    Args:
        employer_id (str):
        accept (Union[Unset, str]):

    Returns:
        Response[RightToWorkReportReportResponse]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
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
    accept: Union[Unset, str] = UNSET,
) -> Optional[RightToWorkReportReportResponse]:
    """RightToWork

     Returns a report summarising RightToWork information for all employees.

    Args:
        employer_id (str):
        accept (Union[Unset, str]):

    Returns:
        Response[RightToWorkReportReportResponse]
    """

    return sync_detailed(
        employer_id=employer_id,
        client=client,
        accept=accept,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    *,
    client: Client,
    accept: Union[Unset, str] = UNSET,
) -> Response[RightToWorkReportReportResponse]:
    """RightToWork

     Returns a report summarising RightToWork information for all employees.

    Args:
        employer_id (str):
        accept (Union[Unset, str]):

    Returns:
        Response[RightToWorkReportReportResponse]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        accept=accept,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    *,
    client: Client,
    accept: Union[Unset, str] = UNSET,
) -> Optional[RightToWorkReportReportResponse]:
    """RightToWork

     Returns a report summarising RightToWork information for all employees.

    Args:
        employer_id (str):
        accept (Union[Unset, str]):

    Returns:
        Response[RightToWorkReportReportResponse]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            client=client,
            accept=accept,
        )
    ).parsed
