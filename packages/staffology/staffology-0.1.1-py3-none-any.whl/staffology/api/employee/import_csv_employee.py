from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import Client
from ...models.csv_file_format import CsvFileFormat
from ...models.import_csv_employee_multipart_data import ImportCsvEmployeeMultipartData
from ...models.item import Item
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    *,
    client: Client,
    multipart_data: ImportCsvEmployeeMultipartData,
    format_: Union[Unset, None, CsvFileFormat] = UNSET,
    preview_only: Union[Unset, None, bool] = False,
    allow_updates: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/employees/import".format(
        client.base_url, employerId=employer_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_format_: Union[Unset, None, str] = UNSET
    if not isinstance(format_, Unset):
        json_format_ = format_.value if format_ else None

    params["format"] = json_format_

    params["previewOnly"] = preview_only

    params["allowUpdates"] = allow_updates

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
    *,
    client: Client,
    multipart_data: ImportCsvEmployeeMultipartData,
    format_: Union[Unset, None, CsvFileFormat] = UNSET,
    preview_only: Union[Unset, None, bool] = False,
    allow_updates: Union[Unset, None, bool] = False,
) -> Response[Union[Any, List[Item]]]:
    """Import CSV

     Import employee data from a CSV file.

    Args:
        employer_id (str):
        format_ (Union[Unset, None, CsvFileFormat]):
        preview_only (Union[Unset, None, bool]):
        allow_updates (Union[Unset, None, bool]):
        multipart_data (ImportCsvEmployeeMultipartData):

    Returns:
        Response[Union[Any, List[Item]]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        multipart_data=multipart_data,
        format_=format_,
        preview_only=preview_only,
        allow_updates=allow_updates,
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
    multipart_data: ImportCsvEmployeeMultipartData,
    format_: Union[Unset, None, CsvFileFormat] = UNSET,
    preview_only: Union[Unset, None, bool] = False,
    allow_updates: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, List[Item]]]:
    """Import CSV

     Import employee data from a CSV file.

    Args:
        employer_id (str):
        format_ (Union[Unset, None, CsvFileFormat]):
        preview_only (Union[Unset, None, bool]):
        allow_updates (Union[Unset, None, bool]):
        multipart_data (ImportCsvEmployeeMultipartData):

    Returns:
        Response[Union[Any, List[Item]]]
    """

    return sync_detailed(
        employer_id=employer_id,
        client=client,
        multipart_data=multipart_data,
        format_=format_,
        preview_only=preview_only,
        allow_updates=allow_updates,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    *,
    client: Client,
    multipart_data: ImportCsvEmployeeMultipartData,
    format_: Union[Unset, None, CsvFileFormat] = UNSET,
    preview_only: Union[Unset, None, bool] = False,
    allow_updates: Union[Unset, None, bool] = False,
) -> Response[Union[Any, List[Item]]]:
    """Import CSV

     Import employee data from a CSV file.

    Args:
        employer_id (str):
        format_ (Union[Unset, None, CsvFileFormat]):
        preview_only (Union[Unset, None, bool]):
        allow_updates (Union[Unset, None, bool]):
        multipart_data (ImportCsvEmployeeMultipartData):

    Returns:
        Response[Union[Any, List[Item]]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        multipart_data=multipart_data,
        format_=format_,
        preview_only=preview_only,
        allow_updates=allow_updates,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    *,
    client: Client,
    multipart_data: ImportCsvEmployeeMultipartData,
    format_: Union[Unset, None, CsvFileFormat] = UNSET,
    preview_only: Union[Unset, None, bool] = False,
    allow_updates: Union[Unset, None, bool] = False,
) -> Optional[Union[Any, List[Item]]]:
    """Import CSV

     Import employee data from a CSV file.

    Args:
        employer_id (str):
        format_ (Union[Unset, None, CsvFileFormat]):
        preview_only (Union[Unset, None, bool]):
        allow_updates (Union[Unset, None, bool]):
        multipart_data (ImportCsvEmployeeMultipartData):

    Returns:
        Response[Union[Any, List[Item]]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            client=client,
            multipart_data=multipart_data,
            format_=format_,
            preview_only=preview_only,
            allow_updates=allow_updates,
        )
    ).parsed
