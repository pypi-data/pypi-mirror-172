from typing import Any, Dict, Optional, cast

import httpx

from ...client import Client
from ...types import Response


def _get_kwargs(
    employer_id: str,
    *,
    client: Client,
    json_body: str,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/dps/notices/xml".format(
        client.base_url, employerId=employer_id
    )

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    json_json_body = json_body

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "json": json_json_body,
    }


def _parse_response(*, response: httpx.Response) -> Optional[int]:
    if response.status_code == 200:
        response_200 = cast(int, response.json())
        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[int]:
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
    json_body: str,
) -> Response[int]:
    """Parse notices from XML

     Checks the supplied XML string for notices. They're then processed in the same was as if received
    from HMRC.
    Only used for testing the parsing of DPS XML.
    Returns an integer showing how many new notices were found

    Args:
        employer_id (str):
        json_body (str):

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
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
    *,
    client: Client,
    json_body: str,
) -> Optional[int]:
    """Parse notices from XML

     Checks the supplied XML string for notices. They're then processed in the same was as if received
    from HMRC.
    Only used for testing the parsing of DPS XML.
    Returns an integer showing how many new notices were found

    Args:
        employer_id (str):
        json_body (str):

    Returns:
        Response[int]
    """

    return sync_detailed(
        employer_id=employer_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    *,
    client: Client,
    json_body: str,
) -> Response[int]:
    """Parse notices from XML

     Checks the supplied XML string for notices. They're then processed in the same was as if received
    from HMRC.
    Only used for testing the parsing of DPS XML.
    Returns an integer showing how many new notices were found

    Args:
        employer_id (str):
        json_body (str):

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    *,
    client: Client,
    json_body: str,
) -> Optional[int]:
    """Parse notices from XML

     Checks the supplied XML string for notices. They're then processed in the same was as if received
    from HMRC.
    Only used for testing the parsing of DPS XML.
    Returns an integer showing how many new notices were found

    Args:
        employer_id (str):
        json_body (str):

    Returns:
        Response[int]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
