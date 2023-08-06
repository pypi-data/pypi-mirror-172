from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.employee_ytd_values import EmployeeYtdValues
from ...models.pay_periods import PayPeriods
from ...models.tax_year import TaxYear
from ...models.ytd_pay_run_multipart_data import YtdPayRunMultipartData
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    multipart_data: YtdPayRunMultipartData,
    ordinal: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/payrun/{taxYear}/{payPeriod}/{periodNumber}/ytd".format(
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

    multipart_multipart_data = multipart_data.to_multipart()

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "files": multipart_multipart_data,
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[List[EmployeeYtdValues]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = EmployeeYtdValues.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[List[EmployeeYtdValues]]:
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
    multipart_data: YtdPayRunMultipartData,
    ordinal: Union[Unset, None, int] = UNSET,
) -> Response[List[EmployeeYtdValues]]:
    """Update YTD

     Upload a CSV to override the YTD values on a Payrun.
    The CSV should have the same headings as the YTD report

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):
        multipart_data (YtdPayRunMultipartData):

    Returns:
        Response[List[EmployeeYtdValues]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        client=client,
        multipart_data=multipart_data,
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
    multipart_data: YtdPayRunMultipartData,
    ordinal: Union[Unset, None, int] = UNSET,
) -> Optional[List[EmployeeYtdValues]]:
    """Update YTD

     Upload a CSV to override the YTD values on a Payrun.
    The CSV should have the same headings as the YTD report

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):
        multipart_data (YtdPayRunMultipartData):

    Returns:
        Response[List[EmployeeYtdValues]]
    """

    return sync_detailed(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        client=client,
        multipart_data=multipart_data,
        ordinal=ordinal,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    tax_year: TaxYear,
    pay_period: PayPeriods,
    period_number: int,
    *,
    client: Client,
    multipart_data: YtdPayRunMultipartData,
    ordinal: Union[Unset, None, int] = UNSET,
) -> Response[List[EmployeeYtdValues]]:
    """Update YTD

     Upload a CSV to override the YTD values on a Payrun.
    The CSV should have the same headings as the YTD report

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):
        multipart_data (YtdPayRunMultipartData):

    Returns:
        Response[List[EmployeeYtdValues]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        tax_year=tax_year,
        pay_period=pay_period,
        period_number=period_number,
        client=client,
        multipart_data=multipart_data,
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
    multipart_data: YtdPayRunMultipartData,
    ordinal: Union[Unset, None, int] = UNSET,
) -> Optional[List[EmployeeYtdValues]]:
    """Update YTD

     Upload a CSV to override the YTD values on a Payrun.
    The CSV should have the same headings as the YTD report

    Args:
        employer_id (str):
        tax_year (TaxYear):
        pay_period (PayPeriods):
        period_number (int):
        ordinal (Union[Unset, None, int]):
        multipart_data (YtdPayRunMultipartData):

    Returns:
        Response[List[EmployeeYtdValues]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            tax_year=tax_year,
            pay_period=pay_period,
            period_number=period_number,
            client=client,
            multipart_data=multipart_data,
            ordinal=ordinal,
        )
    ).parsed
