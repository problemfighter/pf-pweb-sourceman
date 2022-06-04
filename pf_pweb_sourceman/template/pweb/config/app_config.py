class Config:
    APP_NAME = "__APP_NAME__"
    PORT: int = __APP_PORT__

    ENABLE_AUTH_SYSTEM: bool = True

    # Swagger Configuration
    ENABLE_SWAGGER_VIEW_PAGE: bool = True
    ENABLE_SWAGGER_PAGE_AUTH: bool = False
    SWAGGER_ENABLE: bool = True
    SWAGGER_TITLE: str = "__APP_NAME__"

    # API
    ENABLE_API_AUTH: bool = True
    ENABLE_API_END_POINTS: bool = True
    SWAGGER_ENABLE_JWT_AUTH_GLOBAL: bool = True

