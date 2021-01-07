import pytest
from docker.models.containers import Container


@pytest.fixture
def frontend_container(docker_client) -> Container:
    yield docker_client.containers.get("frontend")
