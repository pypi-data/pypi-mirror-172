from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    return_url: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/billing/directdebit/setup".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["returnUrl"] = return_url

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[str]:
    if response.status_code == 200:
        response_200 = cast(str, response.json())
        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[str]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    return_url: Union[Unset, None, str] = UNSET,
) -> Response[str]:
    """Setup DirectDebitMandate

     Returns a Url to redirect a user to in order to start the process of setting up a Direct Debit
    Mandate.
    Once the process is complete then the user is sent to the URL specified.

    Args:
        return_url (Union[Unset, None, str]):

    Returns:
        Response[str]
    """

    kwargs = _get_kwargs(
        client=client,
        return_url=return_url,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    return_url: Union[Unset, None, str] = UNSET,
) -> Optional[str]:
    """Setup DirectDebitMandate

     Returns a Url to redirect a user to in order to start the process of setting up a Direct Debit
    Mandate.
    Once the process is complete then the user is sent to the URL specified.

    Args:
        return_url (Union[Unset, None, str]):

    Returns:
        Response[str]
    """

    return sync_detailed(
        client=client,
        return_url=return_url,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    return_url: Union[Unset, None, str] = UNSET,
) -> Response[str]:
    """Setup DirectDebitMandate

     Returns a Url to redirect a user to in order to start the process of setting up a Direct Debit
    Mandate.
    Once the process is complete then the user is sent to the URL specified.

    Args:
        return_url (Union[Unset, None, str]):

    Returns:
        Response[str]
    """

    kwargs = _get_kwargs(
        client=client,
        return_url=return_url,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    return_url: Union[Unset, None, str] = UNSET,
) -> Optional[str]:
    """Setup DirectDebitMandate

     Returns a Url to redirect a user to in order to start the process of setting up a Direct Debit
    Mandate.
    Once the process is complete then the user is sent to the URL specified.

    Args:
        return_url (Union[Unset, None, str]):

    Returns:
        Response[str]
    """

    return (
        await asyncio_detailed(
            client=client,
            return_url=return_url,
        )
    ).parsed
