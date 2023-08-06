from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.rti_submission_settings import RtiSubmissionSettings
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    json_body: RtiSubmissionSettings,
    id: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/tenants/ritsubmissionsettings".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["id"] = id

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[Any, RtiSubmissionSettings]]:
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 200:
        response_200 = RtiSubmissionSettings.from_dict(response.json())

        return response_200
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[Any, RtiSubmissionSettings]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: RtiSubmissionSettings,
    id: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, RtiSubmissionSettings]]:
    """Update RtiSubmissionSettings

     If the Tenant has BureauFeaturesEnabled then they can store RtiSubmissionSettings for use across
    multiple employers.
    This end point updates the RtiSubmissionSettings.

    Args:
        id (Union[Unset, None, str]):
        json_body (RtiSubmissionSettings):

    Returns:
        Response[Union[Any, RtiSubmissionSettings]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
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
    json_body: RtiSubmissionSettings,
    id: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, RtiSubmissionSettings]]:
    """Update RtiSubmissionSettings

     If the Tenant has BureauFeaturesEnabled then they can store RtiSubmissionSettings for use across
    multiple employers.
    This end point updates the RtiSubmissionSettings.

    Args:
        id (Union[Unset, None, str]):
        json_body (RtiSubmissionSettings):

    Returns:
        Response[Union[Any, RtiSubmissionSettings]]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        id=id,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: RtiSubmissionSettings,
    id: Union[Unset, None, str] = UNSET,
) -> Response[Union[Any, RtiSubmissionSettings]]:
    """Update RtiSubmissionSettings

     If the Tenant has BureauFeaturesEnabled then they can store RtiSubmissionSettings for use across
    multiple employers.
    This end point updates the RtiSubmissionSettings.

    Args:
        id (Union[Unset, None, str]):
        json_body (RtiSubmissionSettings):

    Returns:
        Response[Union[Any, RtiSubmissionSettings]]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        id=id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    json_body: RtiSubmissionSettings,
    id: Union[Unset, None, str] = UNSET,
) -> Optional[Union[Any, RtiSubmissionSettings]]:
    """Update RtiSubmissionSettings

     If the Tenant has BureauFeaturesEnabled then they can store RtiSubmissionSettings for use across
    multiple employers.
    This end point updates the RtiSubmissionSettings.

    Args:
        id (Union[Unset, None, str]):
        json_body (RtiSubmissionSettings):

    Returns:
        Response[Union[Any, RtiSubmissionSettings]]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            id=id,
        )
    ).parsed
