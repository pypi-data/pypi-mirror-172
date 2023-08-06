from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.pay_periods import PayPeriods
from ...models.processing_note import ProcessingNote
from ...models.tax_year import TaxYear
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    json_body: ProcessingNote,
    ordinal: Union[Unset, None, int] = 1,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/payrun/{taxYear}/{payPeriod}/{periodNumber}/processingnotes".format(
        client.base_url,
        employerId=employer_id,
        taxYear=tax_year,
        payPeriod=pay_period,
        periodNumber=period_number,
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["ordinal"] = ordinal

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[Any, ProcessingNote]]:
    if response.status_code == 201:
        response_201 = ProcessingNote.from_dict(response.json())

        return response_201
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[Any, ProcessingNote]]:
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
    *,
    client: Client,
    json_body: ProcessingNote,
    ordinal: Union[Unset, None, int] = 1,
) -> Response[Union[Any, ProcessingNote]]:
    """Create ProcessingNote

     Creates a Processing Note for the PayRun.
    You must have Bureau Features enabled and the payrun must be editable.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):  Default: 1.
        json_body (ProcessingNote):

    Returns:
        Response[Union[Any, ProcessingNote]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        client=client,
        json_body=json_body,
        ordinal=ordinal,
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
    *,
    client: Client,
    json_body: ProcessingNote,
    ordinal: Union[Unset, None, int] = 1,
) -> Optional[Union[Any, ProcessingNote]]:
    """Create ProcessingNote

     Creates a Processing Note for the PayRun.
    You must have Bureau Features enabled and the payrun must be editable.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):  Default: 1.
        json_body (ProcessingNote):

    Returns:
        Response[Union[Any, ProcessingNote]]
    """

    return sync_detailed(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        client=client,
        json_body=json_body,
        ordinal=ordinal,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    json_body: ProcessingNote,
    ordinal: Union[Unset, None, int] = 1,
) -> Response[Union[Any, ProcessingNote]]:
    """Create ProcessingNote

     Creates a Processing Note for the PayRun.
    You must have Bureau Features enabled and the payrun must be editable.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):  Default: 1.
        json_body (ProcessingNote):

    Returns:
        Response[Union[Any, ProcessingNote]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        client=client,
        json_body=json_body,
        ordinal=ordinal,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    json_body: ProcessingNote,
    ordinal: Union[Unset, None, int] = 1,
) -> Optional[Union[Any, ProcessingNote]]:
    """Create ProcessingNote

     Creates a Processing Note for the PayRun.
    You must have Bureau Features enabled and the payrun must be editable.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):  Default: 1.
        json_body (ProcessingNote):

    Returns:
        Response[Union[Any, ProcessingNote]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            tax_year=tax_year,
            pay_period=pay_period,
            period_number=period_number,
            client=client,
            json_body=json_body,
            ordinal=ordinal,
        )
    ).parsed
