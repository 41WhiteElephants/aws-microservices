import pytest
from dataclasses import dataclass


def pytest_addoption(parser):
    parser.addoption("--api_url", action="store")


@pytest.fixture()
def api_url(request):
    api_url_value = request.config.option.api_url
    if api_url_value is None:
        pytest.skip()
    return api_url_value


@pytest.fixture
def lambda_context():
    @dataclass
    class LambdaContext:
        function_name: str = "test"
        aws_request_id: str = "88888888-4444-4444-4444-121212121212"
        invoked_function_arn: str = "arn:aws:lambda:eu-west-1:123456789101:function:test"

    return LambdaContext()
