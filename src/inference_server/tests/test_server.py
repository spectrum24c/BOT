import pytest
from fastapi.testclient import TestClient
from src.inference_server.server import app

client = TestClient(app)

def test_infer():
    response = client.post('/infer', json={"features": [[0.001, 0.01, 0.05]]})
    assert response.status_code == 200
    assert 'prediction' in response.json() or 'error' in response.json()
