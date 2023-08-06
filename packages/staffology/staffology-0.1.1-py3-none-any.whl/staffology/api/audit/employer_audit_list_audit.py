import datetime
from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.entity_type import EntityType
from ...models.item import Item
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    *,
    client: Client,
    entity: Union[Unset, None, EntityType] = UNSET,
    entity_id: Union[Unset, None, str] = UNSET,
    from_date: Union[Unset, None, datetime.datetime] = UNSET,
    to_date: Union[Unset, None, datetime.datetime] = UNSET,
    page_num: Union[Unset, None, int] = UNSET,
    page_size: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/audit".format(
        client.base_url, employerId=employer_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    json_entity: Union[Unset, None, str] = UNSET
    if not isinstance(entity, Unset):
        json_entity = entity.value if entity else None

    params["entity"] = json_entity

    params["entityId"] = entity_id

    json_from_date: Union[Unset, None, str] = UNSET
    if not isinstance(from_date, Unset):
        json_from_date = from_date.isoformat() if from_date else None

    params["fromDate"] = json_from_date

    json_to_date: Union[Unset, None, str] = UNSET
    if not isinstance(to_date, Unset):
        json_to_date = to_date.isoformat() if to_date else None

    params["toDate"] = json_to_date

    params["pageNum"] = page_num

    params["pageSize"] = page_size

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
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
    employer_id: str,
    *,
    client: Client,
    entity: Union[Unset, None, EntityType] = UNSET,
    entity_id: Union[Unset, None, str] = UNSET,
    from_date: Union[Unset, None, datetime.datetime] = UNSET,
    to_date: Union[Unset, None, datetime.datetime] = UNSET,
    page_num: Union[Unset, None, int] = UNSET,
    page_size: Union[Unset, None, int] = UNSET,
) -> Response[List[Item]]:
    """Employer Audit Log

    Args:
        employer_id (str):
        entity (Union[Unset, None, EntityType]): [readonly] Specifies the entity for which audit
            logs need to retrieved
        entity_id (Union[Unset, None, str]):
        from_date (Union[Unset, None, datetime.datetime]):
        to_date (Union[Unset, None, datetime.datetime]):
        page_num (Union[Unset, None, int]):
        page_size (Union[Unset, None, int]):

    Returns:
        Response[List[Item]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        entity=entity,
        entity_id=entity_id,
        from_date=from_date,
        to_date=to_date,
        page_num=page_num,
        page_size=page_size,
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
    entity: Union[Unset, None, EntityType] = UNSET,
    entity_id: Union[Unset, None, str] = UNSET,
    from_date: Union[Unset, None, datetime.datetime] = UNSET,
    to_date: Union[Unset, None, datetime.datetime] = UNSET,
    page_num: Union[Unset, None, int] = UNSET,
    page_size: Union[Unset, None, int] = UNSET,
) -> Optional[List[Item]]:
    """Employer Audit Log

    Args:
        employer_id (str):
        entity (Union[Unset, None, EntityType]): [readonly] Specifies the entity for which audit
            logs need to retrieved
        entity_id (Union[Unset, None, str]):
        from_date (Union[Unset, None, datetime.datetime]):
        to_date (Union[Unset, None, datetime.datetime]):
        page_num (Union[Unset, None, int]):
        page_size (Union[Unset, None, int]):

    Returns:
        Response[List[Item]]
    """

    return sync_detailed(
        employer_id=employer_id,
        client=client,
        entity=entity,
        entity_id=entity_id,
        from_date=from_date,
        to_date=to_date,
        page_num=page_num,
        page_size=page_size,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    *,
    client: Client,
    entity: Union[Unset, None, EntityType] = UNSET,
    entity_id: Union[Unset, None, str] = UNSET,
    from_date: Union[Unset, None, datetime.datetime] = UNSET,
    to_date: Union[Unset, None, datetime.datetime] = UNSET,
    page_num: Union[Unset, None, int] = UNSET,
    page_size: Union[Unset, None, int] = UNSET,
) -> Response[List[Item]]:
    """Employer Audit Log

    Args:
        employer_id (str):
        entity (Union[Unset, None, EntityType]): [readonly] Specifies the entity for which audit
            logs need to retrieved
        entity_id (Union[Unset, None, str]):
        from_date (Union[Unset, None, datetime.datetime]):
        to_date (Union[Unset, None, datetime.datetime]):
        page_num (Union[Unset, None, int]):
        page_size (Union[Unset, None, int]):

    Returns:
        Response[List[Item]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        entity=entity,
        entity_id=entity_id,
        from_date=from_date,
        to_date=to_date,
        page_num=page_num,
        page_size=page_size,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    *,
    client: Client,
    entity: Union[Unset, None, EntityType] = UNSET,
    entity_id: Union[Unset, None, str] = UNSET,
    from_date: Union[Unset, None, datetime.datetime] = UNSET,
    to_date: Union[Unset, None, datetime.datetime] = UNSET,
    page_num: Union[Unset, None, int] = UNSET,
    page_size: Union[Unset, None, int] = UNSET,
) -> Optional[List[Item]]:
    """Employer Audit Log

    Args:
        employer_id (str):
        entity (Union[Unset, None, EntityType]): [readonly] Specifies the entity for which audit
            logs need to retrieved
        entity_id (Union[Unset, None, str]):
        from_date (Union[Unset, None, datetime.datetime]):
        to_date (Union[Unset, None, datetime.datetime]):
        page_num (Union[Unset, None, int]):
        page_size (Union[Unset, None, int]):

    Returns:
        Response[List[Item]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            client=client,
            entity=entity,
            entity_id=entity_id,
            from_date=from_date,
            to_date=to_date,
            page_num=page_num,
            page_size=page_size,
        )
    ).parsed
