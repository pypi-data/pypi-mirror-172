from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.report_pack import ReportPack
from ...types import Response


def _get_kwargs(
    employer_id: str,
    *,
    client: Client,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/bureau/settings/reportpack".format(
        client.base_url, employerId=employer_id
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


def _parse_response(*, response: httpx.Response) -> Optional[ReportPack]:
    if response.status_code == 200:
        response_200 = ReportPack.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[ReportPack]:
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
) -> Response[ReportPack]:
    """Get BureauSettings ReportPack

     If a ReportPack is specified in the BureauSettings then it is returned, otherwise an empty
    ReportPAck is returned

    Args:
        employer_id (str):

    Returns:
        Response[ReportPack]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
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
) -> Optional[ReportPack]:
    """Get BureauSettings ReportPack

     If a ReportPack is specified in the BureauSettings then it is returned, otherwise an empty
    ReportPAck is returned

    Args:
        employer_id (str):

    Returns:
        Response[ReportPack]
    """

    return sync_detailed(
        employer_id=employer_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    *,
    client: Client,
) -> Response[ReportPack]:
    """Get BureauSettings ReportPack

     If a ReportPack is specified in the BureauSettings then it is returned, otherwise an empty
    ReportPAck is returned

    Args:
        employer_id (str):

    Returns:
        Response[ReportPack]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        client=client,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    *,
    client: Client,
) -> Optional[ReportPack]:
    """Get BureauSettings ReportPack

     If a ReportPack is specified in the BureauSettings then it is returned, otherwise an empty
    ReportPAck is returned

    Args:
        employer_id (str):

    Returns:
        Response[ReportPack]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            client=client,
        )
    ).parsed
