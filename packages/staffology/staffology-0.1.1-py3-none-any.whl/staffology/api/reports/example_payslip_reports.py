from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.payslip_customisation import PayslipCustomisation
from ...models.report_response import ReportResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    json_body: PayslipCustomisation,
    employer_id: Union[Unset, None, str] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/payslip/example/pdf".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(accept, Unset):
        headers["accept"] = accept

    params: Dict[str, Any] = {}
    params["employerId"] = employer_id

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


def _parse_response(*, response: httpx.Response) -> Optional[ReportResponse]:
    if response.status_code == 200:
        response_200 = ReportResponse.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[ReportResponse]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: PayslipCustomisation,
    employer_id: Union[Unset, None, str] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Response[ReportResponse]:
    """Example Payslip

     Use this operation to test your PayslipCustomisation.
    We'll use dummy date and create a Payslip PDF or HTML document based on the customisation that you
    submit

    Args:
        employer_id (Union[Unset, None, str]):
        accept (Union[Unset, str]):
        json_body (PayslipCustomisation): Used to represent any customisations you make to the
            look of Payslip PDFs.
            This is covered in detail in the Guides section.

    Returns:
        Response[ReportResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        employer_id=employer_id,
        accept=accept,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    json_body: PayslipCustomisation,
    employer_id: Union[Unset, None, str] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Optional[ReportResponse]:
    """Example Payslip

     Use this operation to test your PayslipCustomisation.
    We'll use dummy date and create a Payslip PDF or HTML document based on the customisation that you
    submit

    Args:
        employer_id (Union[Unset, None, str]):
        accept (Union[Unset, str]):
        json_body (PayslipCustomisation): Used to represent any customisations you make to the
            look of Payslip PDFs.
            This is covered in detail in the Guides section.

    Returns:
        Response[ReportResponse]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        employer_id=employer_id,
        accept=accept,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: PayslipCustomisation,
    employer_id: Union[Unset, None, str] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Response[ReportResponse]:
    """Example Payslip

     Use this operation to test your PayslipCustomisation.
    We'll use dummy date and create a Payslip PDF or HTML document based on the customisation that you
    submit

    Args:
        employer_id (Union[Unset, None, str]):
        accept (Union[Unset, str]):
        json_body (PayslipCustomisation): Used to represent any customisations you make to the
            look of Payslip PDFs.
            This is covered in detail in the Guides section.

    Returns:
        Response[ReportResponse]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        employer_id=employer_id,
        accept=accept,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    json_body: PayslipCustomisation,
    employer_id: Union[Unset, None, str] = UNSET,
    accept: Union[Unset, str] = UNSET,
) -> Optional[ReportResponse]:
    """Example Payslip

     Use this operation to test your PayslipCustomisation.
    We'll use dummy date and create a Payslip PDF or HTML document based on the customisation that you
    submit

    Args:
        employer_id (Union[Unset, None, str]):
        accept (Union[Unset, str]):
        json_body (PayslipCustomisation): Used to represent any customisations you make to the
            look of Payslip PDFs.
            This is covered in detail in the Guides section.

    Returns:
        Response[ReportResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            employer_id=employer_id,
            accept=accept,
        )
    ).parsed
