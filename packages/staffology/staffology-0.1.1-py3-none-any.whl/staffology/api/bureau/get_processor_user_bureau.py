from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.user import User
from ...types import Response


def _get_kwargs(
    employer_id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/bureau/settings/processor".format(
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


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, User]]:
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    if response.status_code == 200:
        response_200 = User.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, User]]:
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
) -> Response[Union[Any, User]]:
    """Get Processor

     If a Processor is specified in the BureauSettings then it is returned as a User, otherwise a 404 is
    returned

    Args:
        employer_id (str):

    Returns:
        Response[Union[Any, User]]
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
) -> Optional[Union[Any, User]]:
    """Get Processor

     If a Processor is specified in the BureauSettings then it is returned as a User, otherwise a 404 is
    returned

    Args:
        employer_id (str):

    Returns:
        Response[Union[Any, User]]
    """

    return sync_detailed(
        employer_id=employer_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    *,
    client: Client,
) -> Response[Union[Any, User]]:
    """Get Processor

     If a Processor is specified in the BureauSettings then it is returned as a User, otherwise a 404 is
    returned

    Args:
        employer_id (str):

    Returns:
        Response[Union[Any, User]]
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
) -> Optional[Union[Any, User]]:
    """Get Processor

     If a Processor is specified in the BureauSettings then it is returned as a User, otherwise a 404 is
    returned

    Args:
        employer_id (str):

    Returns:
        Response[Union[Any, User]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            client=client,
        )
    ).parsed
