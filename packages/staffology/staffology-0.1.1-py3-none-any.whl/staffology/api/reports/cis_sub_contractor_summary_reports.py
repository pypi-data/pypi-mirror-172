from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.cis_sub_contractor_summary_list_report_response import (
    CisSubContractorSummaryListReportResponse,
)
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    *,
    client: Client,
    accept: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/reports/cissummary".format(
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
) -> Optional[CisSubContractorSummaryListReportResponse]:
    if response.status_code == 200:
        response_200 = CisSubContractorSummaryListReportResponse.from_dict(
            response.text
        )

        return response_200
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[CisSubContractorSummaryListReportResponse]:
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
) -> Response[CisSubContractorSummaryListReportResponse]:
    """CIS Subcontractor Summary

     Returns a list of all CIS Subcontractors along with verification details

    Args:
        employer_id (str):
        accept (Union[Unset, str]):

    Returns:
        Response[CisSubContractorSummaryListReportResponse]
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
) -> Optional[CisSubContractorSummaryListReportResponse]:
    """CIS Subcontractor Summary

     Returns a list of all CIS Subcontractors along with verification details

    Args:
        employer_id (str):
        accept (Union[Unset, str]):

    Returns:
        Response[CisSubContractorSummaryListReportResponse]
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
) -> Response[CisSubContractorSummaryListReportResponse]:
    """CIS Subcontractor Summary

     Returns a list of all CIS Subcontractors along with verification details

    Args:
        employer_id (str):
        accept (Union[Unset, str]):

    Returns:
        Response[CisSubContractorSummaryListReportResponse]
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
) -> Optional[CisSubContractorSummaryListReportResponse]:
    """CIS Subcontractor Summary

     Returns a list of all CIS Subcontractors along with verification details

    Args:
        employer_id (str):
        accept (Union[Unset, str]):

    Returns:
        Response[CisSubContractorSummaryListReportResponse]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            client=client,
            accept=accept,
        )
    ).parsed
