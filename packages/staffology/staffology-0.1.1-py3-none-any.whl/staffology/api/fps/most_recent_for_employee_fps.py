from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.item import Item
from ...models.tax_year import TaxYear
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    tax_year: TaxYear,
    employee_id: str,
    *,
    client: Client,
    correction: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/rti/fps/{taxYear}/mostrecentforemployee/{employeeId}".format(
        client.base_url,
        employerId=employer_id,
        taxYear=tax_year,
        employeeId=employee_id,
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["correction"] = correction

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, Item]]:
    if response.status_code == 200:
        response_200 = Item.from_dict(response.json())

        return response_200
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, Item]]:
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
    correction: Union[Unset, None, bool] = False,
) -> Response[Union[Any, Item]]:
    """Get most recent FPS for Employee

     Returns the most recent Full Payment Submission that includes the specified employee

    Args:
        employer_id (str):
        tax_year (TaxYear):
        employee_id (str):
        correction (Union[Unset, None, bool]):

    Returns:
        Response[Union[Any, Item]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        employee_id=employee_id,
        client=client,
        correction=correction,
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
    correction: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, Item]]:
    """Get most recent FPS for Employee

     Returns the most recent Full Payment Submission that includes the specified employee

    Args:
        employer_id (str):
        tax_year (TaxYear):
        employee_id (str):
        correction (Union[Unset, None, bool]):

    Returns:
        Response[Union[Any, Item]]
    """

    return sync_detailed(
        employer_id=employer_id,
        tax_year=tax_year,
        employee_id=employee_id,
        client=client,
        correction=correction,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    tax_year: TaxYear,
    employee_id: str,
    *,
    client: Client,
    correction: Union[Unset, None, bool] = False,
) -> Response[Union[Any, Item]]:
    """Get most recent FPS for Employee

     Returns the most recent Full Payment Submission that includes the specified employee

    Args:
        employer_id (str):
        tax_year (TaxYear):
        employee_id (str):
        correction (Union[Unset, None, bool]):

    Returns:
        Response[Union[Any, Item]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        employee_id=employee_id,
        client=client,
        correction=correction,
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
    correction: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, Item]]:
    """Get most recent FPS for Employee

     Returns the most recent Full Payment Submission that includes the specified employee

    Args:
        employer_id (str):
        tax_year (TaxYear):
        employee_id (str):
        correction (Union[Unset, None, bool]):

    Returns:
        Response[Union[Any, Item]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            tax_year=tax_year,
            employee_id=employee_id,
            client=client,
            correction=correction,
        )
    ).parsed
