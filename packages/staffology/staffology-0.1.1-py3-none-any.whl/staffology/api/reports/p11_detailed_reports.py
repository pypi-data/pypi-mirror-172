from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.p11_detailed_report_response import P11DetailedReportResponse
from ...models.tax_year import TaxYear
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    tax_year: TaxYear,
    employee_id: str,
    *,
    client: Client,
    accept: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/reports/{taxYear}/{employeeId}/p11detailed".format(
        client.base_url,
        employerId=employer_id,
        taxYear=tax_year,
        employeeId=employee_id,
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


def _parse_response(*, response: httpx.Response) -> Optional[P11DetailedReportResponse]:
    if response.status_code == 200:
        response_200 = P11DetailedReportResponse.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[P11DetailedReportResponse]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    tax_year: TaxYear,
    employee_id: str,
    *,
    client: Client,
    accept: Union[Unset, str] = UNSET,
) -> Response[P11DetailedReportResponse]:
    """P11 (Detailed)

     Returns a detailed P11 Report for the given employee.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        employee_id (str):
        accept (Union[Unset, str]):

    Returns:
        Response[P11DetailedReportResponse]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        employee_id=employee_id,
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
    tax_year: TaxYear,
    employee_id: str,
    *,
    client: Client,
    accept: Union[Unset, str] = UNSET,
) -> Optional[P11DetailedReportResponse]:
    """P11 (Detailed)

     Returns a detailed P11 Report for the given employee.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        employee_id (str):
        accept (Union[Unset, str]):

    Returns:
        Response[P11DetailedReportResponse]
    """

    return sync_detailed(
        employer_id=employer_id,
        tax_year=tax_year,
        employee_id=employee_id,
        client=client,
        accept=accept,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    tax_year: TaxYear,
    employee_id: str,
    *,
    client: Client,
    accept: Union[Unset, str] = UNSET,
) -> Response[P11DetailedReportResponse]:
    """P11 (Detailed)

     Returns a detailed P11 Report for the given employee.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        employee_id (str):
        accept (Union[Unset, str]):

    Returns:
        Response[P11DetailedReportResponse]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        employee_id=employee_id,
        client=client,
        accept=accept,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    tax_year: TaxYear,
    employee_id: str,
    *,
    client: Client,
    accept: Union[Unset, str] = UNSET,
) -> Optional[P11DetailedReportResponse]:
    """P11 (Detailed)

     Returns a detailed P11 Report for the given employee.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        employee_id (str):
        accept (Union[Unset, str]):

    Returns:
        Response[P11DetailedReportResponse]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            tax_year=tax_year,
            employee_id=employee_id,
            client=client,
            accept=accept,
        )
    ).parsed
