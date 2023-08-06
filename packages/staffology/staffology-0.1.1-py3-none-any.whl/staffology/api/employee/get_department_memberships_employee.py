from typing import Any, Dict, List, Optional

import httpx

from ...client import Client
from ...models.department_membership import DepartmentMembership
from ...types import Response


def _get_kwargs(
    employer_id: str,
    id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/employees/{id}/departments".format(
        client.base_url, employerId=employer_id, id=id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "get",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[List[DepartmentMembership]]:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = DepartmentMembership.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[List[DepartmentMembership]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    id: str,
    *,
    client: Client,
) -> Response[List[DepartmentMembership]]:
    """Get Employee Departments

    Args:
        employer_id (str):
        id (str):

    Returns:
        Response[List[DepartmentMembership]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    employer_id: str,
    id: str,
    *,
    client: Client,
) -> Optional[List[DepartmentMembership]]:
    """Get Employee Departments

    Args:
        employer_id (str):
        id (str):

    Returns:
        Response[List[DepartmentMembership]]
    """

    return sync_detailed(
        employer_id=employer_id,
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    id: str,
    *,
    client: Client,
) -> Response[List[DepartmentMembership]]:
    """Get Employee Departments

    Args:
        employer_id (str):
        id (str):

    Returns:
        Response[List[DepartmentMembership]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    id: str,
    *,
    client: Client,
) -> Optional[List[DepartmentMembership]]:
    """Get Employee Departments

    Args:
        employer_id (str):
        id (str):

    Returns:
        Response[List[DepartmentMembership]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            id=id,
            client=client,
        )
    ).parsed
