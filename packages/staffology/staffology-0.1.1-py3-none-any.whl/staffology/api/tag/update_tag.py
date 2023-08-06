from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.tag import Tag
from ...types import Response


def _get_kwargs(
    employer_id: str,
    code: str,
    *,
    client: Client,
    json_body: Tag,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/tags/{code}".format(
        client.base_url, employerId=employer_id, code=code
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[Tag]:
    if response.status_code == 200:
        response_200 = Tag.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Tag]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    code: str,
    *,
    client: Client,
    json_body: Tag,
) -> Response[Tag]:
    """Update Tag

     Updates a Tag for the Employer.

    Args:
        employer_id (str):
        code (str):
        json_body (Tag):

    Returns:
        Response[Tag]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        code=code,
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
    code: str,
    *,
    client: Client,
    json_body: Tag,
) -> Optional[Tag]:
    """Update Tag

     Updates a Tag for the Employer.

    Args:
        employer_id (str):
        code (str):
        json_body (Tag):

    Returns:
        Response[Tag]
    """

    return sync_detailed(
        employer_id=employer_id,
        code=code,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    code: str,
    *,
    client: Client,
    json_body: Tag,
) -> Response[Tag]:
    """Update Tag

     Updates a Tag for the Employer.

    Args:
        employer_id (str):
        code (str):
        json_body (Tag):

    Returns:
        Response[Tag]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        code=code,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    code: str,
    *,
    client: Client,
    json_body: Tag,
) -> Optional[Tag]:
    """Update Tag

     Updates a Tag for the Employer.

    Args:
        employer_id (str):
        code (str):
        json_body (Tag):

    Returns:
        Response[Tag]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            code=code,
            client=client,
            json_body=json_body,
        )
    ).parsed
