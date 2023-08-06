from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.item_list_report_response import ItemListReportResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    *,
    client: Client,
    accept: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/reports/AeAssessments".format(
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


def _parse_response(*, response: httpx.Response) -> Optional[ItemListReportResponse]:
    if response.status_code == 200:
        response_200 = ItemListReportResponse.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[ItemListReportResponse]:
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
) -> Response[ItemListReportResponse]:
    """AutoEnrolment Assessments

     Returns a list of Items representing your current Employees along with their most recent Auto
    Enrolment Assessment in the metadata field.

    Args:
        employer_id (str):
        accept (Union[Unset, str]):

    Returns:
        Response[ItemListReportResponse]
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
) -> Optional[ItemListReportResponse]:
    """AutoEnrolment Assessments

     Returns a list of Items representing your current Employees along with their most recent Auto
    Enrolment Assessment in the metadata field.

    Args:
        employer_id (str):
        accept (Union[Unset, str]):

    Returns:
        Response[ItemListReportResponse]
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
) -> Response[ItemListReportResponse]:
    """AutoEnrolment Assessments

     Returns a list of Items representing your current Employees along with their most recent Auto
    Enrolment Assessment in the metadata field.

    Args:
        employer_id (str):
        accept (Union[Unset, str]):

    Returns:
        Response[ItemListReportResponse]
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
) -> Optional[ItemListReportResponse]:
    """AutoEnrolment Assessments

     Returns a list of Items representing your current Employees along with their most recent Auto
    Enrolment Assessment in the metadata field.

    Args:
        employer_id (str):
        accept (Union[Unset, str]):

    Returns:
        Response[ItemListReportResponse]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            client=client,
            accept=accept,
        )
    ).parsed
