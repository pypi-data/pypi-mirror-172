from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.webhook import Webhook
from ...types import Response


def _get_kwargs(
    employer_id: str,
    id: str,
    *,
    client: Client,
    json_body: Webhook,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/webhooks/{id}".format(
        client.base_url, employerId=employer_id, id=id
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


def _parse_response(*, response: httpx.Response) -> Optional[Webhook]:
    if response.status_code == 200:
        response_200 = Webhook.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[Webhook]:
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
    json_body: Webhook,
) -> Response[Webhook]:
    """Update Webhook

     Updates a Webhook for the Employer.

    Args:
        employer_id (str):
        id (str):
        json_body (Webhook):

    Returns:
        Response[Webhook]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
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
    id: str,
    *,
    client: Client,
    json_body: Webhook,
) -> Optional[Webhook]:
    """Update Webhook

     Updates a Webhook for the Employer.

    Args:
        employer_id (str):
        id (str):
        json_body (Webhook):

    Returns:
        Response[Webhook]
    """

    return sync_detailed(
        employer_id=employer_id,
        id=id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    id: str,
    *,
    client: Client,
    json_body: Webhook,
) -> Response[Webhook]:
    """Update Webhook

     Updates a Webhook for the Employer.

    Args:
        employer_id (str):
        id (str):
        json_body (Webhook):

    Returns:
        Response[Webhook]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        id=id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    id: str,
    *,
    client: Client,
    json_body: Webhook,
) -> Optional[Webhook]:
    """Update Webhook

     Updates a Webhook for the Employer.

    Args:
        employer_id (str):
        id (str):
        json_body (Webhook):

    Returns:
        Response[Webhook]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            id=id,
            client=client,
            json_body=json_body,
        )
    ).parsed
