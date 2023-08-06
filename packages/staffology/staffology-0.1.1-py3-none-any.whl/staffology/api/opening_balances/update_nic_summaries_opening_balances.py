from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import Client
from ...models.nic_summary import NicSummary
from ...models.tax_year import TaxYear
from ...types import Response


def _get_kwargs(
    employer_id: str,
    employee_id: str,
    tax_year: TaxYear,
    *,
    client: Client,
    json_body: List[NicSummary],
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/employees/{employeeId}/openingBalances/nic/{taxYear}".format(
        client.base_url,
        employerId=employer_id,
        employeeId=employee_id,
        taxYear=tax_year,
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = []
    for json_body_item_data in json_body:
        json_body_item = json_body_item_data.to_dict()

        json_json_body.append(json_body_item)

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
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
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
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
    json_body: List[NicSummary],
) -> Response[Union[Any, List[NicSummary]]]:
    """Update NicSummaries

     Updates the NicSummaries for an Employee for a given TaxYear.
    If the TaxYear is the same as on their OpeningBalances then the NicSummaries there will also be
    updated.

    Args:
        employer_id (str):
        employee_id (str):
        tax_year (TaxYear):
        json_body (List[NicSummary]):

    Returns:
        Response[Union[Any, List[NicSummary]]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        tax_year=tax_year,
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
    employee_id: str,
    tax_year: TaxYear,
    *,
    client: Client,
    json_body: List[NicSummary],
) -> Optional[Union[Any, List[NicSummary]]]:
    """Update NicSummaries

     Updates the NicSummaries for an Employee for a given TaxYear.
    If the TaxYear is the same as on their OpeningBalances then the NicSummaries there will also be
    updated.

    Args:
        employer_id (str):
        employee_id (str):
        tax_year (TaxYear):
        json_body (List[NicSummary]):

    Returns:
        Response[Union[Any, List[NicSummary]]]
    """

    return sync_detailed(
        employer_id=employer_id,
        employee_id=employee_id,
        tax_year=tax_year,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    employee_id: str,
    tax_year: TaxYear,
    *,
    client: Client,
    json_body: List[NicSummary],
) -> Response[Union[Any, List[NicSummary]]]:
    """Update NicSummaries

     Updates the NicSummaries for an Employee for a given TaxYear.
    If the TaxYear is the same as on their OpeningBalances then the NicSummaries there will also be
    updated.

    Args:
        employer_id (str):
        employee_id (str):
        tax_year (TaxYear):
        json_body (List[NicSummary]):

    Returns:
        Response[Union[Any, List[NicSummary]]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        tax_year=tax_year,
        client=client,
        json_body=json_body,
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
    json_body: List[NicSummary],
) -> Optional[Union[Any, List[NicSummary]]]:
    """Update NicSummaries

     Updates the NicSummaries for an Employee for a given TaxYear.
    If the TaxYear is the same as on their OpeningBalances then the NicSummaries there will also be
    updated.

    Args:
        employer_id (str):
        employee_id (str):
        tax_year (TaxYear):
        json_body (List[NicSummary]):

    Returns:
        Response[Union[Any, List[NicSummary]]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            employee_id=employee_id,
            tax_year=tax_year,
            client=client,
            json_body=json_body,
        )
    ).parsed
