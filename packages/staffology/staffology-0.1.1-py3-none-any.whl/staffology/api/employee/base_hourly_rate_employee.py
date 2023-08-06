from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.pay_basis import PayBasis
from ...models.pay_periods import PayPeriods
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    id: str,
    *,
    client: Client,
    pay_period: Union[Unset, None, PayPeriods] = UNSET,
    pay_basis: Union[Unset, None, PayBasis] = UNSET,
    pay_amount: Union[Unset, None, float] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/employees/{id}/basehourlyrate".format(
        client.base_url, employerId=employer_id, id=id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_pay_period: Union[Unset, None, str] = UNSET
    if not isinstance(pay_period, Unset):
        json_pay_period = pay_period.value if pay_period else None

    params["payPeriod"] = json_pay_period

    json_pay_basis: Union[Unset, None, str] = UNSET
    if not isinstance(pay_basis, Unset):
        json_pay_basis = pay_basis.value if pay_basis else None

    params["payBasis"] = json_pay_basis

    params["payAmount"] = pay_amount

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[float]:
    if response.status_code == 200:
        response_200 = cast(float, response.json())
        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[float]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    id: str,
    *,
    client: Client,
    pay_period: Union[Unset, None, PayPeriods] = UNSET,
    pay_basis: Union[Unset, None, PayBasis] = UNSET,
    pay_amount: Union[Unset, None, float] = UNSET,
) -> Response[float]:
    """Calculate Base Hourly Rate

    Args:
        employer_id (str):
        id (str):
        pay_period (Union[Unset, None, PayPeriods]):
        pay_basis (Union[Unset, None, PayBasis]):
        pay_amount (Union[Unset, None, float]):

    Returns:
        Response[float]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        client=client,
        pay_period=pay_period,
        pay_basis=pay_basis,
        pay_amount=pay_amount,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    employer_id: str,
    id: str,
    *,
    client: Client,
    pay_period: Union[Unset, None, PayPeriods] = UNSET,
    pay_basis: Union[Unset, None, PayBasis] = UNSET,
    pay_amount: Union[Unset, None, float] = UNSET,
) -> Optional[float]:
    """Calculate Base Hourly Rate

    Args:
        employer_id (str):
        id (str):
        pay_period (Union[Unset, None, PayPeriods]):
        pay_basis (Union[Unset, None, PayBasis]):
        pay_amount (Union[Unset, None, float]):

    Returns:
        Response[float]
    """

    return sync_detailed(
        employer_id=employer_id,
        id=id,
        client=client,
        pay_period=pay_period,
        pay_basis=pay_basis,
        pay_amount=pay_amount,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    id: str,
    *,
    client: Client,
    pay_period: Union[Unset, None, PayPeriods] = UNSET,
    pay_basis: Union[Unset, None, PayBasis] = UNSET,
    pay_amount: Union[Unset, None, float] = UNSET,
) -> Response[float]:
    """Calculate Base Hourly Rate

    Args:
        employer_id (str):
        id (str):
        pay_period (Union[Unset, None, PayPeriods]):
        pay_basis (Union[Unset, None, PayBasis]):
        pay_amount (Union[Unset, None, float]):

    Returns:
        Response[float]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        client=client,
        pay_period=pay_period,
        pay_basis=pay_basis,
        pay_amount=pay_amount,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    id: str,
    *,
    client: Client,
    pay_period: Union[Unset, None, PayPeriods] = UNSET,
    pay_basis: Union[Unset, None, PayBasis] = UNSET,
    pay_amount: Union[Unset, None, float] = UNSET,
) -> Optional[float]:
    """Calculate Base Hourly Rate

    Args:
        employer_id (str):
        id (str):
        pay_period (Union[Unset, None, PayPeriods]):
        pay_basis (Union[Unset, None, PayBasis]):
        pay_amount (Union[Unset, None, float]):

    Returns:
        Response[float]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            id=id,
            client=client,
            pay_period=pay_period,
            pay_basis=pay_basis,
            pay_amount=pay_amount,
        )
    ).parsed
