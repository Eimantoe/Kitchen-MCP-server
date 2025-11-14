from .HTTPClientManager import http_client_manager
from .Logger import logger

async def startup_http_client():
    logger.info("Starting http client manager...")
    await http_client_manager.start()
    logger.info("Http client manager has been started")

async def shutdown_http_client():
    logger.info("Shutting down http client manager...")
    await http_client_manager.stop()
    logger.info("http client manager is shut down...")
