import datetime
from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.ni_letter_validation_report_report_response import (
    NiLetterValidationReportReportResponse,
)
from ...models.pay_periods import PayPeriods
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    *,
    client: Client,
    pay_date: Union[Unset, None, datetime.datetime] = UNSET,
    pay_period: Union[Unset, None, PayPeriods] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/reports/NiLetterValidationReport".format(
        client.base_url, employerId=employer_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(accept, Unset):
        headers["accept"] = accept

    params: Dict[str, Any] = {}
    json_pay_date: Union[Unset, None, str] = UNSET
    if not isinstance(pay_date, Unset):
        json_pay_date = pay_date.isoformat() if pay_date else None

    params["payDate"] = json_pay_date

    json_pay_period: Union[Unset, None, str] = UNSET
    if not isinstance(pay_period, Unset):
        json_pay_period = pay_period.value if pay_period else None

    params["payPeriod"] = json_pay_period

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[NiLetterValidationReportReportResponse]:
    if response.status_code == 200:
        response_200 = NiLetterValidationReportReportResponse.from_dict(response.json())

        return response_200
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[NiLetterValidationReportReportResponse]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    *,
    client: Client,
    pay_date: Union[Unset, None, datetime.datetime] = UNSET,
    pay_period: Union[Unset, None, PayPeriods] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Response[NiLetterValidationReportReportResponse]:
    """NI Letter Validation (Employees)

     Checks the NI Letters allocated to your employees. If no pay date is provided, the checks are based
    on todays date.

    Args:
        employer_id (str):
        pay_date (Union[Unset, None, datetime.datetime]):
        pay_period (Union[Unset, None, PayPeriods]):
        accept (Union[Unset, str]):

    Returns:
        Response[NiLetterValidationReportReportResponse]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        pay_date=pay_date,
        pay_period=pay_period,
        accept=accept,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    employer_id: str,
    *,
    client: Client,
    pay_date: Union[Unset, None, datetime.datetime] = UNSET,
    pay_period: Union[Unset, None, PayPeriods] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Optional[NiLetterValidationReportReportResponse]:
    """NI Letter Validation (Employees)

     Checks the NI Letters allocated to your employees. If no pay date is provided, the checks are based
    on todays date.

    Args:
        employer_id (str):
        pay_date (Union[Unset, None, datetime.datetime]):
        pay_period (Union[Unset, None, PayPeriods]):
        accept (Union[Unset, str]):

    Returns:
        Response[NiLetterValidationReportReportResponse]
    """

    return sync_detailed(
        employer_id=employer_id,
        client=client,
        pay_date=pay_date,
        pay_period=pay_period,
        accept=accept,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    *,
    client: Client,
    pay_date: Union[Unset, None, datetime.datetime] = UNSET,
    pay_period: Union[Unset, None, PayPeriods] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Response[NiLetterValidationReportReportResponse]:
    """NI Letter Validation (Employees)

     Checks the NI Letters allocated to your employees. If no pay date is provided, the checks are based
    on todays date.

    Args:
        employer_id (str):
        pay_date (Union[Unset, None, datetime.datetime]):
        pay_period (Union[Unset, None, PayPeriods]):
        accept (Union[Unset, str]):

    Returns:
        Response[NiLetterValidationReportReportResponse]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        pay_date=pay_date,
        pay_period=pay_period,
        accept=accept,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    *,
    client: Client,
    pay_date: Union[Unset, None, datetime.datetime] = UNSET,
    pay_period: Union[Unset, None, PayPeriods] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Optional[NiLetterValidationReportReportResponse]:
    """NI Letter Validation (Employees)

     Checks the NI Letters allocated to your employees. If no pay date is provided, the checks are based
    on todays date.

    Args:
        employer_id (str):
        pay_date (Union[Unset, None, datetime.datetime]):
        pay_period (Union[Unset, None, PayPeriods]):
        accept (Union[Unset, str]):

    Returns:
        Response[NiLetterValidationReportReportResponse]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            client=client,
            pay_date=pay_date,
            pay_period=pay_period,
            accept=accept,
        )
    ).parsed
