from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.recoverable_amounts import RecoverableAmounts
from ...models.tax_year import TaxYear
from ...types import Response


def _get_kwargs(
    employer_id: str,
    tax_year: TaxYear,
    tax_month: int,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/rti/eps/{taxYear}/{taxMonth}/recoverableamounts".format(
        client.base_url, employerId=employer_id, taxYear=tax_year, taxMonth=tax_month
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


def _parse_response(*, response: httpx.Response) -> Optional[RecoverableAmounts]:
    if response.status_code == 200:
        response_200 = RecoverableAmounts.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[RecoverableAmounts]:
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
) -> Response[RecoverableAmounts]:
    """Recoverable Amounts

     Get all recoverable amounts (SMP, etc) for a given tax year, up to the given tax month

    Args:
        employer_id (str):
        tax_year (TaxYear):
        tax_month (int):

    Returns:
        Response[RecoverableAmounts]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        tax_month=tax_month,
        client=client,
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
) -> Optional[RecoverableAmounts]:
    """Recoverable Amounts

     Get all recoverable amounts (SMP, etc) for a given tax year, up to the given tax month

    Args:
        employer_id (str):
        tax_year (TaxYear):
        tax_month (int):

    Returns:
        Response[RecoverableAmounts]
    """

    return sync_detailed(
        employer_id=employer_id,
        tax_year=tax_year,
        tax_month=tax_month,
        client=client,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    tax_year: TaxYear,
    tax_month: int,
    *,
    client: Client,
) -> Response[RecoverableAmounts]:
    """Recoverable Amounts

     Get all recoverable amounts (SMP, etc) for a given tax year, up to the given tax month

    Args:
        employer_id (str):
        tax_year (TaxYear):
        tax_month (int):

    Returns:
        Response[RecoverableAmounts]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        tax_month=tax_month,
        client=client,
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
) -> Optional[RecoverableAmounts]:
    """Recoverable Amounts

     Get all recoverable amounts (SMP, etc) for a given tax year, up to the given tax month

    Args:
        employer_id (str):
        tax_year (TaxYear):
        tax_month (int):

    Returns:
        Response[RecoverableAmounts]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            tax_year=tax_year,
            tax_month=tax_month,
            client=client,
        )
    ).parsed
