from inversity_api.main import get_openapi_docs_config


def test_get_openapi_docs_config_enables_docs_in_dev() -> None:
    assert get_openapi_docs_config("dev") == ("/docs", "/openapi.json")


def test_get_openapi_docs_config_disables_docs_outside_dev() -> None:
    assert get_openapi_docs_config("production") == (None, None)
    assert get_openapi_docs_config(None) == (None, None)
