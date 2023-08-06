from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.employee import Employee
from ...models.update_photo_employee_multipart_data import (
    UpdatePhotoEmployeeMultipartData,
)
from ...types import Response


def _get_kwargs(
    employer_id: str,
    id: str,
    *,
    client: Client,
    multipart_data: UpdatePhotoEmployeeMultipartData,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/employees/{id}/photo".format(
        client.base_url, employerId=employer_id, id=id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    multipart_multipart_data = multipart_data.to_multipart()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "files": multipart_multipart_data,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Employee]:
    if response.status_code == 200:
        response_200 = Employee.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Employee]:
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
    multipart_data: UpdatePhotoEmployeeMultipartData,
) -> Response[Employee]:
    """Update Photo

     If you already have a URL for the employee photo then you can just set the PhotoUrl property of the
    Employee.
    Alternatively, submit an image here and we'll upload it, resize it to 200px squared and set the
    PhotoUrl for you.

    Args:
        employer_id (str):
        id (str):
        multipart_data (UpdatePhotoEmployeeMultipartData):

    Returns:
        Response[Employee]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        client=client,
        multipart_data=multipart_data,
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
    multipart_data: UpdatePhotoEmployeeMultipartData,
) -> Optional[Employee]:
    """Update Photo

     If you already have a URL for the employee photo then you can just set the PhotoUrl property of the
    Employee.
    Alternatively, submit an image here and we'll upload it, resize it to 200px squared and set the
    PhotoUrl for you.

    Args:
        employer_id (str):
        id (str):
        multipart_data (UpdatePhotoEmployeeMultipartData):

    Returns:
        Response[Employee]
    """

    return sync_detailed(
        employer_id=employer_id,
        id=id,
        client=client,
        multipart_data=multipart_data,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    id: str,
    *,
    client: Client,
    multipart_data: UpdatePhotoEmployeeMultipartData,
) -> Response[Employee]:
    """Update Photo

     If you already have a URL for the employee photo then you can just set the PhotoUrl property of the
    Employee.
    Alternatively, submit an image here and we'll upload it, resize it to 200px squared and set the
    PhotoUrl for you.

    Args:
        employer_id (str):
        id (str):
        multipart_data (UpdatePhotoEmployeeMultipartData):

    Returns:
        Response[Employee]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        client=client,
        multipart_data=multipart_data,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    id: str,
    *,
    client: Client,
    multipart_data: UpdatePhotoEmployeeMultipartData,
) -> Optional[Employee]:
    """Update Photo

     If you already have a URL for the employee photo then you can just set the PhotoUrl property of the
    Employee.
    Alternatively, submit an image here and we'll upload it, resize it to 200px squared and set the
    PhotoUrl for you.

    Args:
        employer_id (str):
        id (str):
        multipart_data (UpdatePhotoEmployeeMultipartData):

    Returns:
        Response[Employee]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            id=id,
            client=client,
            multipart_data=multipart_data,
        )
    ).parsed
