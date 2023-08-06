from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.external_data_provider_id import ExternalDataProviderId
from ...models.pay_periods import PayPeriods
from ...models.pay_run_journal import PayRunJournal
from ...models.tax_year import TaxYear
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    id: ExternalDataProviderId,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    force: Union[Unset, None, bool] = UNSET,
    ordinal: Union[Unset, None, int] = 1,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/external-data/{id}/{taxYear}/{payPeriod}/{periodNumber}/journal".format(
        client.base_url,
        employerId=employer_id,
        id=id,
        taxYear=tax_year,
        payPeriod=pay_period,
        periodNumber=period_number,
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["force"] = force

    params["ordinal"] = ordinal

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[PayRunJournal]:
    if response.status_code == 200:
        response_200 = PayRunJournal.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[PayRunJournal]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    id: ExternalDataProviderId,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    force: Union[Unset, None, bool] = UNSET,
    ordinal: Union[Unset, None, int] = 1,
) -> Response[PayRunJournal]:
    """Post Journal

     Post a Journal for a payrun to the ExternalDataProvider
    A 200 response does not mean the journal was necessarily successfully posted.
    The PayRunJournal is returned (without the Lines) so that you can inspect the status to determine
    success

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        force (Union[Unset, None, bool]):
        ordinal (Union[Unset, None, int]):  Default: 1.

    Returns:
        Response[PayRunJournal]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        client=client,
        force=force,
        ordinal=ordinal,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    employer_id: str,
    id: ExternalDataProviderId,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    force: Union[Unset, None, bool] = UNSET,
    ordinal: Union[Unset, None, int] = 1,
) -> Optional[PayRunJournal]:
    """Post Journal

     Post a Journal for a payrun to the ExternalDataProvider
    A 200 response does not mean the journal was necessarily successfully posted.
    The PayRunJournal is returned (without the Lines) so that you can inspect the status to determine
    success

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        force (Union[Unset, None, bool]):
        ordinal (Union[Unset, None, int]):  Default: 1.

    Returns:
        Response[PayRunJournal]
    """

    return sync_detailed(
        employer_id=employer_id,
        id=id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        client=client,
        force=force,
        ordinal=ordinal,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    id: ExternalDataProviderId,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    force: Union[Unset, None, bool] = UNSET,
    ordinal: Union[Unset, None, int] = 1,
) -> Response[PayRunJournal]:
    """Post Journal

     Post a Journal for a payrun to the ExternalDataProvider
    A 200 response does not mean the journal was necessarily successfully posted.
    The PayRunJournal is returned (without the Lines) so that you can inspect the status to determine
    success

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        force (Union[Unset, None, bool]):
        ordinal (Union[Unset, None, int]):  Default: 1.

    Returns:
        Response[PayRunJournal]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        client=client,
        force=force,
        ordinal=ordinal,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    id: ExternalDataProviderId,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    force: Union[Unset, None, bool] = UNSET,
    ordinal: Union[Unset, None, int] = 1,
) -> Optional[PayRunJournal]:
    """Post Journal

     Post a Journal for a payrun to the ExternalDataProvider
    A 200 response does not mean the journal was necessarily successfully posted.
    The PayRunJournal is returned (without the Lines) so that you can inspect the status to determine
    success

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        force (Union[Unset, None, bool]):
        ordinal (Union[Unset, None, int]):  Default: 1.

    Returns:
        Response[PayRunJournal]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            id=id,
            tax_year=tax_year,
            pay_period=pay_period,
            period_number=period_number,
            client=client,
            force=force,
            ordinal=ordinal,
        )
    ).parsed
