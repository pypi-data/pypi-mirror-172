from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.pay_periods import PayPeriods
from ...models.pay_run import PayRun
from ...models.pay_run_state_change import PayRunStateChange
from ...models.tax_year import TaxYear
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    json_body: PayRunStateChange,
    ordinal: Union[Unset, None, int] = 1,
    send_payslip_emails: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = (
        "{}/employers/{employerId}/payrun/{taxYear}/{payPeriod}/{periodNumber}".format(
            client.base_url,
            employerId=employer_id,
            taxYear=tax_year,
            payPeriod=pay_period,
            periodNumber=period_number,
        )
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["ordinal"] = ordinal

    params["sendPayslipEmails"] = send_payslip_emails

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, PayRun]]:
    if response.status_code == 200:
        response_200 = PayRun.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, PayRun]]:
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
    json_body: PayRunStateChange,
    ordinal: Union[Unset, None, int] = 1,
    send_payslip_emails: Union[Unset, None, bool] = False,
) -> Response[Union[Any, PayRun]]:
    """Update PayRun

     Updates a PayRun to the state provided along with the reason (optional) for the change.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):  Default: 1.
        send_payslip_emails (Union[Unset, None, bool]):
        json_body (PayRunStateChange):

    Returns:
        Response[Union[Any, PayRun]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        client=client,
        json_body=json_body,
        ordinal=ordinal,
        send_payslip_emails=send_payslip_emails,
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
    json_body: PayRunStateChange,
    ordinal: Union[Unset, None, int] = 1,
    send_payslip_emails: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, PayRun]]:
    """Update PayRun

     Updates a PayRun to the state provided along with the reason (optional) for the change.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):  Default: 1.
        send_payslip_emails (Union[Unset, None, bool]):
        json_body (PayRunStateChange):

    Returns:
        Response[Union[Any, PayRun]]
    """

    return sync_detailed(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        client=client,
        json_body=json_body,
        ordinal=ordinal,
        send_payslip_emails=send_payslip_emails,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    json_body: PayRunStateChange,
    ordinal: Union[Unset, None, int] = 1,
    send_payslip_emails: Union[Unset, None, bool] = False,
) -> Response[Union[Any, PayRun]]:
    """Update PayRun

     Updates a PayRun to the state provided along with the reason (optional) for the change.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):  Default: 1.
        send_payslip_emails (Union[Unset, None, bool]):
        json_body (PayRunStateChange):

    Returns:
        Response[Union[Any, PayRun]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        client=client,
        json_body=json_body,
        ordinal=ordinal,
        send_payslip_emails=send_payslip_emails,
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
    json_body: PayRunStateChange,
    ordinal: Union[Unset, None, int] = 1,
    send_payslip_emails: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, PayRun]]:
    """Update PayRun

     Updates a PayRun to the state provided along with the reason (optional) for the change.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):  Default: 1.
        send_payslip_emails (Union[Unset, None, bool]):
        json_body (PayRunStateChange):

    Returns:
        Response[Union[Any, PayRun]]
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
            send_payslip_emails=send_payslip_emails,
        )
    ).parsed
