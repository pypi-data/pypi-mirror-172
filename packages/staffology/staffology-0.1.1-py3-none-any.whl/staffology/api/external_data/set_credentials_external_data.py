from typing import Any, Dict, List, Union

import httpx

from ...client import Client
from ...models.external_data_provider_id import ExternalDataProviderId
from ...models.string_string_key_value_pair import StringStringKeyValuePair
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    id: ExternalDataProviderId,
    *,
    client: Client,
    json_body: List[StringStringKeyValuePair],
    username: Union[Unset, None, str] = UNSET,
    password: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/external-data/{id}/authorize".format(
        client.base_url, employerId=employer_id, id=id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["username"] = username

    params["password"] = password

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = []
    for json_body_item_data in json_body:
        json_body_item = json_body_item_data.to_dict()

        json_json_body.append(json_body_item)

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
        "params": params,
    }


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    employer_id: str,
    id: ExternalDataProviderId,
    *,
    client: Client,
    json_body: List[StringStringKeyValuePair],
    username: Union[Unset, None, str] = UNSET,
    password: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """Set Credentials

     For ExternalDataProviders with an AuthScheme of Basic.
    Sets the username and password for the service.

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        username (Union[Unset, None, str]):
        password (Union[Unset, None, str]):
        json_body (List[StringStringKeyValuePair]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        client=client,
        json_body=json_body,
        username=username,
        password=password,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    employer_id: str,
    id: ExternalDataProviderId,
    *,
    client: Client,
    json_body: List[StringStringKeyValuePair],
    username: Union[Unset, None, str] = UNSET,
    password: Union[Unset, None, str] = UNSET,
) -> Response[Any]:
    """Set Credentials

     For ExternalDataProviders with an AuthScheme of Basic.
    Sets the username and password for the service.

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        username (Union[Unset, None, str]):
        password (Union[Unset, None, str]):
        json_body (List[StringStringKeyValuePair]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        client=client,
        json_body=json_body,
        username=username,
        password=password,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
