from pydantic_settings import BaseSettings, SettingsConfigDict
    
class Settings(BaseSettings): # type: ignore
    debug_mode: bool = True

    waitress_service_url : str = "http://localhost:6000"
    waitress_service_menu_endpoint : str = waitress_service_url + "/menu"
    waitress_service_place_order_endpoint : str = waitress_service_url + "/place-order"

    model_config = SettingsConfigDict(
        env_file=".restaurantvenv",
        env_file_encoding="utf-8"
    )

    USER_AGENT : str = "Restaurant-MCP/1.0"

settings = Settings()