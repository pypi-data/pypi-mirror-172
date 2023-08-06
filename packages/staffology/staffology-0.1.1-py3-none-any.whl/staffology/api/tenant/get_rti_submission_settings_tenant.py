from typing import Any, Dict, Optional, Union

import httpx

from ...client import Client
from ...models.rti_submission_settings import RtiSubmissionSettings
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    id: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/tenants/ritsubmissionsettings".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["id"] = id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[RtiSubmissionSettings]:
    if response.status_code == 200:
        response_200 = RtiSubmissionSettings.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[RtiSubmissionSettings]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    id: Union[Unset, None, str] = UNSET,
) -> Response[RtiSubmissionSettings]:
    """Get RtiSubmissionSettings

     If the Tenant has BureauFeaturesEnabled then they can store RtiSubmissionSettings for use across
    multiple employers.
    This end point returns them RtiSubmissionSettings.

    Args:
        id (Union[Unset, None, str]):

    Returns:
        Response[RtiSubmissionSettings]
    """

    kwargs = _get_kwargs(
        client=client,
        id=id,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    id: Union[Unset, None, str] = UNSET,
) -> Optional[RtiSubmissionSettings]:
    """Get RtiSubmissionSettings

     If the Tenant has BureauFeaturesEnabled then they can store RtiSubmissionSettings for use across
    multiple employers.
    This end point returns them RtiSubmissionSettings.

    Args:
        id (Union[Unset, None, str]):

    Returns:
        Response[RtiSubmissionSettings]
    """

    return sync_detailed(
        client=client,
        id=id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    id: Union[Unset, None, str] = UNSET,
) -> Response[RtiSubmissionSettings]:
    """Get RtiSubmissionSettings

     If the Tenant has BureauFeaturesEnabled then they can store RtiSubmissionSettings for use across
    multiple employers.
    This end point returns them RtiSubmissionSettings.

    Args:
        id (Union[Unset, None, str]):

    Returns:
        Response[RtiSubmissionSettings]
    """

    kwargs = _get_kwargs(
        client=client,
        id=id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    id: Union[Unset, None, str] = UNSET,
) -> Optional[RtiSubmissionSettings]:
    """Get RtiSubmissionSettings

     If the Tenant has BureauFeaturesEnabled then they can store RtiSubmissionSettings for use across
    multiple employers.
    This end point returns them RtiSubmissionSettings.

    Args:
        id (Union[Unset, None, str]):

    Returns:
        Response[RtiSubmissionSettings]
    """

    return (
        await asyncio_detailed(
            client=client,
            id=id,
        )
    ).parsed
