"""Import all routers and add them to routers_list."""
from .user import auth_router
from .answer import answer_router
from .gpt import gpt_router

routers_list = [
    auth_router,
    answer_router,
    gpt_router,

]

__all__ = [
    "routers_list",
]
