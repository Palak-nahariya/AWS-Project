def test_app_exists():
    """Make sure the Flask application is created."""
    assert app is not None


def test_app_is_testing():
    """Make sure Flask's test client can be created."""
    app.config["TESTING"] = True

    with app.test_client() as client:
        response = client.get("/")
