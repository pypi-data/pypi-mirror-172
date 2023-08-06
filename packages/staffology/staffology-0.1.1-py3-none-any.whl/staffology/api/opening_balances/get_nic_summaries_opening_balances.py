from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import Client
from ...models.nic_summary import NicSummary
from ...models.tax_year import TaxYear
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    employee_id: str,
    tax_year: TaxYear,
    *,
    client: Client,
    opening_balances_only: Union[Unset, None, bool] = True,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/employees/{employeeId}/openingBalances/nic/{taxYear}".format(
        client.base_url,
        employerId=employer_id,
        employeeId=employee_id,
        taxYear=tax_year,
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["openingBalancesOnly"] = opening_balances_only

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
) -> Optional[Union[Any, List[NicSummary]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = NicSummary.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[Any, List[NicSummary]]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    employee_id: str,
    tax_year: TaxYear,
    *,
    client: Client,
    opening_balances_only: Union[Unset, None, bool] = True,
) -> Response[Union[Any, List[NicSummary]]]:
    """Get NicSummaries

     Returns the NicSummaries for an Employee for a given TaxYear.
    If the TaxYear is the same as on their OpeningBalances then the NicSummaries will be the same as
    shown there.

    Args:
        employer_id (str):
        employee_id (str):
        tax_year (TaxYear):
        opening_balances_only (Union[Unset, None, bool]):  Default: True.

    Returns:
        Response[Union[Any, List[NicSummary]]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        tax_year=tax_year,
        client=client,
        opening_balances_only=opening_balances_only,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    employer_id: str,
    employee_id: str,
    tax_year: TaxYear,
    *,
    client: Client,
    opening_balances_only: Union[Unset, None, bool] = True,
) -> Optional[Union[Any, List[NicSummary]]]:
    """Get NicSummaries

     Returns the NicSummaries for an Employee for a given TaxYear.
    If the TaxYear is the same as on their OpeningBalances then the NicSummaries will be the same as
    shown there.

    Args:
        employer_id (str):
        employee_id (str):
        tax_year (TaxYear):
        opening_balances_only (Union[Unset, None, bool]):  Default: True.

    Returns:
        Response[Union[Any, List[NicSummary]]]
    """

    return sync_detailed(
        employer_id=employer_id,
        employee_id=employee_id,
        tax_year=tax_year,
        client=client,
        opening_balances_only=opening_balances_only,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    employee_id: str,
    tax_year: TaxYear,
    *,
    client: Client,
    opening_balances_only: Union[Unset, None, bool] = True,
) -> Response[Union[Any, List[NicSummary]]]:
    """Get NicSummaries

     Returns the NicSummaries for an Employee for a given TaxYear.
    If the TaxYear is the same as on their OpeningBalances then the NicSummaries will be the same as
    shown there.

    Args:
        employer_id (str):
        employee_id (str):
        tax_year (TaxYear):
        opening_balances_only (Union[Unset, None, bool]):  Default: True.

    Returns:
        Response[Union[Any, List[NicSummary]]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        tax_year=tax_year,
        client=client,
        opening_balances_only=opening_balances_only,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    employee_id: str,
    tax_year: TaxYear,
    *,
    client: Client,
    opening_balances_only: Union[Unset, None, bool] = True,
) -> Optional[Union[Any, List[NicSummary]]]:
    """Get NicSummaries

     Returns the NicSummaries for an Employee for a given TaxYear.
    If the TaxYear is the same as on their OpeningBalances then the NicSummaries will be the same as
    shown there.

    Args:
        employer_id (str):
        employee_id (str):
        tax_year (TaxYear):
        opening_balances_only (Union[Unset, None, bool]):  Default: True.

    Returns:
        Response[Union[Any, List[NicSummary]]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            employee_id=employee_id,
            tax_year=tax_year,
            client=client,
            opening_balances_only=opening_balances_only,
        )
    ).parsed
