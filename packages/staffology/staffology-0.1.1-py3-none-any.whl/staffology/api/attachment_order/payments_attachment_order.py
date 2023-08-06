from typing import Any, Dict, List, Optional

import httpx

from ...client import Client
from ...models.attachment_order_payment import AttachmentOrderPayment
from ...models.tax_year import TaxYear
from ...types import Response


def _get_kwargs(
    employer_id: str,
    employee_id: str,
    tax_year: TaxYear,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/employees/{employeeId}/attachmentorders/payments/{taxYear}".format(
        client.base_url,
        employerId=employer_id,
        employeeId=employee_id,
        taxYear=tax_year,
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[List[AttachmentOrderPayment]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = AttachmentOrderPayment.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[List[AttachmentOrderPayment]]:
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
) -> Response[List[AttachmentOrderPayment]]:
    """Get Payments

     Lists all Payments made to AttachmentOrders for the Employee in the given TaxYear

    Args:
        employer_id (str):
        employee_id (str):
        tax_year (TaxYear):

    Returns:
        Response[List[AttachmentOrderPayment]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        tax_year=tax_year,
        client=client,
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
) -> Optional[List[AttachmentOrderPayment]]:
    """Get Payments

     Lists all Payments made to AttachmentOrders for the Employee in the given TaxYear

    Args:
        employer_id (str):
        employee_id (str):
        tax_year (TaxYear):

    Returns:
        Response[List[AttachmentOrderPayment]]
    """

    return sync_detailed(
        employer_id=employer_id,
        employee_id=employee_id,
        tax_year=tax_year,
        client=client,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    employee_id: str,
    tax_year: TaxYear,
    *,
    client: Client,
) -> Response[List[AttachmentOrderPayment]]:
    """Get Payments

     Lists all Payments made to AttachmentOrders for the Employee in the given TaxYear

    Args:
        employer_id (str):
        employee_id (str):
        tax_year (TaxYear):

    Returns:
        Response[List[AttachmentOrderPayment]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        tax_year=tax_year,
        client=client,
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
) -> Optional[List[AttachmentOrderPayment]]:
    """Get Payments

     Lists all Payments made to AttachmentOrders for the Employee in the given TaxYear

    Args:
        employer_id (str):
        employee_id (str):
        tax_year (TaxYear):

    Returns:
        Response[List[AttachmentOrderPayment]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            employee_id=employee_id,
            tax_year=tax_year,
            client=client,
        )
    ).parsed
