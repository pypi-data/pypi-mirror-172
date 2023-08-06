from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.mail_settings import MailSettings
from ...types import Response


def _get_kwargs(
    employer_id: str,
    *,
    client: Client,
    json_body: MailSettings,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/email/settings".format(
        client.base_url, employerId=employer_id
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


def _parse_response(*, response: httpx.Response) -> Optional[MailSettings]:
    if response.status_code == 200:
        response_200 = MailSettings.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[MailSettings]:
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
    json_body: MailSettings,
) -> Response[MailSettings]:
    """Update MailSettings

     Updates the MailSettings for an Employer.

    Args:
        employer_id (str):
        json_body (MailSettings): Determines the settings used when the Employer sends emails.
            If CustomiseSmtpSettings is false then SmtpSettings will be null and our default internal
            settings will be used;

    Returns:
        Response[MailSettings]
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
    json_body: MailSettings,
) -> Optional[MailSettings]:
    """Update MailSettings

     Updates the MailSettings for an Employer.

    Args:
        employer_id (str):
        json_body (MailSettings): Determines the settings used when the Employer sends emails.
            If CustomiseSmtpSettings is false then SmtpSettings will be null and our default internal
            settings will be used;

    Returns:
        Response[MailSettings]
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
    json_body: MailSettings,
) -> Response[MailSettings]:
    """Update MailSettings

     Updates the MailSettings for an Employer.

    Args:
        employer_id (str):
        json_body (MailSettings): Determines the settings used when the Employer sends emails.
            If CustomiseSmtpSettings is false then SmtpSettings will be null and our default internal
            settings will be used;

    Returns:
        Response[MailSettings]
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
    json_body: MailSettings,
) -> Optional[MailSettings]:
    """Update MailSettings

     Updates the MailSettings for an Employer.

    Args:
        employer_id (str):
        json_body (MailSettings): Determines the settings used when the Employer sends emails.
            If CustomiseSmtpSettings is false then SmtpSettings will be null and our default internal
            settings will be used;

    Returns:
        Response[MailSettings]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
