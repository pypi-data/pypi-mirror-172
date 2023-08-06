import datetime
from typing import Any, Dict, List, Optional, Union, cast

import httpx

from ...client import Client
from ...models.item import Item
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    *,
    client: Client,
    cyclical_reenrolment_date: Union[Unset, None, datetime.datetime] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/autoenrolment/renrol".format(
        client.base_url, employerId=employer_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_cyclical_reenrolment_date: Union[Unset, None, str] = UNSET
    if not isinstance(cyclical_reenrolment_date, Unset):
        json_cyclical_reenrolment_date = (
            cyclical_reenrolment_date.isoformat() if cyclical_reenrolment_date else None
        )

    params["cyclicalReenrolmentDate"] = json_cyclical_reenrolment_date

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
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
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
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
    cyclical_reenrolment_date: Union[Unset, None, datetime.datetime] = UNSET,
) -> Response[Union[Any, List[Item]]]:
    """Cyclical Re-enrolment

     Performs a Cyclical Re-enrolment. All employees that have opted-out or ceased membership
    will be re-assessed and auto-enrolled if necessary.
    The employers cyclical re-enrolment date will then be updated to the date provided.

    Args:
        employer_id (str):
        cyclical_reenrolment_date (Union[Unset, None, datetime.datetime]):

    Returns:
        Response[Union[Any, List[Item]]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        cyclical_reenrolment_date=cyclical_reenrolment_date,
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
    cyclical_reenrolment_date: Union[Unset, None, datetime.datetime] = UNSET,
) -> Optional[Union[Any, List[Item]]]:
    """Cyclical Re-enrolment

     Performs a Cyclical Re-enrolment. All employees that have opted-out or ceased membership
    will be re-assessed and auto-enrolled if necessary.
    The employers cyclical re-enrolment date will then be updated to the date provided.

    Args:
        employer_id (str):
        cyclical_reenrolment_date (Union[Unset, None, datetime.datetime]):

    Returns:
        Response[Union[Any, List[Item]]]
    """

    return sync_detailed(
        employer_id=employer_id,
        client=client,
        cyclical_reenrolment_date=cyclical_reenrolment_date,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    *,
    client: Client,
    cyclical_reenrolment_date: Union[Unset, None, datetime.datetime] = UNSET,
) -> Response[Union[Any, List[Item]]]:
    """Cyclical Re-enrolment

     Performs a Cyclical Re-enrolment. All employees that have opted-out or ceased membership
    will be re-assessed and auto-enrolled if necessary.
    The employers cyclical re-enrolment date will then be updated to the date provided.

    Args:
        employer_id (str):
        cyclical_reenrolment_date (Union[Unset, None, datetime.datetime]):

    Returns:
        Response[Union[Any, List[Item]]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        cyclical_reenrolment_date=cyclical_reenrolment_date,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    *,
    client: Client,
    cyclical_reenrolment_date: Union[Unset, None, datetime.datetime] = UNSET,
) -> Optional[Union[Any, List[Item]]]:
    """Cyclical Re-enrolment

     Performs a Cyclical Re-enrolment. All employees that have opted-out or ceased membership
    will be re-assessed and auto-enrolled if necessary.
    The employers cyclical re-enrolment date will then be updated to the date provided.

    Args:
        employer_id (str):
        cyclical_reenrolment_date (Union[Unset, None, datetime.datetime]):

    Returns:
        Response[Union[Any, List[Item]]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            client=client,
            cyclical_reenrolment_date=cyclical_reenrolment_date,
        )
    ).parsed
