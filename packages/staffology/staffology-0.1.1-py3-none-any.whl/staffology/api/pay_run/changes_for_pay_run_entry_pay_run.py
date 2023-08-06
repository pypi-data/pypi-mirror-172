from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.change_summary import ChangeSummary
from ...models.pay_periods import PayPeriods
from ...models.tax_year import TaxYear
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    id: str,
    *,
    client: Client,
    ordinal: Union[Unset, None, int] = 1,
    significant_changes_only: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/payrun/{taxYear}/{payPeriod}/{periodNumber}/{id}/changes".format(
        client.base_url,
        employerId=employer_id,
        taxYear=tax_year,
        payPeriod=pay_period,
        periodNumber=period_number,
        id=id,
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["ordinal"] = ordinal

    params["significantChangesOnly"] = significant_changes_only

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[List[ChangeSummary]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ChangeSummary.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[List[ChangeSummary]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    id: str,
    *,
    client: Client,
    ordinal: Union[Unset, None, int] = 1,
    significant_changes_only: Union[Unset, None, bool] = False,
) -> Response[List[ChangeSummary]]:
    """List PayRun Changes for PayRunEntry

     Returns a list of AuditEntry reflecting changes made to a PayRunEntry and related employee record
    for a given PayRun
    This endpoint is currently being beta tested and subject to un-announced breaking changes.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        id (str):
        ordinal (Union[Unset, None, int]):  Default: 1.
        significant_changes_only (Union[Unset, None, bool]):

    Returns:
        Response[List[ChangeSummary]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        id=id,
        client=client,
        ordinal=ordinal,
        significant_changes_only=significant_changes_only,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    id: str,
    *,
    client: Client,
    ordinal: Union[Unset, None, int] = 1,
    significant_changes_only: Union[Unset, None, bool] = False,
) -> Optional[List[ChangeSummary]]:
    """List PayRun Changes for PayRunEntry

     Returns a list of AuditEntry reflecting changes made to a PayRunEntry and related employee record
    for a given PayRun
    This endpoint is currently being beta tested and subject to un-announced breaking changes.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        id (str):
        ordinal (Union[Unset, None, int]):  Default: 1.
        significant_changes_only (Union[Unset, None, bool]):

    Returns:
        Response[List[ChangeSummary]]
    """

    return sync_detailed(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        id=id,
        client=client,
        ordinal=ordinal,
        significant_changes_only=significant_changes_only,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    id: str,
    *,
    client: Client,
    ordinal: Union[Unset, None, int] = 1,
    significant_changes_only: Union[Unset, None, bool] = False,
) -> Response[List[ChangeSummary]]:
    """List PayRun Changes for PayRunEntry

     Returns a list of AuditEntry reflecting changes made to a PayRunEntry and related employee record
    for a given PayRun
    This endpoint is currently being beta tested and subject to un-announced breaking changes.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        id (str):
        ordinal (Union[Unset, None, int]):  Default: 1.
        significant_changes_only (Union[Unset, None, bool]):

    Returns:
        Response[List[ChangeSummary]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        id=id,
        client=client,
        ordinal=ordinal,
        significant_changes_only=significant_changes_only,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    id: str,
    *,
    client: Client,
    ordinal: Union[Unset, None, int] = 1,
    significant_changes_only: Union[Unset, None, bool] = False,
) -> Optional[List[ChangeSummary]]:
    """List PayRun Changes for PayRunEntry

     Returns a list of AuditEntry reflecting changes made to a PayRunEntry and related employee record
    for a given PayRun
    This endpoint is currently being beta tested and subject to un-announced breaking changes.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        id (str):
        ordinal (Union[Unset, None, int]):  Default: 1.
        significant_changes_only (Union[Unset, None, bool]):

    Returns:
        Response[List[ChangeSummary]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            tax_year=tax_year,
            pay_period=pay_period,
            period_number=period_number,
            id=id,
            client=client,
            ordinal=ordinal,
            significant_changes_only=significant_changes_only,
        )
    ).parsed
