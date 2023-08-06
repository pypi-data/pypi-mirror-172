from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.finalise_pay_run_pay_run_json_body import FinalisePayRunPayRunJsonBody
from ...models.pay_periods import PayPeriods
from ...models.tax_year import TaxYear
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    json_body: FinalisePayRunPayRunJsonBody,
    ordinal: Union[Unset, None, int] = 1,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/payrun/{taxYear}/{payPeriod}/{periodNumber}/finalise".format(
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


def _parse_response(*, response: httpx.Response) -> Optional[bool]:
    if response.status_code == 200:
        response_200 = cast(bool, response.json())
        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[bool]:
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
    json_body: FinalisePayRunPayRunJsonBody,
    ordinal: Union[Unset, None, int] = 1,
) -> Response[bool]:
    """Finalise a PayRun (deprecated)

     This endpoint is now deprecated and will be removed in Jan 2022.
    You should instead use the Update method and set the State to Finalised.

    Returns True if the resulting FPS has been automatically submitted due to the Employers
    RTISubmissionSettings, otherwise returns false.
    You can suppress the emailing of payslips to employees by adding a key named
    dontEmailEmployeePayslips with a value of true to the body. See the related guides for more
    information.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):  Default: 1.
        json_body (FinalisePayRunPayRunJsonBody):

    Returns:
        Response[bool]
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
    json_body: FinalisePayRunPayRunJsonBody,
    ordinal: Union[Unset, None, int] = 1,
) -> Optional[bool]:
    """Finalise a PayRun (deprecated)

     This endpoint is now deprecated and will be removed in Jan 2022.
    You should instead use the Update method and set the State to Finalised.

    Returns True if the resulting FPS has been automatically submitted due to the Employers
    RTISubmissionSettings, otherwise returns false.
    You can suppress the emailing of payslips to employees by adding a key named
    dontEmailEmployeePayslips with a value of true to the body. See the related guides for more
    information.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):  Default: 1.
        json_body (FinalisePayRunPayRunJsonBody):

    Returns:
        Response[bool]
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
    json_body: FinalisePayRunPayRunJsonBody,
    ordinal: Union[Unset, None, int] = 1,
) -> Response[bool]:
    """Finalise a PayRun (deprecated)

     This endpoint is now deprecated and will be removed in Jan 2022.
    You should instead use the Update method and set the State to Finalised.

    Returns True if the resulting FPS has been automatically submitted due to the Employers
    RTISubmissionSettings, otherwise returns false.
    You can suppress the emailing of payslips to employees by adding a key named
    dontEmailEmployeePayslips with a value of true to the body. See the related guides for more
    information.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):  Default: 1.
        json_body (FinalisePayRunPayRunJsonBody):

    Returns:
        Response[bool]
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
    json_body: FinalisePayRunPayRunJsonBody,
    ordinal: Union[Unset, None, int] = 1,
) -> Optional[bool]:
    """Finalise a PayRun (deprecated)

     This endpoint is now deprecated and will be removed in Jan 2022.
    You should instead use the Update method and set the State to Finalised.

    Returns True if the resulting FPS has been automatically submitted due to the Employers
    RTISubmissionSettings, otherwise returns false.
    You can suppress the emailing of payslips to employees by adding a key named
    dontEmailEmployeePayslips with a value of true to the body. See the related guides for more
    information.

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):  Default: 1.
        json_body (FinalisePayRunPayRunJsonBody):

    Returns:
        Response[bool]
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
