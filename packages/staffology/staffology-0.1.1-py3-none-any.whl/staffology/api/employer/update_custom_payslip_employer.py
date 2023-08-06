from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.payslip_customisation import PayslipCustomisation
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    client: Client,
    json_body: PayslipCustomisation,
) -> Dict[str, Any]:
    url = "{}/employers/{id}/custompayslip".format(client.base_url, id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[PayslipCustomisation]:
    if response.status_code == 200:
        response_200 = PayslipCustomisation.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[PayslipCustomisation]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    id: str,
    *,
    client: Client,
    json_body: PayslipCustomisation,
) -> Response[PayslipCustomisation]:
    """Update Payslip Customisations

     Set the settings used to customise PaySlips for this Employer

    Args:
        id (str):
        json_body (PayslipCustomisation): Used to represent any customisations you make to the
            look of Payslip PDFs.
            This is covered in detail in the Guides section.

    Returns:
        Response[PayslipCustomisation]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    id: str,
    *,
    client: Client,
    json_body: PayslipCustomisation,
) -> Optional[PayslipCustomisation]:
    """Update Payslip Customisations

     Set the settings used to customise PaySlips for this Employer

    Args:
        id (str):
        json_body (PayslipCustomisation): Used to represent any customisations you make to the
            look of Payslip PDFs.
            This is covered in detail in the Guides section.

    Returns:
        Response[PayslipCustomisation]
    """

    return sync_detailed(
        id=id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Client,
    json_body: PayslipCustomisation,
) -> Response[PayslipCustomisation]:
    """Update Payslip Customisations

     Set the settings used to customise PaySlips for this Employer

    Args:
        id (str):
        json_body (PayslipCustomisation): Used to represent any customisations you make to the
            look of Payslip PDFs.
            This is covered in detail in the Guides section.

    Returns:
        Response[PayslipCustomisation]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    id: str,
    *,
    client: Client,
    json_body: PayslipCustomisation,
) -> Optional[PayslipCustomisation]:
    """Update Payslip Customisations

     Set the settings used to customise PaySlips for this Employer

    Args:
        id (str):
        json_body (PayslipCustomisation): Used to represent any customisations you make to the
            look of Payslip PDFs.
            This is covered in detail in the Guides section.

    Returns:
        Response[PayslipCustomisation]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            json_body=json_body,
        )
    ).parsed
