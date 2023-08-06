from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...models.tax_year import TaxYear
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    *,
    client: Client,
    tax_year: Union[Unset, None, TaxYear] = UNSET,
    exclude_employees_with_p60_email_sent: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/reports/p60/email".format(
        client.base_url, employerId=employer_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_tax_year: Union[Unset, None, str] = UNSET
    if not isinstance(tax_year, Unset):
        json_tax_year = tax_year.value if tax_year else None

    params["taxYear"] = json_tax_year

    params["excludeEmployeesWithP60EmailSent"] = exclude_employees_with_p60_email_sent

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    employer_id: str,
    *,
    client: Client,
    tax_year: Union[Unset, None, TaxYear] = UNSET,
    exclude_employees_with_p60_email_sent: Union[Unset, None, bool] = False,
) -> Response[Any]:
    """Email P60 to all Employees

     Email P60 to all Employee

    Args:
        employer_id (str):
        tax_year (Union[Unset, None, TaxYear]):
        exclude_employees_with_p60_email_sent (Union[Unset, None, bool]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        tax_year=tax_year,
        exclude_employees_with_p60_email_sent=exclude_employees_with_p60_email_sent,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    employer_id: str,
    *,
    client: Client,
    tax_year: Union[Unset, None, TaxYear] = UNSET,
    exclude_employees_with_p60_email_sent: Union[Unset, None, bool] = False,
) -> Response[Any]:
    """Email P60 to all Employees

     Email P60 to all Employee

    Args:
        employer_id (str):
        tax_year (Union[Unset, None, TaxYear]):
        exclude_employees_with_p60_email_sent (Union[Unset, None, bool]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        tax_year=tax_year,
        exclude_employees_with_p60_email_sent=exclude_employees_with_p60_email_sent,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
