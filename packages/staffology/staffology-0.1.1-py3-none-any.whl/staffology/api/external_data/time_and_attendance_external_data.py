import datetime
from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.external_data_provider_id import ExternalDataProviderId
from ...models.pay_options_import import PayOptionsImport
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    id: ExternalDataProviderId,
    *,
    client: Client,
    from_: Union[Unset, None, datetime.datetime] = UNSET,
    to: Union[Unset, None, datetime.datetime] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/external-data/{id}/time-and-attendance".format(
        client.base_url, employerId=employer_id, id=id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_from_: Union[Unset, None, str] = UNSET
    if not isinstance(from_, Unset):
        json_from_ = from_.isoformat() if from_ else None

    params["from"] = json_from_

    json_to: Union[Unset, None, str] = UNSET
    if not isinstance(to, Unset):
        json_to = to.isoformat() if to else None

    params["to"] = json_to

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, response: httpx.Response) -> Optional[List[PayOptionsImport]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = PayOptionsImport.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[List[PayOptionsImport]]:
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
    from_: Union[Unset, None, datetime.datetime] = UNSET,
    to: Union[Unset, None, datetime.datetime] = UNSET,
) -> Response[List[PayOptionsImport]]:
    """Get Time And Attendance Data

     Return a list of PayOptionsImport representing Time and Attendance data from the specified
    ExternalDataProvider, for to specified date range

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        from_ (Union[Unset, None, datetime.datetime]):
        to (Union[Unset, None, datetime.datetime]):

    Returns:
        Response[List[PayOptionsImport]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        client=client,
        from_=from_,
        to=to,
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
    from_: Union[Unset, None, datetime.datetime] = UNSET,
    to: Union[Unset, None, datetime.datetime] = UNSET,
) -> Optional[List[PayOptionsImport]]:
    """Get Time And Attendance Data

     Return a list of PayOptionsImport representing Time and Attendance data from the specified
    ExternalDataProvider, for to specified date range

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        from_ (Union[Unset, None, datetime.datetime]):
        to (Union[Unset, None, datetime.datetime]):

    Returns:
        Response[List[PayOptionsImport]]
    """

    return sync_detailed(
        employer_id=employer_id,
        id=id,
        client=client,
        from_=from_,
        to=to,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    id: ExternalDataProviderId,
    *,
    client: Client,
    from_: Union[Unset, None, datetime.datetime] = UNSET,
    to: Union[Unset, None, datetime.datetime] = UNSET,
) -> Response[List[PayOptionsImport]]:
    """Get Time And Attendance Data

     Return a list of PayOptionsImport representing Time and Attendance data from the specified
    ExternalDataProvider, for to specified date range

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        from_ (Union[Unset, None, datetime.datetime]):
        to (Union[Unset, None, datetime.datetime]):

    Returns:
        Response[List[PayOptionsImport]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        client=client,
        from_=from_,
        to=to,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    id: ExternalDataProviderId,
    *,
    client: Client,
    from_: Union[Unset, None, datetime.datetime] = UNSET,
    to: Union[Unset, None, datetime.datetime] = UNSET,
) -> Optional[List[PayOptionsImport]]:
    """Get Time And Attendance Data

     Return a list of PayOptionsImport representing Time and Attendance data from the specified
    ExternalDataProvider, for to specified date range

    Args:
        employer_id (str):
        id (ExternalDataProviderId):
        from_ (Union[Unset, None, datetime.datetime]):
        to (Union[Unset, None, datetime.datetime]):

    Returns:
        Response[List[PayOptionsImport]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            id=id,
            client=client,
            from_=from_,
            to=to,
        )
    ).parsed
