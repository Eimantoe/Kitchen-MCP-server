from typing import Any, List, Dict

from mcp.server.fastmcp import FastMCP

from shared.Settings import settings
from shared.Logger import logger
from shared.APIRequest import APIRequest
from shared.Lifecycle import (
    startup_http_client,
    shutdown_http_client
)
from contextlib import asynccontextmanager
from shared.models.WaitressServiceModel import PlaceOrderRequest

@asynccontextmanager
async def lifespan(mcp: FastMCP):
    # Startup actions
    await startup_http_client()
    yield
    # Shutdown actions
    await shutdown_http_client()

mcp = FastMCP("Restaurant MCP", lifespan=lifespan, port=9000, debug=settings.debug_mode)

@mcp.tool(description="Fetches the menu from the Waitress service.")
async def get_menu() -> Any:
   
    api_request = APIRequest(method=APIRequest.Method.GET, url=settings.waitress_service_menu_endpoint)

    response = await api_request.sendRequest()
    logger.info("Menu fetched successfully", menu=response.json())

    return response.json()

@mcp.tool(description="Places an order via the Waitress service.")
async def place_order(table_no: int, items: List[Dict[str, int]], comments : str = "") -> Any:

    place_order_request = PlaceOrderRequest(
        table_no=table_no,
        items=items,
        comments=comments
    )

    json_payload = place_order_request.model_dump()
    logger.info("Placing order", order=json_payload)

    api_request = APIRequest(APIRequest.Method.POST, settings.waitress_service_place_order_endpoint, payload=json_payload)

    response = await api_request.sendRequest()

    logger.info("Order placed successfully", order=response.json())



    return response.json()

@mcp.tool(description="You can check if the certain order is ready by providing the order ID.")
async def check_order_status(order_id: int) -> str:
    
    api_request = APIRequest(APIRequest.Method.GET, settings.waitress_service_url + f"/order/{order_id}/status")
    response = await api_request.sendRequest()
    logger.info("Order status fetched successfully", status=response.json())

    responseData = response.json()
    return responseData['results']

def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()