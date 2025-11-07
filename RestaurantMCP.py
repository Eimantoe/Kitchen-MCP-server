from typing import Any
from mcp.server.fastmcp import FastMCP

from kitchen_commons.shared.APIRequest import APIRequest
from kitchen_commons.shared.Logging import logger
from kitchen_commons.shared.Settings import settings

mcp = FastMCP("Restaurant MCP")


# Tool to fetch the menu from the Waitress service
@mcp.tool()
async def get_menu() -> Any:
    """tw
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