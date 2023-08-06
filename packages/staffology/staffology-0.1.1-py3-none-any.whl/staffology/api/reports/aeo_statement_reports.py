from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.attachment_order_report_response import AttachmentOrderReportResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employee_id: str,
    id: str,
    *,
    client: Client,
    employer_id: Union[Unset, None, str] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/aeo/{employeeId}/{id}".format(
        client.base_url, employeeId=employee_id, id=id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(accept, Unset):
        headers["accept"] = accept

    params: Dict[str, Any] = {}
    params["employerId"] = employer_id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[AttachmentOrderReportResponse]:
    if response.status_code == 200:
        response_200 = AttachmentOrderReportResponse.from_dict(response.json())

        return response_200
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[AttachmentOrderReportResponse]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employee_id: str,
    id: str,
    *,
    client: Client,
    employer_id: Union[Unset, None, str] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Response[AttachmentOrderReportResponse]:
    """AEO Statement

     Returns a statement for an Attachment Order, listing payments that have been made.

    Args:
        employee_id (str):
        id (str):
        employer_id (Union[Unset, None, str]):
        accept (Union[Unset, str]):

    Returns:
        Response[AttachmentOrderReportResponse]
    """

    kwargs = _get_kwargs(
        employee_id=employee_id,
        id=id,
        client=client,
        employer_id=employer_id,
        accept=accept,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    employee_id: str,
    id: str,
    *,
    client: Client,
    employer_id: Union[Unset, None, str] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Optional[AttachmentOrderReportResponse]:
    """AEO Statement

     Returns a statement for an Attachment Order, listing payments that have been made.

    Args:
        employee_id (str):
        id (str):
        employer_id (Union[Unset, None, str]):
        accept (Union[Unset, str]):

    Returns:
        Response[AttachmentOrderReportResponse]
    """

    return sync_detailed(
        employee_id=employee_id,
        id=id,
        client=client,
        employer_id=employer_id,
        accept=accept,
    ).parsed


async def asyncio_detailed(
    employee_id: str,
    id: str,
    *,
    client: Client,
    employer_id: Union[Unset, None, str] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Response[AttachmentOrderReportResponse]:
    """AEO Statement

     Returns a statement for an Attachment Order, listing payments that have been made.

    Args:
        employee_id (str):
        id (str):
        employer_id (Union[Unset, None, str]):
        accept (Union[Unset, str]):

    Returns:
        Response[AttachmentOrderReportResponse]
    """

    kwargs = _get_kwargs(
        employee_id=employee_id,
        id=id,
        client=client,
        employer_id=employer_id,
        accept=accept,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employee_id: str,
    id: str,
    *,
    client: Client,
    employer_id: Union[Unset, None, str] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Optional[AttachmentOrderReportResponse]:
    """AEO Statement

     Returns a statement for an Attachment Order, listing payments that have been made.

    Args:
        employee_id (str):
        id (str):
        employer_id (Union[Unset, None, str]):
        accept (Union[Unset, str]):

    Returns:
        Response[AttachmentOrderReportResponse]
    """

    return (
        await asyncio_detailed(
            employee_id=employee_id,
            id=id,
            client=client,
            employer_id=employer_id,
            accept=accept,
        )
    ).parsed
