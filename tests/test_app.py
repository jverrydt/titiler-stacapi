"""test titiler-stacapi app."""


def test_landing(app):
    """Test / endpoint."""
    response = app.get("/")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    body = response.json()
    assert body["title"] == "titiler-stacapi"
    assert body["links"]

    response = app.get("/?f=html")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "titiler-stacapi" in response.text

    # Check accept headers
    response = app.get("/", headers={"accept": "text/html"})
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "titiler-stacapi" in response.text

    # accept quality
    response = app.get(
        "/", headers={"accept": "application/json;q=0.9, text/html;q=1.0"}
    )
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "titiler-stacapi" in response.text

    # accept quality but only json is available
    response = app.get("/", headers={"accept": "text/csv;q=1.0, application/json"})
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    body = response.json()
    assert body["title"] == "titiler-stacapi"

    # accept quality but only json is available
    response = app.get("/", headers={"accept": "text/csv;q=1.0, */*"})
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    body = response.json()
    assert body["title"] == "titiler-stacapi"

    # Invalid accept, return default
    response = app.get("/", headers={"accept": "text/htm"})
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    body = response.json()
    assert body["title"] == "titiler-stacapi"
    assert body["links"]

    # make sure `?f=` has priority over headers
    response = app.get("/?f=json", headers={"accept": "text/html"})
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    body = response.json()
    assert body["title"] == "titiler-stacapi"


def test_docs(app):
    """Test /api endpoint."""
    response = app.get("/api")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    body = response.json()
    assert body["openapi"]

    response = app.get("/api.html")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_debug(app):
    """Test / endpoint."""
    response = app.get("/debug")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    body = response.json()
    assert body["url"] == "http://something.stac"
