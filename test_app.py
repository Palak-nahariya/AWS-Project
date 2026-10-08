from app import app


def test_app_exists():
    """Make sure the Flask application is created."""
    assert app is not None


def test_app_can_start():
    """Make sure the Flask application can handle a request."""
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.get("/")

        assert response.status_code in (200, 404)
