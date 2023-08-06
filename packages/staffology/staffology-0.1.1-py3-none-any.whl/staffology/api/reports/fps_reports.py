from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.fps_report_response import FpsReportResponse
from ...models.tax_year import TaxYear
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    tax_year: TaxYear,
    id: str,
    *,
    client: Client,
    inc_all_employees: Union[Unset, None, bool] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/reports/{taxYear}/fps/{id}".format(
        client.base_url, employerId=employer_id, taxYear=tax_year, id=id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(accept, Unset):
        headers["accept"] = accept

    params: Dict[str, Any] = {}
    params["incAllEmployees"] = inc_all_employees

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[FpsReportResponse]:
    if response.status_code == 200:
        response_200 = FpsReportResponse.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[FpsReportResponse]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    tax_year: TaxYear,
    id: str,
    *,
    client: Client,
    inc_all_employees: Union[Unset, None, bool] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Response[FpsReportResponse]:
    """FPS

     Returns an FPS as a CSV file

    Args:
        employer_id (str):
        tax_year (TaxYear):
        id (str):
        inc_all_employees (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[FpsReportResponse]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        id=id,
        client=client,
        inc_all_employees=inc_all_employees,
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
    id: str,
    *,
    client: Client,
    inc_all_employees: Union[Unset, None, bool] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Optional[FpsReportResponse]:
    """FPS

     Returns an FPS as a CSV file

    Args:
        employer_id (str):
        tax_year (TaxYear):
        id (str):
        inc_all_employees (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[FpsReportResponse]
    """

    return sync_detailed(
        employer_id=employer_id,
        tax_year=tax_year,
        id=id,
        client=client,
        inc_all_employees=inc_all_employees,
        accept=accept,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    tax_year: TaxYear,
    id: str,
    *,
    client: Client,
    inc_all_employees: Union[Unset, None, bool] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Response[FpsReportResponse]:
    """FPS

     Returns an FPS as a CSV file

    Args:
        employer_id (str):
        tax_year (TaxYear):
        id (str):
        inc_all_employees (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[FpsReportResponse]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        id=id,
        client=client,
        inc_all_employees=inc_all_employees,
        accept=accept,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    tax_year: TaxYear,
    id: str,
    *,
    client: Client,
    inc_all_employees: Union[Unset, None, bool] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Optional[FpsReportResponse]:
    """FPS

     Returns an FPS as a CSV file

    Args:
        employer_id (str):
        tax_year (TaxYear):
        id (str):
        inc_all_employees (Union[Unset, None, bool]):
        accept (Union[Unset, str]):

    Returns:
        Response[FpsReportResponse]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            tax_year=tax_year,
            id=id,
            client=client,
            inc_all_employees=inc_all_employees,
            accept=accept,
        )
    ).parsed
