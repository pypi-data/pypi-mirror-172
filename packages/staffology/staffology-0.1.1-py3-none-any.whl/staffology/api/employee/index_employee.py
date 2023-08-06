from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.employee_status import EmployeeStatus
from ...models.item import Item
from ...types import UNSET, Response, Unset


def _get_kwargs(
    employer_id: str,
    *,
    client: Client,
    page_num: Union[Unset, None, int] = UNSET,
    page_size: Union[Unset, None, int] = UNSET,
    status: Union[Unset, None, EmployeeStatus] = UNSET,
    dept_code: Union[Unset, None, str] = UNSET,
    pension_scheme_id: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/employees".format(
        client.base_url, employerId=employer_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["pageNum"] = page_num

    params["pageSize"] = page_size

    json_status: Union[Unset, None, str] = UNSET
    if not isinstance(status, Unset):
        json_status = status.value if status else None

    params["status"] = json_status

    params["deptCode"] = dept_code

    params["pensionSchemeId"] = pension_scheme_id

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
    page_num: Union[Unset, None, int] = UNSET,
    page_size: Union[Unset, None, int] = UNSET,
    status: Union[Unset, None, EmployeeStatus] = UNSET,
    dept_code: Union[Unset, None, str] = UNSET,
    pension_scheme_id: Union[Unset, None, str] = UNSET,
) -> Response[List[Item]]:
    """List Employees

    Args:
        employer_id (str):
        page_num (Union[Unset, None, int]):
        page_size (Union[Unset, None, int]):
        status (Union[Unset, None, EmployeeStatus]): [readonly] Indicates whether the Employee is
            currently employed or not
        dept_code (Union[Unset, None, str]):
        pension_scheme_id (Union[Unset, None, str]):

    Returns:
        Response[List[Item]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        page_num=page_num,
        page_size=page_size,
        status=status,
        dept_code=dept_code,
        pension_scheme_id=pension_scheme_id,
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
    page_num: Union[Unset, None, int] = UNSET,
    page_size: Union[Unset, None, int] = UNSET,
    status: Union[Unset, None, EmployeeStatus] = UNSET,
    dept_code: Union[Unset, None, str] = UNSET,
    pension_scheme_id: Union[Unset, None, str] = UNSET,
) -> Optional[List[Item]]:
    """List Employees

    Args:
        employer_id (str):
        page_num (Union[Unset, None, int]):
        page_size (Union[Unset, None, int]):
        status (Union[Unset, None, EmployeeStatus]): [readonly] Indicates whether the Employee is
            currently employed or not
        dept_code (Union[Unset, None, str]):
        pension_scheme_id (Union[Unset, None, str]):

    Returns:
        Response[List[Item]]
    """

    return sync_detailed(
        employer_id=employer_id,
        client=client,
        page_num=page_num,
        page_size=page_size,
        status=status,
        dept_code=dept_code,
        pension_scheme_id=pension_scheme_id,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    *,
    client: Client,
    page_num: Union[Unset, None, int] = UNSET,
    page_size: Union[Unset, None, int] = UNSET,
    status: Union[Unset, None, EmployeeStatus] = UNSET,
    dept_code: Union[Unset, None, str] = UNSET,
    pension_scheme_id: Union[Unset, None, str] = UNSET,
) -> Response[List[Item]]:
    """List Employees

    Args:
        employer_id (str):
        page_num (Union[Unset, None, int]):
        page_size (Union[Unset, None, int]):
        status (Union[Unset, None, EmployeeStatus]): [readonly] Indicates whether the Employee is
            currently employed or not
        dept_code (Union[Unset, None, str]):
        pension_scheme_id (Union[Unset, None, str]):

    Returns:
        Response[List[Item]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        page_num=page_num,
        page_size=page_size,
        status=status,
        dept_code=dept_code,
        pension_scheme_id=pension_scheme_id,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    *,
    client: Client,
    page_num: Union[Unset, None, int] = UNSET,
    page_size: Union[Unset, None, int] = UNSET,
    status: Union[Unset, None, EmployeeStatus] = UNSET,
    dept_code: Union[Unset, None, str] = UNSET,
    pension_scheme_id: Union[Unset, None, str] = UNSET,
) -> Optional[List[Item]]:
    """List Employees

    Args:
        employer_id (str):
        page_num (Union[Unset, None, int]):
        page_size (Union[Unset, None, int]):
        status (Union[Unset, None, EmployeeStatus]): [readonly] Indicates whether the Employee is
            currently employed or not
        dept_code (Union[Unset, None, str]):
        pension_scheme_id (Union[Unset, None, str]):

    Returns:
        Response[List[Item]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            client=client,
            page_num=page_num,
            page_size=page_size,
            status=status,
            dept_code=dept_code,
            pension_scheme_id=pension_scheme_id,
        )
    ).parsed
