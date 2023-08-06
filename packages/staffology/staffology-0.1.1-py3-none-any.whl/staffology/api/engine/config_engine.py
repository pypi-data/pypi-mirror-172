from typing import Any, Dict, Union

import httpx

from ...client import Client
from ...models.tax_year import TaxYear
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    tax_year: Union[Unset, None, TaxYear] = UNSET,
) -> Dict[str, Any]:
    url = "{}/engine/config".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_tax_year: Union[Unset, None, str] = UNSET
    if not isinstance(tax_year, Unset):
        json_tax_year = tax_year.value if tax_year else None

    params["taxYear"] = json_tax_year

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    *,
    client: Client,
    tax_year: Union[Unset, None, TaxYear] = UNSET,
) -> Response[Any]:
    """Get Configuration

     Returns the raw configuration data that is used as the basis for any calculations for the given tax
    year.
    You would never need to use this configuration values yourself in any API calls. It is provided just
    for information purposes

    Args:
        tax_year (Union[Unset, None, TaxYear]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        tax_year=tax_year,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    *,
    client: Client,
    tax_year: Union[Unset, None, TaxYear] = UNSET,
) -> Response[Any]:
    """Get Configuration

     Returns the raw configuration data that is used as the basis for any calculations for the given tax
    year.
    You would never need to use this configuration values yourself in any API calls. It is provided just
    for information purposes

    Args:
        tax_year (Union[Unset, None, TaxYear]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        client=client,
        tax_year=tax_year,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
