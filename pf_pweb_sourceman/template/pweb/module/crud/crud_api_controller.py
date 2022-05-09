from flask import Blueprint

url_prefix = "/api/v1/__url_name__"
__name__api_controller = Blueprint(
    "__name__api_controller",
    __name__,
    url_prefix=url_prefix
)




