from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.employer_template import EmployerTemplate
from ...models.employer_template_type import EmployerTemplateType
from ...types import Response


def _get_kwargs(
    employer_id: str,
    type: EmployerTemplateType,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/templates/{type}".format(
        client.base_url, employerId=employer_id, type=type
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


def _parse_response(*, response: httpx.Response) -> Optional[EmployerTemplate]:
    if response.status_code == 200:
        response_200 = EmployerTemplate.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[EmployerTemplate]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    type: EmployerTemplateType,
    *,
    client: Client,
) -> Response[EmployerTemplate]:
    """Get EmployerTemplate

     Gets the EmployerTemplate specified by the Type.

    Args:
        employer_id (str):
        type (EmployerTemplateType):

    Returns:
        Response[EmployerTemplate]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        type=type,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    employer_id: str,
    type: EmployerTemplateType,
    *,
    client: Client,
) -> Optional[EmployerTemplate]:
    """Get EmployerTemplate

     Gets the EmployerTemplate specified by the Type.

    Args:
        employer_id (str):
        type (EmployerTemplateType):

    Returns:
        Response[EmployerTemplate]
    """

    return sync_detailed(
        employer_id=employer_id,
        type=type,
        client=client,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    type: EmployerTemplateType,
    *,
    client: Client,
) -> Response[EmployerTemplate]:
    """Get EmployerTemplate

     Gets the EmployerTemplate specified by the Type.

    Args:
        employer_id (str):
        type (EmployerTemplateType):

    Returns:
        Response[EmployerTemplate]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        type=type,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    type: EmployerTemplateType,
    *,
    client: Client,
) -> Optional[EmployerTemplate]:
    """Get EmployerTemplate

     Gets the EmployerTemplate specified by the Type.

    Args:
        employer_id (str):
        type (EmployerTemplateType):

    Returns:
        Response[EmployerTemplate]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            type=type,
            client=client,
        )
    ).parsed
