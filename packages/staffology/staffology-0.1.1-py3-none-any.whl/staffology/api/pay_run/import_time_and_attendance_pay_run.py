from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.external_data_provider_id import ExternalDataProviderId
from ...models.pay_options_import import PayOptionsImport
from ...models.pay_periods import PayPeriods
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    pay_period: PayPeriods,
    *,
    client: Client,
    provider_id: Union[Unset, None, ExternalDataProviderId] = UNSET,
    ordinal: Union[Unset, None, int] = 1,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/payrun/{payPeriod}/importtimeandattendance".format(
        client.base_url, employerId=employer_id, payPeriod=pay_period
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_provider_id: Union[Unset, None, str] = UNSET
    if not isinstance(provider_id, Unset):
        json_provider_id = provider_id.value if provider_id else None

    params["providerId"] = json_provider_id

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


def _parse_response(*, response: httpx.Response) -> Optional[List[PayOptionsImport]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = PayOptionsImport.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[List[PayOptionsImport]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    pay_period: PayPeriods,
    *,
    client: Client,
    provider_id: Union[Unset, None, ExternalDataProviderId] = UNSET,
    ordinal: Union[Unset, None, int] = 1,
) -> Response[List[PayOptionsImport]]:
    """Import Time And Attendance

     If the employer is connected to an ExternalDataProvider that provides Time and Attendance data then
    this API
    call will update the currently open payrun for the PayPeriod specified with data from the specified
    provider.
    Returns a list of PayOptionsImport to show what's been imported.

    Args:
        employer_id (str):
        pay_period (PayPeriods):
        provider_id (Union[Unset, None, ExternalDataProviderId]):
        ordinal (Union[Unset, None, int]):  Default: 1.

    Returns:
        Response[List[PayOptionsImport]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        pay_period=pay_period,
        client=client,
        provider_id=provider_id,
        ordinal=ordinal,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    employer_id: str,
    pay_period: PayPeriods,
    *,
    client: Client,
    provider_id: Union[Unset, None, ExternalDataProviderId] = UNSET,
    ordinal: Union[Unset, None, int] = 1,
) -> Optional[List[PayOptionsImport]]:
    """Import Time And Attendance

     If the employer is connected to an ExternalDataProvider that provides Time and Attendance data then
    this API
    call will update the currently open payrun for the PayPeriod specified with data from the specified
    provider.
    Returns a list of PayOptionsImport to show what's been imported.

    Args:
        employer_id (str):
        pay_period (PayPeriods):
        provider_id (Union[Unset, None, ExternalDataProviderId]):
        ordinal (Union[Unset, None, int]):  Default: 1.

    Returns:
        Response[List[PayOptionsImport]]
    """

    return sync_detailed(
        employer_id=employer_id,
        pay_period=pay_period,
        client=client,
        provider_id=provider_id,
        ordinal=ordinal,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    pay_period: PayPeriods,
    *,
    client: Client,
    provider_id: Union[Unset, None, ExternalDataProviderId] = UNSET,
    ordinal: Union[Unset, None, int] = 1,
) -> Response[List[PayOptionsImport]]:
    """Import Time And Attendance

     If the employer is connected to an ExternalDataProvider that provides Time and Attendance data then
    this API
    call will update the currently open payrun for the PayPeriod specified with data from the specified
    provider.
    Returns a list of PayOptionsImport to show what's been imported.

    Args:
        employer_id (str):
        pay_period (PayPeriods):
        provider_id (Union[Unset, None, ExternalDataProviderId]):
        ordinal (Union[Unset, None, int]):  Default: 1.

    Returns:
        Response[List[PayOptionsImport]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        pay_period=pay_period,
        client=client,
        provider_id=provider_id,
        ordinal=ordinal,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    pay_period: PayPeriods,
    *,
    client: Client,
    provider_id: Union[Unset, None, ExternalDataProviderId] = UNSET,
    ordinal: Union[Unset, None, int] = 1,
) -> Optional[List[PayOptionsImport]]:
    """Import Time And Attendance

     If the employer is connected to an ExternalDataProvider that provides Time and Attendance data then
    this API
    call will update the currently open payrun for the PayPeriod specified with data from the specified
    provider.
    Returns a list of PayOptionsImport to show what's been imported.

    Args:
        employer_id (str):
        pay_period (PayPeriods):
        provider_id (Union[Unset, None, ExternalDataProviderId]):
        ordinal (Union[Unset, None, int]):  Default: 1.

    Returns:
        Response[List[PayOptionsImport]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            pay_period=pay_period,
            client=client,
            provider_id=provider_id,
            ordinal=ordinal,
        )
    ).parsed
