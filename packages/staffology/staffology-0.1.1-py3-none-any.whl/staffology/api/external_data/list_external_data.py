from typing import Any, Dict, List, Optional

import httpx

from ...client import Client
from ...models.external_data_provider import ExternalDataProvider
from ...types import Response


def _get_kwargs(
    employer_id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/external-data".format(
        client.base_url, employerId=employer_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[List[ExternalDataProvider]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = ExternalDataProvider.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[List[ExternalDataProvider]]:
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
) -> Response[List[ExternalDataProvider]]:
    """List Providers

     Returns a list of External Data Providers and indicates which the Employer has successfully
    authenticated with.

    Args:
        employer_id (str):

    Returns:
        Response[List[ExternalDataProvider]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
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
) -> Optional[List[ExternalDataProvider]]:
    """List Providers

     Returns a list of External Data Providers and indicates which the Employer has successfully
    authenticated with.

    Args:
        employer_id (str):

    Returns:
        Response[List[ExternalDataProvider]]
    """

    return sync_detailed(
        employer_id=employer_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    *,
    client: Client,
) -> Response[List[ExternalDataProvider]]:
    """List Providers

     Returns a list of External Data Providers and indicates which the Employer has successfully
    authenticated with.

    Args:
        employer_id (str):

    Returns:
        Response[List[ExternalDataProvider]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    *,
    client: Client,
) -> Optional[List[ExternalDataProvider]]:
    """List Providers

     Returns a list of External Data Providers and indicates which the Employer has successfully
    authenticated with.

    Args:
        employer_id (str):

    Returns:
        Response[List[ExternalDataProvider]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            client=client,
        )
    ).parsed
