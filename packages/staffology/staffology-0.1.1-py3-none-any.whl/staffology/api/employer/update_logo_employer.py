from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.employer import Employer
from ...models.update_logo_employer_multipart_data import (
    UpdateLogoEmployerMultipartData,
)
from ...types import Response


def _get_kwargs(
    id: str,
    *,
    client: Client,
    multipart_data: UpdateLogoEmployerMultipartData,
) -> Dict[str, Any]:
    url = "{}/employers/{id}/logo".format(client.base_url, id=id)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    multipart_multipart_data = multipart_data.to_multipart()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "files": multipart_multipart_data,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Employer]:
    if response.status_code == 200:
        response_200 = Employer.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Employer]:
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
    multipart_data: UpdateLogoEmployerMultipartData,
) -> Response[Employer]:
    """Update Employer Logo

     If you already have a URL for the employer Logo then you can just set the LogoUrl property of the
    Employer.
    Alternatively, submit a logo here and we'll upload it and set the LogoUrl for you.

    Args:
        id (str):
        multipart_data (UpdateLogoEmployerMultipartData):

    Returns:
        Response[Employer]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        multipart_data=multipart_data,
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
    multipart_data: UpdateLogoEmployerMultipartData,
) -> Optional[Employer]:
    """Update Employer Logo

     If you already have a URL for the employer Logo then you can just set the LogoUrl property of the
    Employer.
    Alternatively, submit a logo here and we'll upload it and set the LogoUrl for you.

    Args:
        id (str):
        multipart_data (UpdateLogoEmployerMultipartData):

    Returns:
        Response[Employer]
    """

    return sync_detailed(
        id=id,
        client=client,
        multipart_data=multipart_data,
    ).parsed


async def asyncio_detailed(
    id: str,
    *,
    client: Client,
    multipart_data: UpdateLogoEmployerMultipartData,
) -> Response[Employer]:
    """Update Employer Logo

     If you already have a URL for the employer Logo then you can just set the LogoUrl property of the
    Employer.
    Alternatively, submit a logo here and we'll upload it and set the LogoUrl for you.

    Args:
        id (str):
        multipart_data (UpdateLogoEmployerMultipartData):

    Returns:
        Response[Employer]
    """

    kwargs = _get_kwargs(
        id=id,
        client=client,
        multipart_data=multipart_data,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    id: str,
    *,
    client: Client,
    multipart_data: UpdateLogoEmployerMultipartData,
) -> Optional[Employer]:
    """Update Employer Logo

     If you already have a URL for the employer Logo then you can just set the LogoUrl property of the
    Employer.
    Alternatively, submit a logo here and we'll upload it and set the LogoUrl for you.

    Args:
        id (str):
        multipart_data (UpdateLogoEmployerMultipartData):

    Returns:
        Response[Employer]
    """

    return (
        await asyncio_detailed(
            id=id,
            client=client,
            multipart_data=multipart_data,
        )
    ).parsed
