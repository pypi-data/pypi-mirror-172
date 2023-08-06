from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.report_response import ReportResponse
from ...models.tax_year import TaxYear
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    employer_id: Union[Unset, None, str] = UNSET,
    tax_year: Union[Unset, None, TaxYear] = UNSET,
    include_bank_account_details: Union[Unset, None, bool] = UNSET,
    include_ytd: Union[Unset, None, bool] = UNSET,
    inc_pension_info: Union[Unset, None, bool] = UNSET,
    include_pay_info: Union[Unset, None, bool] = UNSET,
    include_notes: Union[Unset, None, bool] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employees".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(accept, Unset):
        headers["accept"] = accept

    params: Dict[str, Any] = {}
    params["employerId"] = employer_id

    json_tax_year: Union[Unset, None, str] = UNSET
    if not isinstance(tax_year, Unset):
        json_tax_year = tax_year.value if tax_year else None

    params["taxYear"] = json_tax_year

    params["includeBankAccountDetails"] = include_bank_account_details

    params["includeYtd"] = include_ytd

    params["incPensionInfo"] = inc_pension_info

    params["includePayInfo"] = include_pay_info

    params["includeNotes"] = include_notes

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
    *,
    client: Client,
    employer_id: Union[Unset, None, str] = UNSET,
    tax_year: Union[Unset, None, TaxYear] = UNSET,
    include_bank_account_details: Union[Unset, None, bool] = UNSET,
    include_ytd: Union[Unset, None, bool] = UNSET,
    inc_pension_info: Union[Unset, None, bool] = UNSET,
    include_pay_info: Union[Unset, None, bool] = UNSET,
    include_notes: Union[Unset, None, bool] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Response[ReportResponse]:
    """Employee Export Details

     Returns a CSV file containing details for all Employees.

    Args:
        employer_id (Union[Unset, None, str]):
        tax_year (Union[Unset, None, TaxYear]):
        include_bank_account_details (Union[Unset, None, bool]):
        include_ytd (Union[Unset, None, bool]):
        inc_pension_info (Union[Unset, None, bool]):
        include_pay_info (Union[Unset, None, bool]):
        include_notes (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[ReportResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        employer_id=employer_id,
        tax_year=tax_year,
        include_bank_account_details=include_bank_account_details,
        include_ytd=include_ytd,
        inc_pension_info=inc_pension_info,
        include_pay_info=include_pay_info,
        include_notes=include_notes,
        accept=accept,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    employer_id: Union[Unset, None, str] = UNSET,
    tax_year: Union[Unset, None, TaxYear] = UNSET,
    include_bank_account_details: Union[Unset, None, bool] = UNSET,
    include_ytd: Union[Unset, None, bool] = UNSET,
    inc_pension_info: Union[Unset, None, bool] = UNSET,
    include_pay_info: Union[Unset, None, bool] = UNSET,
    include_notes: Union[Unset, None, bool] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Optional[ReportResponse]:
    """Employee Export Details

     Returns a CSV file containing details for all Employees.

    Args:
        employer_id (Union[Unset, None, str]):
        tax_year (Union[Unset, None, TaxYear]):
        include_bank_account_details (Union[Unset, None, bool]):
        include_ytd (Union[Unset, None, bool]):
        inc_pension_info (Union[Unset, None, bool]):
        include_pay_info (Union[Unset, None, bool]):
        include_notes (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[ReportResponse]
    """

    return sync_detailed(
        client=client,
        employer_id=employer_id,
        tax_year=tax_year,
        include_bank_account_details=include_bank_account_details,
        include_ytd=include_ytd,
        inc_pension_info=inc_pension_info,
        include_pay_info=include_pay_info,
        include_notes=include_notes,
        accept=accept,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    employer_id: Union[Unset, None, str] = UNSET,
    tax_year: Union[Unset, None, TaxYear] = UNSET,
    include_bank_account_details: Union[Unset, None, bool] = UNSET,
    include_ytd: Union[Unset, None, bool] = UNSET,
    inc_pension_info: Union[Unset, None, bool] = UNSET,
    include_pay_info: Union[Unset, None, bool] = UNSET,
    include_notes: Union[Unset, None, bool] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Response[ReportResponse]:
    """Employee Export Details

     Returns a CSV file containing details for all Employees.

    Args:
        employer_id (Union[Unset, None, str]):
        tax_year (Union[Unset, None, TaxYear]):
        include_bank_account_details (Union[Unset, None, bool]):
        include_ytd (Union[Unset, None, bool]):
        inc_pension_info (Union[Unset, None, bool]):
        include_pay_info (Union[Unset, None, bool]):
        include_notes (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[ReportResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        employer_id=employer_id,
        tax_year=tax_year,
        include_bank_account_details=include_bank_account_details,
        include_ytd=include_ytd,
        inc_pension_info=inc_pension_info,
        include_pay_info=include_pay_info,
        include_notes=include_notes,
        accept=accept,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    employer_id: Union[Unset, None, str] = UNSET,
    tax_year: Union[Unset, None, TaxYear] = UNSET,
    include_bank_account_details: Union[Unset, None, bool] = UNSET,
    include_ytd: Union[Unset, None, bool] = UNSET,
    inc_pension_info: Union[Unset, None, bool] = UNSET,
    include_pay_info: Union[Unset, None, bool] = UNSET,
    include_notes: Union[Unset, None, bool] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Optional[ReportResponse]:
    """Employee Export Details

     Returns a CSV file containing details for all Employees.

    Args:
        employer_id (Union[Unset, None, str]):
        tax_year (Union[Unset, None, TaxYear]):
        include_bank_account_details (Union[Unset, None, bool]):
        include_ytd (Union[Unset, None, bool]):
        inc_pension_info (Union[Unset, None, bool]):
        include_pay_info (Union[Unset, None, bool]):
        include_notes (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[ReportResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            employer_id=employer_id,
            tax_year=tax_year,
            include_bank_account_details=include_bank_account_details,
            include_ytd=include_ytd,
            inc_pension_info=inc_pension_info,
            include_pay_info=include_pay_info,
            include_notes=include_notes,
            accept=accept,
        )
    ).parsed
