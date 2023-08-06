from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.cis_statement_list_report_response import CisStatementListReportResponse
from ...models.tax_year import TaxYear
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    tax_year: TaxYear,
    tax_month: int,
    *,
    client: Client,
    employee_id: Union[Unset, None, str] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/reports/{taxYear}/cisstatement/{taxMonth}".format(
        client.base_url, employerId=employer_id, taxYear=tax_year, taxMonth=tax_month
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


def _parse_response(
    *, response: httpx.Response
) -> Optional[CisStatementListReportResponse]:
    if response.status_code == 200:
        response_200 = CisStatementListReportResponse.from_dict(response.json())

        return response_200
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[CisStatementListReportResponse]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    tax_year: TaxYear,
    tax_month: int,
    *,
    client: Client,
    employee_id: Union[Unset, None, str] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Response[CisStatementListReportResponse]:
    """CIS Statement

     Returns a CIS Statement for the employee specified.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        tax_month (int):
        employee_id (Union[Unset, None, str]):
        accept (Union[Unset, str]):

    Returns:
        Response[CisStatementListReportResponse]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        tax_month=tax_month,
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
    tax_year: TaxYear,
    tax_month: int,
    *,
    client: Client,
    employee_id: Union[Unset, None, str] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Optional[CisStatementListReportResponse]:
    """CIS Statement

     Returns a CIS Statement for the employee specified.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        tax_month (int):
        employee_id (Union[Unset, None, str]):
        accept (Union[Unset, str]):

    Returns:
        Response[CisStatementListReportResponse]
    """

    return sync_detailed(
        employer_id=employer_id,
        tax_year=tax_year,
        tax_month=tax_month,
        client=client,
        employee_id=employee_id,
        accept=accept,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    tax_year: TaxYear,
    tax_month: int,
    *,
    client: Client,
    employee_id: Union[Unset, None, str] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Response[CisStatementListReportResponse]:
    """CIS Statement

     Returns a CIS Statement for the employee specified.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        tax_month (int):
        employee_id (Union[Unset, None, str]):
        accept (Union[Unset, str]):

    Returns:
        Response[CisStatementListReportResponse]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        tax_month=tax_month,
        client=client,
        employee_id=employee_id,
        accept=accept,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    tax_year: TaxYear,
    tax_month: int,
    *,
    client: Client,
    employee_id: Union[Unset, None, str] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Optional[CisStatementListReportResponse]:
    """CIS Statement

     Returns a CIS Statement for the employee specified.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        tax_month (int):
        employee_id (Union[Unset, None, str]):
        accept (Union[Unset, str]):

    Returns:
        Response[CisStatementListReportResponse]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            tax_year=tax_year,
            tax_month=tax_month,
            client=client,
            employee_id=employee_id,
            accept=accept,
        )
    ).parsed
