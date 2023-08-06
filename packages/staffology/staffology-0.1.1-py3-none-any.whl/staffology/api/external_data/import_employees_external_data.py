from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import Client
from ...models.external_data_provider_id import ExternalDataProviderId
from ...models.item import Item
from ...types import Response


def _get_kwargs(
    employer_id: str,
    id: ExternalDataProviderId,
    *,
    client: Client,
    json_body: List[str],
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/external-data/{id}/employees".format(
        client.base_url, employerId=employer_id, id=id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Union[Any, List[Item]]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if response.status_code == 409:
        response_409 = cast(Any, None)
        return response_409
    return None


def _build_response(*, response: httpx.Response) -> Response[Union[Any, List[Item]]]:
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
    json_body: List[str],
) -> Response[Union[Any, List[Item]]]:
    """Import Employees

     Import Employees from the external data provider.

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        json_body (List[str]):

    Returns:
        Response[Union[Any, List[Item]]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        client=client,
        json_body=json_body,
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
    json_body: List[str],
) -> Optional[Union[Any, List[Item]]]:
    """Import Employees

     Import Employees from the external data provider.

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        json_body (List[str]):

    Returns:
        Response[Union[Any, List[Item]]]
    """

    return sync_detailed(
        employer_id=employer_id,
        id=id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    id: ExternalDataProviderId,
    *,
    client: Client,
    json_body: List[str],
) -> Response[Union[Any, List[Item]]]:
    """Import Employees

     Import Employees from the external data provider.

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        json_body (List[str]):

    Returns:
        Response[Union[Any, List[Item]]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    id: ExternalDataProviderId,
    *,
    client: Client,
    json_body: List[str],
) -> Optional[Union[Any, List[Item]]]:
    """Import Employees

     Import Employees from the external data provider.

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        json_body (List[str]):

    Returns:
        Response[Union[Any, List[Item]]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            id=id,
            client=client,
            json_body=json_body,
        )
    ).parsed
