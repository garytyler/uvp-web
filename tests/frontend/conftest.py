import pytest


@pytest.fixture
def cls_browser(browser, request):
    request.cls.browser = browser


@pytest.fixture
def cls_random_string_factory(random_string_factory, request):
    request.random_string_factory = random_string_factory
