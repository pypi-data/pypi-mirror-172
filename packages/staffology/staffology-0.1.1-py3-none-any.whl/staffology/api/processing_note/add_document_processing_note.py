from typing import Any, Dict

import httpx

from ...client import Client
from ...models.add_document_processing_note_multipart_data import (
    AddDocumentProcessingNoteMultipartData,
)
from ...types import Response


def _get_kwargs(
    employer_id: str,
    id: str,
    *,
    client: Client,
    multipart_data: AddDocumentProcessingNoteMultipartData,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/payrun/{id}/documents".format(
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


def _build_response(*, response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=None,
    )


def sync_detailed(
    employer_id: str,
    id: str,
    *,
    client: Client,
    multipart_data: AddDocumentProcessingNoteMultipartData,
) -> Response[Any]:
    """Add Document

     Adds document to the ProcessingNote

    Args:
        employer_id (str):
        id (str):
        multipart_data (AddDocumentProcessingNoteMultipartData):

    Returns:
        Response[Any]
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


async def asyncio_detailed(
    employer_id: str,
    id: str,
    *,
    client: Client,
    multipart_data: AddDocumentProcessingNoteMultipartData,
) -> Response[Any]:
    """Add Document

     Adds document to the ProcessingNote

    Args:
        employer_id (str):
        id (str):
        multipart_data (AddDocumentProcessingNoteMultipartData):

    Returns:
        Response[Any]
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
