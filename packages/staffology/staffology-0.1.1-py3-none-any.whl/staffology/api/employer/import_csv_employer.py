from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.import_csv_employer_multipart_data import ImportCsvEmployerMultipartData
from ...models.item import Item
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    multipart_data: ImportCsvEmployerMultipartData,
    preview_only: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/employers/import".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["previewOnly"] = preview_only

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    multipart_multipart_data = multipart_data.to_multipart()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "files": multipart_multipart_data,
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[List[Item]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[List[Item]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    multipart_data: ImportCsvEmployerMultipartData,
    preview_only: Union[Unset, None, bool] = False,
) -> Response[List[Item]]:
    """Import CSV

     Import employers from a CSV file.

    Args:
        preview_only (Union[Unset, None, bool]):
        multipart_data (ImportCsvEmployerMultipartData):

    Returns:
        Response[List[Item]]
    """

    kwargs = _get_kwargs(
        client=client,
        multipart_data=multipart_data,
        preview_only=preview_only,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    multipart_data: ImportCsvEmployerMultipartData,
    preview_only: Union[Unset, None, bool] = False,
) -> Optional[List[Item]]:
    """Import CSV

     Import employers from a CSV file.

    Args:
        preview_only (Union[Unset, None, bool]):
        multipart_data (ImportCsvEmployerMultipartData):

    Returns:
        Response[List[Item]]
    """

    return sync_detailed(
        client=client,
        multipart_data=multipart_data,
        preview_only=preview_only,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    multipart_data: ImportCsvEmployerMultipartData,
    preview_only: Union[Unset, None, bool] = False,
) -> Response[List[Item]]:
    """Import CSV

     Import employers from a CSV file.

    Args:
        preview_only (Union[Unset, None, bool]):
        multipart_data (ImportCsvEmployerMultipartData):

    Returns:
        Response[List[Item]]
    """

    kwargs = _get_kwargs(
        client=client,
        multipart_data=multipart_data,
        preview_only=preview_only,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    multipart_data: ImportCsvEmployerMultipartData,
    preview_only: Union[Unset, None, bool] = False,
) -> Optional[List[Item]]:
    """Import CSV

     Import employers from a CSV file.

    Args:
        preview_only (Union[Unset, None, bool]):
        multipart_data (ImportCsvEmployerMultipartData):

    Returns:
        Response[List[Item]]
    """

    return (
        await asyncio_detailed(
            client=client,
            multipart_data=multipart_data,
            preview_only=preview_only,
        )
    ).parsed
