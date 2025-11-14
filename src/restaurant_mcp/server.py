from typing import Any

from mcp.server.fastmcp import FastMCP

from shared.Settings import settings
from shared.Logger import logger
from shared.APIRequest import APIRequest
from shared.Lifecycle import (
    startup_http_client,
    shutdown_http_client
)

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastMCP):
    await startup_http_client()
    
    yield

    await shutdown_http_client()

mcp = FastMCP("Restaurant MCP", lifespan=lifespan)

# Tool to fetch the menu from the Waitress service
@mcp.tool()
async def get_menu() -> Any:
    """
    Fetches the menu from the Waitress service.
    """
    api_request = APIRequest(
        method=APIRequest.Method.GET,
        url=f"{settings.waitress_service_url}/menu"
    )
    response = await api_request.sendRequest()
    logger.info("Menu fetched successfully", menu=response.json())
    return response.json()


def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()