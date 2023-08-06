from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.employer_email import EmployerEmail
from ...types import Response


def _get_kwargs(
    employer_id: str,
    email_id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/email/{emailId}".format(
        client.base_url, employerId=employer_id, emailId=email_id
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


def _parse_response(*, response: httpx.Response) -> Optional[EmployerEmail]:
    if response.status_code == 200:
        response_200 = EmployerEmail.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[EmployerEmail]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    email_id: str,
    *,
    client: Client,
) -> Response[EmployerEmail]:
    """Get Email

     Returns the email along with its status.

    Args:
        employer_id (str):
        email_id (str):

    Returns:
        Response[EmployerEmail]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        email_id=email_id,
        client=client,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    employer_id: str,
    email_id: str,
    *,
    client: Client,
) -> Optional[EmployerEmail]:
    """Get Email

     Returns the email along with its status.

    Args:
        employer_id (str):
        email_id (str):

    Returns:
        Response[EmployerEmail]
    """

    return sync_detailed(
        employer_id=employer_id,
        email_id=email_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    email_id: str,
    *,
    client: Client,
) -> Response[EmployerEmail]:
    """Get Email

     Returns the email along with its status.

    Args:
        employer_id (str):
        email_id (str):

    Returns:
        Response[EmployerEmail]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        email_id=email_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    email_id: str,
    *,
    client: Client,
) -> Optional[EmployerEmail]:
    """Get Email

     Returns the email along with its status.

    Args:
        employer_id (str):
        email_id (str):

    Returns:
        Response[EmployerEmail]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            email_id=email_id,
            client=client,
        )
    ).parsed
