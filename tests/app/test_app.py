import os
import pytest
import redis
import requests
from requests.exceptions import ConnectionError


def is_responsive(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except ConnectionError:
        return False

@pytest.fixture(scope="session")
def web_service(docker_ip, docker_services):
    """Ensure that web service is up and responsive."""
    # `port_for` takes a container port and returns the corresponding host port
    port = docker_services.port_for("web", 5000)
    url = "http://{}:{}".format(docker_ip, port)
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_responsive(url)
    )
    return url

@pytest.fixture(scope="session") #TODO: Correct fixture to return Redis service
def redis_service(docker_ip, docker_services):
    """Ensure that redis service is up and responsive."""
    redis_host = os.getenv('REDIS_HOST')
    redis_port = int(os.getenv('REDIS_PORT'))
    port = docker_services.port_for("redis", redis_port)
    url = "http://{}:{}".format(docker_ip, port)
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_responsive(url)
    )
    return redis.Redis(host=redis_host, port=redis_port)

def test_web_service_is_running(web_service):
    response = requests.get(web_service)
    assert response.status_code == 200

def test_redis_db_is_running(redis_service):
    pass #TODO: Correct once redis fixture is in place
    # assert redis_service.ping()
