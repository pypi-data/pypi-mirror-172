from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    *,
    client: Client,
    u: Union[Unset, None, str] = UNSET,
    k: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/email/settings/verify".format(
        client.base_url, employerId=employer_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["u"] = u

    params["k"] = k

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
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
    *,
    client: Client,
    u: Union[Unset, None, str] = UNSET,
    k: Union[Unset, None, str] = UNSET,
) -> Response[bool]:
    """Email Verification (Respond)

     Used to process the link sent in an email to verify an email address that's being used in
    MailSettings.

    Args:
        employer_id (str):
        u (Union[Unset, None, str]):
        k (Union[Unset, None, str]):

    Returns:
        Response[bool]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        u=u,
        k=k,
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
    u: Union[Unset, None, str] = UNSET,
    k: Union[Unset, None, str] = UNSET,
) -> Optional[bool]:
    """Email Verification (Respond)

     Used to process the link sent in an email to verify an email address that's being used in
    MailSettings.

    Args:
        employer_id (str):
        u (Union[Unset, None, str]):
        k (Union[Unset, None, str]):

    Returns:
        Response[bool]
    """

    return sync_detailed(
        employer_id=employer_id,
        client=client,
        u=u,
        k=k,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    *,
    client: Client,
    u: Union[Unset, None, str] = UNSET,
    k: Union[Unset, None, str] = UNSET,
) -> Response[bool]:
    """Email Verification (Respond)

     Used to process the link sent in an email to verify an email address that's being used in
    MailSettings.

    Args:
        employer_id (str):
        u (Union[Unset, None, str]):
        k (Union[Unset, None, str]):

    Returns:
        Response[bool]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        u=u,
        k=k,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    *,
    client: Client,
    u: Union[Unset, None, str] = UNSET,
    k: Union[Unset, None, str] = UNSET,
) -> Optional[bool]:
    """Email Verification (Respond)

     Used to process the link sent in an email to verify an email address that's being used in
    MailSettings.

    Args:
        employer_id (str):
        u (Union[Unset, None, str]):
        k (Union[Unset, None, str]):

    Returns:
        Response[bool]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            client=client,
            u=u,
            k=k,
        )
    ).parsed
