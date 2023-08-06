from typing import Any, Dict, Optional

import httpx

from ...client import Client
from ...models.get_hub_script_by_path_response_200 import GetHubScriptByPathResponse200
from ...types import Response


def _get_kwargs(
    *,
    client: Client,
    path: str,
) -> Dict[str, Any]:
    url = "{}/scripts/hub/get_full/{path}".format(client.base_url, path=path)

    headers: Dict[str, Any] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
    }


def _parse_response(*, response: httpx.Response) -> Optional[GetHubScriptByPathResponse200]:
    if response.status_code == 200:
        response_200 = GetHubScriptByPathResponse200.from_dict(response.json())

        return response_200
    return None


def _build_response(*, response: httpx.Response) -> Response[GetHubScriptByPathResponse200]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    path: str,
) -> Response[GetHubScriptByPathResponse200]:
    kwargs = _get_kwargs(
        client=client,
        path=path,
    )

    response = httpx.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    path: str,
) -> Optional[GetHubScriptByPathResponse200]:
    """ """

    return sync_detailed(
        client=client,
        path=path,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    path: str,
) -> Response[GetHubScriptByPathResponse200]:
    kwargs = _get_kwargs(
        client=client,
        path=path,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    path: str,
) -> Optional[GetHubScriptByPathResponse200]:
    """ """

    return (
        await asyncio_detailed(
            client=client,
            path=path,
        )
    ).parsed
