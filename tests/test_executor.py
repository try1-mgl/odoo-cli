import pytest

from core.connector import OdooConnector
from core.executor import OdooExecutor


@pytest.fixture(scope="module")
def odoo_connector():
    """Fixture to provide a connected OdooConnector instance."""
    try:
        conn = OdooConnector()
        return conn
    except Exception as e:
        pytest.skip(f"Odoo is not available or profile is misconfigured: {e}")


@pytest.fixture(scope="module")
def executor(odoo_connector):
    """Fixture to provide an OdooExecutor instance."""
    return OdooExecutor(odoo_connector)


def test_connection_uid(odoo_connector):
    """Test that the connector successfully retrieves a UID."""
    assert odoo_connector.uid is not None
    assert isinstance(odoo_connector.uid, int)
    assert odoo_connector.uid > 0


def test_executor_search(executor):
    """Test that the executor can perform a basic search on res.users."""
    result = executor.search("res.users", [], limit=1)
    assert isinstance(result, list)
    assert len(result) > 0


def test_executor_read(executor):
    """Test that the executor can read fields of a specific user."""
    # First find a user
    user_ids = executor.search("res.users", [], limit=1)

    # Read the name field
    users = executor.read("res.users", user_ids, fields=["name", "login"])
    assert isinstance(users, list)
    assert len(users) == 1
    assert "name" in users[0]
    assert "login" in users[0]
