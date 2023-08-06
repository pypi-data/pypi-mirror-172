from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.cis_verification import CisVerification
from ...models.tax_year import TaxYear
from ...types import Response


def _get_kwargs(
    employer_id: str,
    tax_year: TaxYear,
    id: str,
    *,
    client: Client,
    json_body: CisVerification,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/rti/cis-verification/{taxYear}/{id}".format(
        client.base_url, employerId=employer_id, taxYear=tax_year, id=id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[CisVerification]:
    if response.status_code == 200:
        response_200 = CisVerification.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[CisVerification]:
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
    json_body: CisVerification,
) -> Response[CisVerification]:
    """Update CisVerificationRequest

     Updates an existing CIS Verification Request.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        id (str):
        json_body (CisVerification): If an Employee is marked as a CIS Subcontractor then this
            model is included ad a child of CisDetails and is used to represent the Verification
            details of the Subcontractor

    Returns:
        Response[CisVerification]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        id=id,
        client=client,
        json_body=json_body,
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
    json_body: CisVerification,
) -> Optional[CisVerification]:
    """Update CisVerificationRequest

     Updates an existing CIS Verification Request.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        id (str):
        json_body (CisVerification): If an Employee is marked as a CIS Subcontractor then this
            model is included ad a child of CisDetails and is used to represent the Verification
            details of the Subcontractor

    Returns:
        Response[CisVerification]
    """

    return sync_detailed(
        employer_id=employer_id,
        tax_year=tax_year,
        id=id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    tax_year: TaxYear,
    id: str,
    *,
    client: Client,
    json_body: CisVerification,
) -> Response[CisVerification]:
    """Update CisVerificationRequest

     Updates an existing CIS Verification Request.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        id (str):
        json_body (CisVerification): If an Employee is marked as a CIS Subcontractor then this
            model is included ad a child of CisDetails and is used to represent the Verification
            details of the Subcontractor

    Returns:
        Response[CisVerification]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        id=id,
        client=client,
        json_body=json_body,
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
    json_body: CisVerification,
) -> Optional[CisVerification]:
    """Update CisVerificationRequest

     Updates an existing CIS Verification Request.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        id (str):
        json_body (CisVerification): If an Employee is marked as a CIS Subcontractor then this
            model is included ad a child of CisDetails and is used to represent the Verification
            details of the Subcontractor

    Returns:
        Response[CisVerification]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            tax_year=tax_year,
            id=id,
            client=client,
            json_body=json_body,
        )
    ).parsed
