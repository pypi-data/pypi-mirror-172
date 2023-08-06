from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.external_data_provider_id import ExternalDataProviderId
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    id: ExternalDataProviderId,
    *,
    client: Client,
    return_url: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/external-data/{id}/authorize".format(
        client.base_url, employerId=employer_id, id=id
    )

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
    employer_id: str,
    id: ExternalDataProviderId,
    *,
    client: Client,
    return_url: Union[Unset, None, str] = UNSET,
) -> Response[str]:
    """Get Authorization Url

     For ExternalDataProviders with an AuthScheme of OAuth1 or OAuth2.
    Returns a Url to redirect a user to in order to start the authorization process with the given
    ExternalDataProvider.
    Our API handles the response from the OAuth provider and processes it to obtain a token.
    The user is then sent to the URL specified.

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        return_url (Union[Unset, None, str]):

    Returns:
        Response[str]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        client=client,
        return_url=return_url,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    employer_id: str,
    id: ExternalDataProviderId,
    *,
    client: Client,
    return_url: Union[Unset, None, str] = UNSET,
) -> Optional[str]:
    """Get Authorization Url

     For ExternalDataProviders with an AuthScheme of OAuth1 or OAuth2.
    Returns a Url to redirect a user to in order to start the authorization process with the given
    ExternalDataProvider.
    Our API handles the response from the OAuth provider and processes it to obtain a token.
    The user is then sent to the URL specified.

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        return_url (Union[Unset, None, str]):

    Returns:
        Response[str]
    """

    return sync_detailed(
        employer_id=employer_id,
        id=id,
        client=client,
        return_url=return_url,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    id: ExternalDataProviderId,
    *,
    client: Client,
    return_url: Union[Unset, None, str] = UNSET,
) -> Response[str]:
    """Get Authorization Url

     For ExternalDataProviders with an AuthScheme of OAuth1 or OAuth2.
    Returns a Url to redirect a user to in order to start the authorization process with the given
    ExternalDataProvider.
    Our API handles the response from the OAuth provider and processes it to obtain a token.
    The user is then sent to the URL specified.

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        return_url (Union[Unset, None, str]):

    Returns:
        Response[str]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        client=client,
        return_url=return_url,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    id: ExternalDataProviderId,
    *,
    client: Client,
    return_url: Union[Unset, None, str] = UNSET,
) -> Optional[str]:
    """Get Authorization Url

     For ExternalDataProviders with an AuthScheme of OAuth1 or OAuth2.
    Returns a Url to redirect a user to in order to start the authorization process with the given
    ExternalDataProvider.
    Our API handles the response from the OAuth provider and processes it to obtain a token.
    The user is then sent to the URL specified.

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        return_url (Union[Unset, None, str]):

    Returns:
        Response[str]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            id=id,
            client=client,
            return_url=return_url,
        )
    ).parsed
