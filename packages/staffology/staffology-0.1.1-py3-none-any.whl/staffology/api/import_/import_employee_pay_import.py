from typing import Any, Dict, List, Union

import httpx

from ...client import Client
from ...models.pay_options_import import PayOptionsImport
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    *,
    client: Client,
    json_body: List[PayOptionsImport],
    lines_only: Union[Unset, None, bool] = False,
    append: Union[Unset, None, bool] = False,
    update_existing: Union[Unset, None, bool] = False,
    validate_only: Union[Unset, None, bool] = False,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/import/pay".format(
        client.base_url, employerId=employer_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["linesOnly"] = lines_only

    params["append"] = append

    params["updateExisting"] = update_existing

    params["validateOnly"] = validate_only

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = []
    for json_body_item_data in json_body:
        json_body_item = json_body_item_data.to_dict()

        json_json_body.append(json_body_item)

    return {
        "method": "post",
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
    *,
    client: Client,
    json_body: List[PayOptionsImport],
    lines_only: Union[Unset, None, bool] = False,
    append: Union[Unset, None, bool] = False,
    update_existing: Union[Unset, None, bool] = False,
    validate_only: Union[Unset, None, bool] = False,
) -> Response[Any]:
    """Import Pay To Employee

     Takes a list PayOptionsImport and updates employees PayOptions to use the values provided.

    Args:
        employer_id (str):
        lines_only (Union[Unset, None, bool]):
        append (Union[Unset, None, bool]):
        update_existing (Union[Unset, None, bool]):
        validate_only (Union[Unset, None, bool]):
        json_body (List[PayOptionsImport]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        json_body=json_body,
        lines_only=lines_only,
        append=append,
        update_existing=update_existing,
        validate_only=validate_only,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


async def asyncio_detailed(
    employer_id: str,
    *,
    client: Client,
    json_body: List[PayOptionsImport],
    lines_only: Union[Unset, None, bool] = False,
    append: Union[Unset, None, bool] = False,
    update_existing: Union[Unset, None, bool] = False,
    validate_only: Union[Unset, None, bool] = False,
) -> Response[Any]:
    """Import Pay To Employee

     Takes a list PayOptionsImport and updates employees PayOptions to use the values provided.

    Args:
        employer_id (str):
        lines_only (Union[Unset, None, bool]):
        append (Union[Unset, None, bool]):
        update_existing (Union[Unset, None, bool]):
        validate_only (Union[Unset, None, bool]):
        json_body (List[PayOptionsImport]):

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        json_body=json_body,
        lines_only=lines_only,
        append=append,
        update_existing=update_existing,
        validate_only=validate_only,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)
