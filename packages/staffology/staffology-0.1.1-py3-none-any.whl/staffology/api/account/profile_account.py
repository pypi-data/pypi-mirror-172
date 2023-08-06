from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.user import User
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    json_body: User,
) -> Dict[str, Any]:
    url = "{}/account/profile".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[User]:
    if response.status_code == 200:
        response_200 = User.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[User]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    json_body: User,
) -> Response[User]:
    """Update Profile

     Updates your profile. Only Salutation, FirstName, LastName, JobType, JobTitle, TelephoneNumber,
    BusinessName, Industry, Address and DisplayPrefs fields are updated.

    Args:
        json_body (User): Represents a User Account.
            As well as basic details about the user it also includes details of Employers that the
            user account can access.

    Returns:
        Response[User]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    json_body: User,
) -> Optional[User]:
    """Update Profile

     Updates your profile. Only Salutation, FirstName, LastName, JobType, JobTitle, TelephoneNumber,
    BusinessName, Industry, Address and DisplayPrefs fields are updated.

    Args:
        json_body (User): Represents a User Account.
            As well as basic details about the user it also includes details of Employers that the
            user account can access.

    Returns:
        Response[User]
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    json_body: User,
) -> Response[User]:
    """Update Profile

     Updates your profile. Only Salutation, FirstName, LastName, JobType, JobTitle, TelephoneNumber,
    BusinessName, Industry, Address and DisplayPrefs fields are updated.

    Args:
        json_body (User): Represents a User Account.
            As well as basic details about the user it also includes details of Employers that the
            user account can access.

    Returns:
        Response[User]
    """

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    json_body: User,
) -> Optional[User]:
    """Update Profile

     Updates your profile. Only Salutation, FirstName, LastName, JobType, JobTitle, TelephoneNumber,
    BusinessName, Industry, Address and DisplayPrefs fields are updated.

    Args:
        json_body (User): Represents a User Account.
            As well as basic details about the user it also includes details of Employers that the
            user account can access.

    Returns:
        Response[User]
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
