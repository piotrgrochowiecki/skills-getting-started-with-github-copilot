import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities database between tests."""
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(copy.deepcopy(original))
