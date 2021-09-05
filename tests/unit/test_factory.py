from mercator import create_app
import io


def test_config():
    """Test create_app"""
    assert not create_app().testing


def test_health_check(client):
    """Test /health endpoint"""
    response = client.get("/health")
    assert response.data == b"OK"


def test_map_interface(client):
    """Test /map_interface endpoint"""
    # Create temp file
    with open("tests/unit/testimage.png", 'rb') as img:
        imgByteIO = io.BytesIO(img.read())

    tmp_file = {'file': (imgByteIO, 'testimage.png')}

    response = client.post(
        "/map_interface", content_type='multipart/form-data', data=tmp_file)

    # We only care about the content-type of the response
    assert response.headers.get("content-type") == "application/json"
