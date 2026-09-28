from src.modules import modules
from src.modules.user.api.router import router


def test_module_registered() -> None:
    assert modules["user"] == "src.modules.user"


def test_router_prefix() -> None:
    assert router.prefix == "/users"
