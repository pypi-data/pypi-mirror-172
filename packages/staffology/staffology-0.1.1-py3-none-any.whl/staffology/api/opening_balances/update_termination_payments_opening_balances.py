from typing import Any, Dict, Optional, Union, cast

import httpx

from ...client import Client
from ...models.opening_balances import OpeningBalances
from ...types import Response


def _get_kwargs(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
    json_body: OpeningBalances,
) -> Dict[str, Any]:
    url = "{}/employers/{employerId}/employees/{employeeId}/openingBalances/terminationpayments".format(
        client.base_url, employerId=employer_id, employeeId=employee_id
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


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[Any, OpeningBalances]]:
    if response.status_code == 200:
        response_200 = OpeningBalances.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = cast(Any, None)
        return response_400
    if response.status_code == 404:
        response_404 = cast(Any, None)
        return response_404
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[Any, OpeningBalances]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
    json_body: OpeningBalances,
) -> Response[Union[Any, OpeningBalances]]:
    """Update Termination Pay

     Updates the Termination Pay value on the Opening Balances for an Employee.
    This would ideally be done when the Opening Balances are updated but if payruns have already been
    started for the employee then Opening Balances can't be updated - hence this API call just to update
    the Termination Pay value.
    Only the TerminationPayments property of the submitted OpeningBalances model is updated.

    Args:
        employer_id (str):
        employee_id (str):
        json_body (OpeningBalances):

    Returns:
        Response[Union[Any, OpeningBalances]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
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
    employee_id: str,
    *,
    client: Client,
    json_body: OpeningBalances,
) -> Optional[Union[Any, OpeningBalances]]:
    """Update Termination Pay

     Updates the Termination Pay value on the Opening Balances for an Employee.
    This would ideally be done when the Opening Balances are updated but if payruns have already been
    started for the employee then Opening Balances can't be updated - hence this API call just to update
    the Termination Pay value.
    Only the TerminationPayments property of the submitted OpeningBalances model is updated.

    Args:
        employer_id (str):
        employee_id (str):
        json_body (OpeningBalances):

    Returns:
        Response[Union[Any, OpeningBalances]]
    """

    return sync_detailed(
        employer_id=employer_id,
        employee_id=employee_id,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
    json_body: OpeningBalances,
) -> Response[Union[Any, OpeningBalances]]:
    """Update Termination Pay

     Updates the Termination Pay value on the Opening Balances for an Employee.
    This would ideally be done when the Opening Balances are updated but if payruns have already been
    started for the employee then Opening Balances can't be updated - hence this API call just to update
    the Termination Pay value.
    Only the TerminationPayments property of the submitted OpeningBalances model is updated.

    Args:
        employer_id (str):
        employee_id (str):
        json_body (OpeningBalances):

    Returns:
        Response[Union[Any, OpeningBalances]]
    """

    kwargs = _get_kwargs(
        employer_id=employer_id,
        employee_id=employee_id,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(response=response)


async def asyncio(
    employer_id: str,
    employee_id: str,
    *,
    client: Client,
    json_body: OpeningBalances,
) -> Optional[Union[Any, OpeningBalances]]:
    """Update Termination Pay

     Updates the Termination Pay value on the Opening Balances for an Employee.
    This would ideally be done when the Opening Balances are updated but if payruns have already been
    started for the employee then Opening Balances can't be updated - hence this API call just to update
    the Termination Pay value.
    Only the TerminationPayments property of the submitted OpeningBalances model is updated.

    Args:
        employer_id (str):
        employee_id (str):
        json_body (OpeningBalances):

    Returns:
        Response[Union[Any, OpeningBalances]]
    """

    return (
        await asyncio_detailed(
            employer_id=employer_id,
            employee_id=employee_id,
            client=client,
            json_body=json_body,
        )
    ).parsed
