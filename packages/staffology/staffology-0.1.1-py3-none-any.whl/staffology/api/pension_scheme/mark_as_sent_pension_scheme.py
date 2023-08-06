from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.external_provider_conversation import ExternalProviderConversation
from ...models.tax_year import TaxYear
from ...types import Response


def _get_kwargs(
    employer_id: str,
    id: str,
    tax_year: TaxYear,
    submission_id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/pensionschemes/{id}/contributions/{taxYear}/{submissionId}/markassent".format(
        client.base_url,
        employerId=employer_id,
        id=id,
        taxYear=tax_year,
        submissionId=submission_id,
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[ExternalProviderConversation]:
    if response.status_code == 200:
        response_200 = ExternalProviderConversation.from_dict(response.json())

        return response_200
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[ExternalProviderConversation]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    id: str,
    tax_year: TaxYear,
    submission_id: str,
    *,
    client: Client,
) -> Response[ExternalProviderConversation]:
    """Mark as Sent

     Marks the Pension Contributions as sent

    Args:
        employer_id (str):
        id (str):
        tax_year (TaxYear):
        submission_id (str):

    Returns:
        Response[ExternalProviderConversation]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        tax_year=tax_year,
        submission_id=submission_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    employer_id: str,
    id: str,
    tax_year: TaxYear,
    submission_id: str,
    *,
    client: Client,
) -> Optional[ExternalProviderConversation]:
    """Mark as Sent

     Marks the Pension Contributions as sent

    Args:
        employer_id (str):
        id (str):
        tax_year (TaxYear):
        submission_id (str):

    Returns:
        Response[ExternalProviderConversation]
    """

    return sync_detailed(
        employer_id=employer_id,
        id=id,
        tax_year=tax_year,
        submission_id=submission_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    id: str,
    tax_year: TaxYear,
    submission_id: str,
    *,
    client: Client,
) -> Response[ExternalProviderConversation]:
    """Mark as Sent

     Marks the Pension Contributions as sent

    Args:
        employer_id (str):
        id (str):
        tax_year (TaxYear):
        submission_id (str):

    Returns:
        Response[ExternalProviderConversation]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        tax_year=tax_year,
        submission_id=submission_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    id: str,
    tax_year: TaxYear,
    submission_id: str,
    *,
    client: Client,
) -> Optional[ExternalProviderConversation]:
    """Mark as Sent

     Marks the Pension Contributions as sent

    Args:
        employer_id (str):
        id (str):
        tax_year (TaxYear):
        submission_id (str):

    Returns:
        Response[ExternalProviderConversation]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            id=id,
            tax_year=tax_year,
            submission_id=submission_id,
            client=client,
        )
    ).parsed
